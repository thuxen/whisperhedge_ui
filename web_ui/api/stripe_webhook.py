"""
Stripe webhook handler for subscription events
This needs to be set up as an API endpoint that Stripe can POST to
"""
from typing import Dict, Any
from supabase import create_client
import os


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
        "status": "active",
    }).eq("user_id", user_id).execute()
    
    print(f"User {user_id} upgraded to {tier_name}")


def handle_subscription_updated(event_data: Dict[str, Any], supabase_client):
    """
    Handle customer.subscription.updated event
    Updates subscription status when changed in Stripe
    """
    subscription = event_data["object"]
    subscription_id = subscription["id"]
    status = subscription["status"]
    
    # Update subscription status
    supabase_client.table("user_subscriptions").update({
        "status": status,
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"Subscription {subscription_id} status updated to {status}")


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
        "status": "cancelled",
    }).eq("stripe_subscription_id", subscription_id).execute()
    
    print(f"Subscription {subscription_id} cancelled, user downgraded to free")


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
            handle_checkout_completed(event["data"], supabase)
        elif event_type == "customer.subscription.updated":
            handle_subscription_updated(event["data"], supabase)
        elif event_type == "customer.subscription.deleted":
            handle_subscription_deleted(event["data"], supabase)
        else:
            print(f"Unhandled event type: {event_type}")
        
        return True
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return False
