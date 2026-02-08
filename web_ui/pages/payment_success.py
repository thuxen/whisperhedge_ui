"""
Payment Success Page - Handles Stripe checkout redirect and subscription sync
"""
import reflex as rx
import stripe
import os
import sys
from web_ui.branding.colors import COLORS
from web_ui.branding.config import BrandConfig
from web_ui.state import AuthState


class PaymentSuccessState(rx.State):
    """State for payment success page"""
    is_processing: bool = True
    success: bool = False
    error_message: str = ""
    status_message: str = "Processing your payment..."
    session_id: str = ""
    payment_intent_id: str = ""
    invoice_number: str = ""
    order_reference: str = ""
    should_redirect: bool = False
    
    async def trigger_payment_processing(self, session_id: str):
        """Manual trigger for payment processing - bypasses on_load"""
        print("=" * 80, flush=True)
        sys.stdout.flush()
        print("[PAYMENT SUCCESS] MANUAL TRIGGER - Processing payment", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] Session ID: {session_id}", flush=True)
        sys.stdout.flush()
        
        if not session_id:
            print("[PAYMENT SUCCESS ERROR] No session_id provided to trigger!", flush=True)
            sys.stdout.flush()
            self.error_message = "No session ID provided"
            self.is_processing = False
            return
        
        self.session_id = session_id
        await self.process_payment()
    
    async def on_load(self):
        """Called when payment success page loads - FALLBACK ONLY"""
        print("=" * 80, flush=True)
        sys.stdout.flush()
        print("[PAYMENT SUCCESS] on_load handler executing (FALLBACK)", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] Environment check:", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - APP_URL: {os.getenv('APP_URL', 'NOT SET')}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - REFLEX_DOMAIN: {os.getenv('REFLEX_DOMAIN', 'NOT SET')}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] Router state:", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - Path: {self.router.page.path}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - Host: {self.router.page.host}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - Full URL: {self.router.page.raw_path}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS]   - Query params: {self.router.page.params}", flush=True)
        sys.stdout.flush()
        
        # Get session_id from query params
        session_id = self.router.page.params.get("session_id", "")
        
        if not session_id:
            print("[PAYMENT SUCCESS] on_load: No session_id - client-side script should handle this", flush=True)
            sys.stdout.flush()
            return
        
        print(f"[PAYMENT SUCCESS] on_load: Session ID found: {session_id}", flush=True)
        sys.stdout.flush()
        print(f"[PAYMENT SUCCESS] on_load: Triggering payment processing", flush=True)
        sys.stdout.flush()
        
        self.session_id = session_id
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
            
            # Get payment intent and invoice for order reference
            self.payment_intent_id = session.payment_intent if hasattr(session, 'payment_intent') else ""
            print(f"[PAYMENT SUCCESS]   - Payment Intent: {self.payment_intent_id}", flush=True)
            sys.stdout.flush()
            
            # Create order reference from payment intent (last 8 chars for readability)
            if self.payment_intent_id:
                self.order_reference = self.payment_intent_id.split('_')[-1].upper()[:8]
            else:
                self.order_reference = subscription_id.split('_')[-1].upper()[:8]
            
            print(f"[PAYMENT SUCCESS]   - Order Reference: {self.order_reference}", flush=True)
            sys.stdout.flush()
            
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
            
            # Query plan_tiers table to get the plan_tier_id based on tier_name
            plan_tier_id = None
            print(f"[PAYMENT SUCCESS] Looking up plan_tier_id for tier_name: {tier_name}", flush=True)
            sys.stdout.flush()
            
            try:
                tier_result = supabase.table("plan_tiers").select("id").eq("tier_name", tier_name).execute()
                print(f"[PAYMENT SUCCESS] Plan tier query result: {tier_result.data}", flush=True)
                sys.stdout.flush()
                
                if tier_result.data and len(tier_result.data) > 0:
                    plan_tier_id = tier_result.data[0]['id']
                    print(f"[PAYMENT SUCCESS] ✓ Found plan_tier_id: {plan_tier_id}", flush=True)
                    sys.stdout.flush()
                else:
                    print(f"[PAYMENT SUCCESS WARNING] No plan tier found for tier_name: {tier_name}", flush=True)
                    sys.stdout.flush()
            except Exception as tier_error:
                print(f"[PAYMENT SUCCESS ERROR] Failed to query plan_tiers: {tier_error}", flush=True)
                sys.stdout.flush()
                import traceback
                traceback.print_exc()
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
            
            # Add plan_tier_id if found
            if plan_tier_id:
                subscription_data["plan_tier_id"] = plan_tier_id
                print(f"[PAYMENT SUCCESS] Including plan_tier_id in upsert: {plan_tier_id}", flush=True)
                sys.stdout.flush()
            else:
                print(f"[PAYMENT SUCCESS WARNING] plan_tier_id not found, will not update tier", flush=True)
                sys.stdout.flush()
            
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
            
            # Set flag to trigger redirect in component
            self.should_redirect = True
            print("[PAYMENT SUCCESS] Redirect flag set to True", flush=True)
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
    """Payment success page with clean redirect flow"""
    return rx.box(
        # Client-side script to trigger payment processing immediately
        rx.script("""
            (function() {
                console.log('[PAYMENT SUCCESS] Page loaded - client-side script executing');
                console.log('[PAYMENT SUCCESS] Current URL:', window.location.href);
                
                // Get session_id from URL
                const urlParams = new URLSearchParams(window.location.search);
                const sessionId = urlParams.get('session_id');
                
                console.log('[PAYMENT SUCCESS] Session ID from URL:', sessionId);
                
                if (sessionId) {
                    console.log('[PAYMENT SUCCESS] Calling trigger_payment_processing with session_id');
                    
                    // Wait for Reflex to be ready, then trigger the event
                    setTimeout(() => {
                        try {
                            // Call the Reflex event handler directly
                            if (window.__reflex && window.__reflex.Event) {
                                console.log('[PAYMENT SUCCESS] Reflex available, triggering event');
                                window.__reflex.Event('payment_success_state.trigger_payment_processing', {session_id: sessionId});
                            } else {
                                console.error('[PAYMENT SUCCESS] Reflex not available yet, retrying...');
                                // Retry after another delay
                                setTimeout(() => {
                                    if (window.__reflex && window.__reflex.Event) {
                                        window.__reflex.Event('payment_success_state.trigger_payment_processing', {session_id: sessionId});
                                    } else {
                                        console.error('[PAYMENT SUCCESS] Reflex still not available!');
                                    }
                                }, 1000);
                            }
                        } catch (e) {
                            console.error('[PAYMENT SUCCESS] Error triggering event:', e);
                        }
                    }, 500);
                } else {
                    console.error('[PAYMENT SUCCESS] No session_id found in URL!');
                }
            })();
        """),
        # Auto-redirect script when success flag is set
        rx.cond(
            PaymentSuccessState.success,
            rx.script("""
                setTimeout(() => {
                    console.log('[PAYMENT SUCCESS] Redirecting to dashboard...');
                    window.location.href = '/dashboard?payment_success=true';
                }, 2000);
            """),
        ),
        rx.center(
            rx.vstack(
                # Processing state
                rx.cond(
                    PaymentSuccessState.is_processing,
                    rx.vstack(
                        rx.heading("Processing Payment", size="7", color=COLORS.TEXT_PRIMARY),
                        rx.spinner(size="3", color=COLORS.ACCENT_PRIMARY, margin_top="1rem"),
                        rx.text(PaymentSuccessState.status_message, color=COLORS.TEXT_SECONDARY, margin_top="1rem"),
                        spacing="4",
                        align="center",
                    ),
                ),
                # Success state
                rx.cond(
                    PaymentSuccessState.success,
                    rx.vstack(
                        rx.heading("✓ Payment Successful!", size="7", color=COLORS.ACCENT_SUCCESS),
                        rx.text(
                            PaymentSuccessState.status_message,
                            size="4",
                            color=COLORS.TEXT_PRIMARY,
                            margin_top="1rem",
                        ),
                        rx.text(
                            "Redirecting to dashboard in 2 seconds...",
                            color=COLORS.TEXT_SECONDARY,
                            margin_top="1rem",
                        ),
                        rx.link(
                            "Click here if not redirected",
                            href="/dashboard?payment_success=true",
                            color=COLORS.ACCENT_PRIMARY,
                            margin_top="0.5rem",
                        ),
                        spacing="4",
                        align="center",
                    ),
                ),
                # Error state
                rx.cond(
                    PaymentSuccessState.error_message != "",
                    rx.vstack(
                        rx.heading("Payment Error", size="7", color=COLORS.ACCENT_ERROR),
                        rx.text(
                            PaymentSuccessState.error_message,
                            color=COLORS.ACCENT_ERROR,
                            margin_top="1rem",
                        ),
                        rx.link(
                            rx.button("Return to Dashboard", size="3", margin_top="2rem"),
                            href="/dashboard",
                        ),
                        spacing="4",
                        align="center",
                    ),
                ),
                spacing="6",
                align="center",
                padding="2rem",
            ),
            min_height="100vh",
        ),
        width="100%",
        background=COLORS.BG_PRIMARY,
    )
