"""
Simplified Stripe webhook handler
Only syncs subscription status to local database
Billing history is handled by Stripe Customer Portal
"""
from typing import Dict, Any
from supabase import create_client
import os
from datetime import datetime


def handle_checkout_completed(event_data: Dict[str, Any], supabase_client):
    """
    Handle checkout.session.completed event
    Updates user subscription when they complete payment
    """
    session = event_data["object"]
    
    user_id = session["metadata"]["user_id"]
    tier_name = session["metadata"]["tier_name"]
    customer_id = session["customer"]
    subscription_id = session["subscription"]
    
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
    
    print(f"✅ User {user_id} upgraded to {tier_name}")


def handle_subscription_updated(event_data: Dict[str, Any], supabase_client):
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
    
    # Update subscription status
    supabase_client.table("user_subscriptions").update({
        "subscription_status": status,
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "cancel_at_period_end": cancel_at_period_end,
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"✅ Subscription {subscription_id} status updated to {status}")


def handle_subscription_deleted(event_data: Dict[str, Any], supabase_client):
    """
    Handle customer.subscription.deleted event
    Downgrades user to free tier when subscription is cancelled
    """
    subscription = event_data["object"]
    subscription_id = subscription["id"]
    
    # Get free tier
    free_tier_result = supabase_client.table("plan_tiers").select("*").eq("tier_name", "free").single().execute()
    
    if not free_tier_result.data:
        print("❌ Free tier not found")
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
    
    print(f"✅ Subscription {subscription_id} cancelled, user downgraded to free")


def handle_invoice_payment_failed(event_data: Dict[str, Any], supabase_client):
    """
    Handle invoice.payment_failed event
    Marks subscription as past_due but keeps access (graceful degradation)
    """
    invoice = event_data["object"]
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    # Update subscription status to past_due (but don't cut off access)
    supabase_client.table("user_subscriptions").update({
        "subscription_status": "past_due",
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"⚠️  Payment failed for subscription {subscription_id} - marked as past_due")


def handle_invoice_payment_succeeded(event_data: Dict[str, Any], supabase_client):
    """
    Handle invoice.payment_succeeded event
    Updates subscription status back to active after successful payment
    """
    invoice = event_data["object"]
    subscription_id = invoice.get("subscription")
    
    if not subscription_id:
        return
    
    # Update subscription status back to active
    supabase_client.table("user_subscriptions").update({
        "subscription_status": "active",
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"✅ Payment succeeded for subscription {subscription_id}")


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
        print("❌ Supabase credentials not configured")
        return False
    
    supabase = create_client(supabase_url, supabase_key)
    
    event_type = event["type"]
    
    try:
        if event_type == "checkout.session.completed":
            handle_checkout_completed(event["data"], supabase)
        elif event_type == "customer.subscription.updated":
            handle_subscription_updated(event["data"], supabase)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(event["data"], supabase)
        elif event_type == "invoice.payment_succeeded":
            handle_invoice_payment_succeeded(event["data"], supabase)
        elif event_type == "invoice.payment_failed":
            handle_invoice_payment_failed(event["data"], supabase)
        else:
            print(f"ℹ️  Unhandled event type: {event_type}")
        
        return True
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        import traceback
        traceback.print_exc()
        return False
