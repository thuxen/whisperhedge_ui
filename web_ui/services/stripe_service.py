"""
Stripe integration service for subscription management
"""
import os
import stripe
from typing import Optional, Dict, Any


# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Stripe Price IDs - Set these in your environment variables after creating products in Stripe
STRIPE_PRICE_IDS = {
    "hobby": os.getenv("STRIPE_PRICE_HOBBY", ""),  # $19.99/mo
    "pro": os.getenv("STRIPE_PRICE_PRO", ""),      # $49.99/mo
    "elite": os.getenv("STRIPE_PRICE_ELITE", ""),  # $149.99/mo
}


def create_checkout_session(
    user_id: str,
    user_email: str,
    tier_name: str,
    success_url: str,
    cancel_url: str,
) -> Optional[str]:
    """
    Create a Stripe Checkout session for plan subscription
    
    Args:
        user_id: User's UUID from Supabase
        user_email: User's email
        tier_name: Plan tier name (hobby, pro, elite)
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if user cancels
        
    Returns:
        Checkout session URL or None if error
    """
    try:
        print(f"[STRIPE] Creating checkout session for user {user_id}")
        print(f"[STRIPE]   - Email: {user_email}")
        print(f"[STRIPE]   - Tier: {tier_name}")
        print(f"[STRIPE]   - Success URL: {success_url}")
        print(f"[STRIPE]   - Cancel URL: {cancel_url}")
        
        price_id = STRIPE_PRICE_IDS.get(tier_name)
        if not price_id:
            print(f"[STRIPE ERROR] Invalid tier name: {tier_name}")
            raise ValueError(f"Invalid tier name: {tier_name}")
        
        print(f"[STRIPE]   - Price ID: {price_id}")
        
        session = stripe.checkout.Session.create(
            customer_email=user_email,
            mode="subscription",
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            metadata={
                "user_id": user_id,
                "tier_name": tier_name,
            },
            success_url=success_url,
            cancel_url=cancel_url,
            allow_promotion_codes=True,
            billing_address_collection="auto",
        )
        
        print(f"[STRIPE] ✓ Checkout session created: {session.id}")
        print(f"[STRIPE]   - Session URL: {session.url}")
        print(f"[STRIPE]   - Customer: {session.customer}")
        
        return session.url
    except Exception as e:
        print(f"[STRIPE ERROR] Failed to create checkout session: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_customer_portal_session(
    customer_id: str,
    return_url: str,
) -> Optional[str]:
    """
    Create a Stripe Customer Portal session for subscription management
    
    Args:
        customer_id: Stripe customer ID
        return_url: URL to redirect back to after portal session
        
    Returns:
        Portal session URL or None if error
    """
    try:
        print(f"[STRIPE] Creating customer portal session")
        print(f"[STRIPE]   - Customer ID: {customer_id}")
        print(f"[STRIPE]   - Return URL: {return_url}")
        
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        
        print(f"[STRIPE] ✓ Portal session created: {session.id}")
        print(f"[STRIPE]   - Portal URL: {session.url}")
        
        return session.url
    except Exception as e:
        print(f"[STRIPE ERROR] Failed to create portal session: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_subscription_details(subscription_id: str) -> Optional[Dict[str, Any]]:
    """
    Get subscription details from Stripe
    
    Args:
        subscription_id: Stripe subscription ID
        
    Returns:
        Subscription details dict or None if error
    """
    try:
        print(f"[STRIPE] Retrieving subscription details: {subscription_id}")
        
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        details = {
            "id": subscription.id,
            "customer": subscription.customer,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
            "cancel_at_period_end": subscription.cancel_at_period_end,
        }
        
        print(f"[STRIPE] ✓ Subscription retrieved")
        print(f"[STRIPE]   - Status: {details['status']}")
        print(f"[STRIPE]   - Customer: {details['customer']}")
        
        return details
    except Exception as e:
        print(f"[STRIPE ERROR] Failed to retrieve subscription: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_webhook_signature(payload: bytes, sig_header: str) -> Optional[Dict[str, Any]]:
    """
    Verify Stripe webhook signature and return event
    
    Args:
        payload: Raw request body
        sig_header: Stripe-Signature header
        
    Returns:
        Stripe event dict or None if verification fails
    """
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not webhook_secret:
        print("STRIPE_WEBHOOK_SECRET not set")
        return None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        return event
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return None
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return None
