"""
Payment Success Page - Handles Stripe checkout redirect and subscription sync
"""
import reflex as rx
import sys
from ..state import AuthState


class PaymentSuccessState(rx.State):
    """State for payment success page"""
    is_processing: bool = True
    success: bool = False
    error_message: str = ""
    status_message: str = "Processing your payment..."
    session_id: str = ""
    
    async def on_load(self):
        """Called when payment success page loads"""
        print("=" * 80, flush=True)
        sys.stdout.flush()
        print("[PAYMENT SUCCESS] Page loaded", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] Current URL: {self.router.page.path}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] Query params: {self.router.page.params}", flush=True)
        sys.stdout.flush()
        
        # Get session_id from query params
        session_id = self.router.page.params.get("session_id", "")
        
        if not session_id:
            print("[PAYMENT SUCCESS ERROR] No session_id in query params!", flush=True)
            sys.stdout.flush()
            self.error_message = "No session ID provided"
            self.is_processing = False
            return
        
        print(f"[PAYMENT SUCCESS] Session ID: {session_id}", flush=True)
        sys.stdout.flush()
        self.session_id = session_id
        
        # Process the payment
        await self.process_payment()
    
    async def process_payment(self):
        """Process the Stripe payment and update subscription"""
        try:
            print("[PAYMENT SUCCESS] Starting payment processing...", flush=True)
            sys.stdout.flush()
            
            # Get user info
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            user_email = auth_state.user_email
            
            print(f"[PAYMENT SUCCESS] User ID: {user_id}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] User Email: {user_email}", flush=True)
            sys.stdout.flush()
            
            if not user_id:
                print("[PAYMENT SUCCESS ERROR] No user_id found in auth state!", flush=True)
                sys.stdout.flush()
                self.error_message = "User not authenticated"
                self.is_processing = False
                return
            
            # Retrieve Stripe session
            print(f"[PAYMENT SUCCESS] Retrieving Stripe session: {self.session_id}", flush=True)
            sys.stdout.flush()
            
            import stripe
            import os
            
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            print(f"[PAYMENT SUCCESS] Stripe API key configured: {bool(stripe.api_key)}", flush=True)
            sys.stdout.flush()
            
            session = stripe.checkout.Session.retrieve(self.session_id)
            print(f"[PAYMENT SUCCESS] ✓ Session retrieved", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - Payment status: {session.payment_status}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - Customer: {session.customer}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - Subscription: {session.subscription}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - Metadata: {session.metadata}", flush=True)
            sys.stdout.flush()
            
            if session.payment_status != "paid":
                print(f"[PAYMENT SUCCESS ERROR] Payment not completed: {session.payment_status}", flush=True)
                sys.stdout.flush()
                self.error_message = f"Payment status: {session.payment_status}"
                self.is_processing = False
                return
            
            # Get subscription details
            subscription_id = session.subscription
            customer_id = session.customer
            tier_name = session.metadata.get("tier_name", "unknown")
            
            print(f"[PAYMENT SUCCESS] Retrieving subscription: {subscription_id}", flush=True)
            sys.stdout.flush()
            
            subscription = stripe.Subscription.retrieve(subscription_id)
            print(f"[PAYMENT SUCCESS] ✓ Subscription retrieved", flush=True)
            sys.stdout.flush()
            
            print(f"[PAYMENT SUCCESS] DUMPING ENTIRE SUBSCRIPTION OBJECT:", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] {subscription}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] SUBSCRIPTION DICT: {dict(subscription)}", flush=True)
            sys.stdout.flush()
            
            print(f"[PAYMENT SUCCESS] Extracting subscription fields...", flush=True)
            sys.stdout.flush()
            
            try:
                sub_status = subscription.status
                print(f"[PAYMENT SUCCESS]   - status: {sub_status}", flush=True)
                sys.stdout.flush()
            except Exception as e:
                print(f"[PAYMENT SUCCESS ERROR] Failed to get status: {e}", flush=True)
                sys.stdout.flush()
                sub_status = "unknown"
            
            try:
                # CRITICAL: Must use subscription['items'] not subscription.items
                # because .items conflicts with Python dict.items() method
                # See: https://github.com/stripe/stripe-python/issues/297
                first_item = subscription['items']['data'][0]
                sub_period_start = first_item['current_period_start']
                print(f"[PAYMENT SUCCESS]   - current_period_start: {sub_period_start}", flush=True)
                sys.stdout.flush()
            except Exception as e:
                print(f"[PAYMENT SUCCESS ERROR] Failed to get current_period_start: {e}", flush=True)
                sys.stdout.flush()
                import traceback
                traceback.print_exc()
                sys.stdout.flush()
                sub_period_start = None
            
            try:
                first_item = subscription['items']['data'][0]
                sub_period_end = first_item['current_period_end']
                print(f"[PAYMENT SUCCESS]   - current_period_end: {sub_period_end}", flush=True)
                sys.stdout.flush()
            except Exception as e:
                print(f"[PAYMENT SUCCESS ERROR] Failed to get current_period_end: {e}", flush=True)
                sys.stdout.flush()
                import traceback
                traceback.print_exc()
                sys.stdout.flush()
                sub_period_end = None
            
            # Update Supabase
            print("[PAYMENT SUCCESS] Updating Supabase...", flush=True)
            sys.stdout.flush()
            
            from supabase import create_client
            
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # Use service role JWT key to bypass RLS
            print(f"[PAYMENT SUCCESS] SUPABASE_URL: {supabase_url}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] SUPABASE_SERVICE_ROLE_KEY exists: {bool(supabase_key)}", flush=True)
            sys.stdout.flush()
            
            supabase = create_client(supabase_url, supabase_key)
            
            print(f"[PAYMENT SUCCESS] Supabase client created", flush=True)
            sys.stdout.flush()
            
            # Convert Unix timestamps to ISO datetime for Postgres
            from datetime import datetime, timezone
            
            period_start_dt = None
            period_end_dt = None
            
            if sub_period_start:
                period_start_dt = datetime.fromtimestamp(sub_period_start, tz=timezone.utc).isoformat()
                print(f"[PAYMENT SUCCESS] Converted period_start: {sub_period_start} -> {period_start_dt}", flush=True)
                sys.stdout.flush()
            
            if sub_period_end:
                period_end_dt = datetime.fromtimestamp(sub_period_end, tz=timezone.utc).isoformat()
                print(f"[PAYMENT SUCCESS] Converted period_end: {sub_period_end} -> {period_end_dt}", flush=True)
                sys.stdout.flush()
            
            # Prepare subscription data (match actual table schema)
            subscription_data = {
                "user_id": user_id,
                "stripe_customer_id": customer_id,
                "stripe_subscription_id": subscription_id,
                "subscription_status": sub_status,  # Column name is 'subscription_status' not 'status'
                "current_period_start": period_start_dt,
                "current_period_end": period_end_dt,
            }
            # Note: tier_name removed - not in user_subscriptions table
            
            print(f"[PAYMENT SUCCESS] FULL SUBSCRIPTION DATA DICT:", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] {subscription_data}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - user_id: {subscription_data['user_id']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - stripe_customer_id: {subscription_data['stripe_customer_id']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - stripe_subscription_id: {subscription_data['stripe_subscription_id']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - subscription_status: {subscription_data['subscription_status']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - current_period_start: {subscription_data['current_period_start']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - current_period_end: {subscription_data['current_period_end']}", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS]   - tier_name from metadata: {tier_name} (not stored in DB)", flush=True)
            sys.stdout.flush()
            
            # Upsert to database
            print(f"[PAYMENT SUCCESS] EXECUTING SUPABASE UPSERT...", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] Table: user_subscriptions", flush=True)
            sys.stdout.flush()
            print(f"[PAYMENT SUCCESS] Operation: upsert", flush=True)
            sys.stdout.flush()
            
            try:
                # Upsert with on_conflict to update existing user row
                result = supabase.table("user_subscriptions").upsert(subscription_data, on_conflict="user_id").execute()
                print(f"[PAYMENT SUCCESS] ✓ Database upsert executed", flush=True)
                sys.stdout.flush()
                print(f"[PAYMENT SUCCESS] Result object: {result}", flush=True)
                sys.stdout.flush()
                print(f"[PAYMENT SUCCESS] Result.data: {result.data}", flush=True)
                sys.stdout.flush()
                print(f"[PAYMENT SUCCESS] Result.count: {getattr(result, 'count', 'N/A')}", flush=True)
                sys.stdout.flush()
            except Exception as db_error:
                print(f"[PAYMENT SUCCESS ERROR] DATABASE UPSERT FAILED: {db_error}", flush=True)
                sys.stdout.flush()
                import traceback
                traceback.print_exc()
                sys.stdout.flush()
                raise
            
            # Success!
            self.success = True
            self.is_processing = False
            self.status_message = f"Payment successful! Your {tier_name.title()} plan is now active."
            
            print("[PAYMENT SUCCESS] ✓✓✓ PAYMENT PROCESSING COMPLETE ✓✓✓", flush=True)
            sys.stdout.flush()
            print("=" * 80, flush=True)
            sys.stdout.flush()
            
        except Exception as e:
            print(f"[PAYMENT SUCCESS ERROR] Exception occurred: {e}", flush=True)
            sys.stdout.flush()
            import traceback
            traceback.print_exc()
            sys.stdout.flush()
            
            self.error_message = f"Error processing payment: {str(e)}"
            self.is_processing = False
            self.success = False


def payment_success_page() -> rx.Component:
    """Payment success page - minimal UI with maximum logging"""
    return rx.vstack(
        rx.heading("Payment Processing"),
        
        rx.cond(
            PaymentSuccessState.is_processing,
            rx.vstack(
                rx.spinner(),
                rx.text(PaymentSuccessState.status_message),
            ),
        ),
        
        rx.cond(
            PaymentSuccessState.success,
            rx.vstack(
                rx.text("✓ SUCCESS"),
                rx.text(PaymentSuccessState.status_message),
                rx.text("Redirecting to dashboard..."),
                rx.script(
                    """
                    setTimeout(function() {
                        window.location.href = '/dashboard';
                    }, 5000);
                    """
                ),
            ),
        ),
        
        rx.cond(
            PaymentSuccessState.error_message != "",
            rx.vstack(
                rx.text("⚠ ERROR"),
                rx.text("Payment Processing Error"),
                rx.text(PaymentSuccessState.error_message),
                rx.button(
                    "Go to Dashboard",
                    on_click=rx.redirect("/dashboard"),
                ),
            ),
        ),
        
        rx.text(f"Session ID: {PaymentSuccessState.session_id}"),
    )
