"""
API endpoint for processing Stripe payments without authentication
This endpoint is called by the static payment-success.html page
"""
import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import stripe
from supabase import create_client

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class ProcessPaymentRequest(BaseModel):
    session_id: str


@router.post("/process-payment")
async def process_payment(request: ProcessPaymentRequest):
    """Process Stripe payment and update user subscription - NO AUTH REQUIRED"""
    try:
        print("=" * 80, flush=True)
        sys.stdout.flush()
        print(f"[API PAYMENT] Processing payment for session: {request.session_id}", flush=True)
        sys.stdout.flush()
        
        # Retrieve Stripe session
        session = stripe.checkout.Session.retrieve(request.session_id)
        
        print(f"[API PAYMENT] Session retrieved", flush=True)
        sys.stdout.flush()
        print(f"[API PAYMENT]   - Payment status: {session.payment_status}", flush=True)
        sys.stdout.flush()
        print(f"[API PAYMENT]   - Customer: {session.customer}", flush=True)
        sys.stdout.flush()
        print(f"[API PAYMENT]   - Subscription: {session.subscription}", flush=True)
        sys.stdout.flush()
        
        if session.payment_status != "paid":
            print(f"[API PAYMENT ERROR] Payment not completed: {session.payment_status}", flush=True)
            sys.stdout.flush()
            return {"success": False, "error": f"Payment status: {session.payment_status}"}
        
        # Get user_id from metadata
        user_id = session.metadata.get("user_id")
        tier_name = session.metadata.get("tier_name")
        
        if not user_id or not tier_name:
            print(f"[API PAYMENT ERROR] Missing metadata: user_id={user_id}, tier_name={tier_name}", flush=True)
            sys.stdout.flush()
            return {"success": False, "error": "Missing user information in payment session"}
        
        print(f"[API PAYMENT] User ID: {user_id}", flush=True)
        sys.stdout.flush()
        print(f"[API PAYMENT] Tier: {tier_name}", flush=True)
        sys.stdout.flush()
        
        # Update database
        supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        
        # Get tier details
        tier_result = supabase.table("plan_tiers").select("*").eq("tier_name", tier_name).execute()
        
        if not tier_result.data:
            print(f"[API PAYMENT ERROR] Tier not found: {tier_name}", flush=True)
            sys.stdout.flush()
            return {"success": False, "error": f"Invalid tier: {tier_name}"}
        
        tier = tier_result.data[0]
        
        # Update or insert subscription
        subscription_data = {
            "user_id": user_id,
            "tier_id": tier["id"],
            "stripe_customer_id": session.customer,
            "stripe_subscription_id": session.subscription,
            "subscription_status": "active",
            "current_period_start": None,  # Will be set by Stripe webhook
            "current_period_end": None,
        }
        
        # Check if subscription exists
        existing = supabase.table("user_subscriptions").select("*").eq("user_id", user_id).execute()
        
        if existing.data:
            # Update existing
            print(f"[API PAYMENT] Updating existing subscription", flush=True)
            sys.stdout.flush()
            result = supabase.table("user_subscriptions").update(subscription_data).eq("user_id", user_id).execute()
        else:
            # Insert new
            print(f"[API PAYMENT] Creating new subscription", flush=True)
            sys.stdout.flush()
            result = supabase.table("user_subscriptions").insert(subscription_data).execute()
        
        print(f"[API PAYMENT] ✓ Subscription updated successfully", flush=True)
        sys.stdout.flush()
        
        return {
            "success": True,
            "tier": tier_name,
            "message": "Payment processed successfully"
        }
        
    except stripe.error.StripeError as e:
        print(f"[API PAYMENT ERROR] Stripe error: {e}", flush=True)
        sys.stdout.flush()
        return {"success": False, "error": f"Stripe error: {str(e)}"}
    
    except Exception as e:
        print(f"[API PAYMENT ERROR] Unexpected error: {e}", flush=True)
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        return {"success": False, "error": f"Server error: {str(e)}"}
