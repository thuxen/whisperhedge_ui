"""
Stripe webhook handler for subscription events
This needs to be set up as an API endpoint that Stripe can POST to
"""
from typing import Dict, Any
from supabase import create_client
import os
from datetime import datetime


def log_payment_event(event: Dict[str, Any], supabase_client, user_id: str = None):
    """
    Log all Stripe events to payment_events table for audit trail
    """
    event_obj = event["object"]
    
    payment_event = {
        "stripe_event_id": event.get("id"),
        "user_id": user_id,
        "stripe_customer_id": event_obj.get("customer"),
        "stripe_subscription_id": event_obj.get("subscription"),
        "stripe_invoice_id": event_obj.get("invoice"),
        "stripe_payment_intent_id": event_obj.get("payment_intent"),
        "event_type": event.get("type"),
        "event_status": event_obj.get("status", "succeeded"),
        "amount_cents": event_obj.get("amount_total") or event_obj.get("amount_paid"),
        "currency": event_obj.get("currency", "usd"),
        "metadata": event_obj.get("metadata", {}),
        "raw_event": event,
        "event_timestamp": datetime.fromtimestamp(event["created"]),
    }
    
    supabase_client.table("payment_events").insert(payment_event).execute()


def handle_checkout_completed(event_data: Dict[str, Any], supabase_client, event: Dict[str, Any]):
    """
    Handle checkout.session.completed event
    Updates user subscription when they complete payment
    """
    session = event_data["object"]
    
    user_id = session["metadata"]["user_id"]
    tier_name = session["metadata"]["tier_name"]
    customer_id = session["customer"]
    subscription_id = session["subscription"]
    amount_total = session.get("amount_total", 0)
    
    # Log the event
    log_payment_event(event, supabase_client, user_id)
    
    # Get the plan tier details
    tier_result = supabase_client.table("plan_tiers").select("*").eq("tier_name", tier_name).single().execute()
    
    if not tier_result.data:
        print(f"Plan tier not found: {tier_name}")
        return
    
    tier = tier_result.data
    
    # Update user subscription
    supabase_client.table("user_subscriptions").update({
        "plan_tier_id": tier["id"],
        "subscribed_tvl_limit": tier["max_tvl"],
        "subscribed_position_limit": tier["max_positions"],
        "subscribed_rebalance_frequency": tier["rebalance_frequency"],
        "stripe_customer_id": customer_id,
        "stripe_subscription_id": subscription_id,
        "subscription_status": "active",
    }).eq("user_id", user_id).execute()
    
    # Add to billing history
    supabase_client.table("billing_history").insert({
        "user_id": user_id,
        "payment_date": datetime.now(),
        "amount_cents": amount_total,
        "currency": session.get("currency", "usd"),
        "status": "paid",
        "billing_type": "subscription",
        "plan_tier_name": tier_name,
        "description": f"Subscription to {tier['display_name']} plan",
        "stripe_invoice_id": session.get("invoice"),
        "stripe_payment_intent_id": session.get("payment_intent"),
    }).execute()
    
    print(f"User {user_id} upgraded to {tier_name}")


def handle_subscription_updated(event_data: Dict[str, Any], supabase_client, event: Dict[str, Any]):
    """
    Handle customer.subscription.updated event
    Updates subscription status when changed in Stripe
    """
    subscription = event_data["object"]
    subscription_id = subscription["id"]
    status = subscription["status"]
    current_period_start = datetime.fromtimestamp(subscription["current_period_start"])
    current_period_end = datetime.fromtimestamp(subscription["current_period_end"])
    cancel_at_period_end = subscription.get("cancel_at_period_end", False)
    
    # Get user_id from subscription
    user_result = supabase_client.table("user_subscriptions").select("user_id").eq("stripe_subscription_id", subscription_id).single().execute()
    user_id = user_result.data["user_id"] if user_result.data else None
    
    # Log the event
    if user_id:
        log_payment_event(event, supabase_client, user_id)
    
    # Update subscription status
    supabase_client.table("user_subscriptions").update({
        "subscription_status": status,
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "cancel_at_period_end": cancel_at_period_end,
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"Subscription {subscription_id} status updated to {status}")


def handle_subscription_deleted(event_data: Dict[str, Any], supabase_client, event: Dict[str, Any]):
    """
    Handle customer.subscription.deleted event
    Downgrades user to free tier when subscription is cancelled
    """
    subscription = event_data["object"]
    subscription_id = subscription["id"]
    
    # Get user_id from subscription
    user_result = supabase_client.table("user_subscriptions").select("user_id").eq("stripe_subscription_id", subscription_id).single().execute()
    user_id = user_result.data["user_id"] if user_result.data else None
    
    # Log the event
    if user_id:
        log_payment_event(event, supabase_client, user_id)
    
    # Get free tier
    free_tier_result = supabase_client.table("plan_tiers").select("*").eq("tier_name", "free").single().execute()
    
    if not free_tier_result.data:
        print("Free tier not found")
        return
    
    free_tier = free_tier_result.data
    
    # Downgrade to free tier
    supabase_client.table("user_subscriptions").update({
        "plan_tier_id": free_tier["id"],
        "subscribed_tvl_limit": free_tier["max_tvl"],
        "subscribed_position_limit": free_tier["max_positions"],
        "subscribed_rebalance_frequency": free_tier["rebalance_frequency"],
        "stripe_subscription_id": None,
        "subscription_status": "canceled",
        "cancelled_at": datetime.now(),
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"Subscription {subscription_id} cancelled, user downgraded to free")


def handle_invoice_payment_succeeded(event_data: Dict[str, Any], supabase_client, event: Dict[str, Any]):
    """
    Handle invoice.payment_succeeded event
    Logs successful recurring payments
    """
    invoice = event_data["object"]
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    # Get user_id from subscription
    user_result = supabase_client.table("user_subscriptions").select("user_id, plan_tier_id").eq("stripe_subscription_id", subscription_id).single().execute()
    
    if not user_result.data:
        print(f"Subscription not found: {subscription_id}")
        return
    
    user_id = user_result.data["user_id"]
    plan_tier_id = user_result.data["plan_tier_id"]
    
    # Get tier name
    tier_result = supabase_client.table("plan_tiers").select("tier_name, display_name").eq("id", plan_tier_id).single().execute()
    tier_name = tier_result.data["tier_name"] if tier_result.data else "unknown"
    display_name = tier_result.data["display_name"] if tier_result.data else "Unknown Plan"
    
    # Log the event
    log_payment_event(event, supabase_client, user_id)
    
    # Add to billing history
    supabase_client.table("billing_history").insert({
        "user_id": user_id,
        "payment_date": datetime.fromtimestamp(invoice["created"]),
        "amount_cents": invoice.get("amount_paid", 0),
        "currency": invoice.get("currency", "usd"),
        "status": "paid",
        "billing_type": "subscription",
        "plan_tier_name": tier_name,
        "description": f"Monthly subscription - {display_name}",
        "stripe_invoice_id": invoice["id"],
        "stripe_payment_intent_id": invoice.get("payment_intent"),
        "invoice_url": invoice.get("hosted_invoice_url"),
        "period_start": datetime.fromtimestamp(invoice["period_start"]),
        "period_end": datetime.fromtimestamp(invoice["period_end"]),
    }).execute()
    
    print(f"Payment succeeded for subscription {subscription_id}")


def handle_invoice_payment_failed(event_data: Dict[str, Any], supabase_client, event: Dict[str, Any]):
    """
    Handle invoice.payment_failed event
    Logs failed payments and updates subscription status
    """
    invoice = event_data["object"]
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    # Get user_id from subscription
    user_result = supabase_client.table("user_subscriptions").select("user_id, plan_tier_id").eq("stripe_subscription_id", subscription_id).single().execute()
    
    if not user_result.data:
        print(f"Subscription not found: {subscription_id}")
        return
    
    user_id = user_result.data["user_id"]
    plan_tier_id = user_result.data["plan_tier_id"]
    
    # Get tier name
    tier_result = supabase_client.table("plan_tiers").select("tier_name, display_name").eq("id", plan_tier_id).single().execute()
    tier_name = tier_result.data["tier_name"] if tier_result.data else "unknown"
    display_name = tier_result.data["display_name"] if tier_result.data else "Unknown Plan"
    
    # Log the event
    log_payment_event(event, supabase_client, user_id)
    
    # Add to billing history
    supabase_client.table("billing_history").insert({
        "user_id": user_id,
        "payment_date": datetime.fromtimestamp(invoice["created"]),
        "amount_cents": invoice.get("amount_due", 0),
        "currency": invoice.get("currency", "usd"),
        "status": "failed",
        "billing_type": "subscription",
        "plan_tier_name": tier_name,
        "description": f"Failed payment - {display_name}",
        "stripe_invoice_id": invoice["id"],
        "invoice_url": invoice.get("hosted_invoice_url"),
        "period_start": datetime.fromtimestamp(invoice["period_start"]),
        "period_end": datetime.fromtimestamp(invoice["period_end"]),
    }).execute()
    
    # Update subscription status to past_due
    supabase_client.table("user_subscriptions").update({
        "subscription_status": "past_due",
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"Payment failed for subscription {subscription_id}")


def process_stripe_webhook(event: Dict[str, Any]) -> bool:
    """
    Process Stripe webhook event
    
    Args:
        event: Stripe event dict
        
    Returns:
        True if processed successfully, False otherwise
    """
    # Initialize Supabase client
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for admin operations
    
    if not supabase_url or not supabase_key:
        print("Supabase credentials not configured")
        return False
    
    supabase = create_client(supabase_url, supabase_key)
    
    event_type = event["type"]
    
    try:
        if event_type == "checkout.session.completed":
            handle_checkout_completed(event["data"], supabase, event)
        elif event_type == "customer.subscription.updated":
            handle_subscription_updated(event["data"], supabase, event)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(event["data"], supabase, event)
        elif event_type == "invoice.payment_succeeded":
            handle_invoice_payment_succeeded(event["data"], supabase, event)
        elif event_type == "invoice.payment_failed":
            handle_invoice_payment_failed(event["data"], supabase, event)
        else:
            print(f"Unhandled event type: {event_type}")
        
        return True
    except Exception as e:
        print(f"Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return False
