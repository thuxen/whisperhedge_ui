import reflex as rx
import sys
from .auth import get_supabase_client


class AuthState(rx.State):
    is_authenticated: bool = False
    user_email: str = ""
    user_id: str = ""
    access_token: str = ""  # Store session token for RLS
    error_message: str = ""
    success_message: str = ""
    is_loading: bool = False

    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    async def sign_up(self, form_data: dict):
        import sys
        
        print("=" * 80, flush=True)
        sys.stdout.flush()
        print("[SIGNUP] Sign up attempt started", flush=True)
        sys.stdout.flush()
        
        self.is_loading = True
        self.clear_messages()
        
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        
        print(f"[SIGNUP] Email: {email}", flush=True)
        sys.stdout.flush()
        print(f"[SIGNUP] Password length: {len(password) if password else 0}", flush=True)
        sys.stdout.flush()
        print(f"[SIGNUP] Confirm password length: {len(confirm_password) if confirm_password else 0}", flush=True)
        sys.stdout.flush()
        
        if not email or not password:
            print("[SIGNUP ERROR] Email or password missing", flush=True)
            sys.stdout.flush()
            self.error_message = "Email and password are required"
            self.is_loading = False
            return
        
        if password != confirm_password:
            print("[SIGNUP ERROR] Passwords do not match", flush=True)
            sys.stdout.flush()
            self.error_message = "Passwords do not match"
            self.is_loading = False
            return
        
        if len(password) < 6:
            print("[SIGNUP ERROR] Password too short", flush=True)
            sys.stdout.flush()
            self.error_message = "Password must be at least 6 characters"
            self.is_loading = False
            return
        
        try:
            print("[SIGNUP] Validation passed, calling Supabase...", flush=True)
            sys.stdout.flush()
            
            supabase = get_supabase_client()
            print("[SIGNUP] Supabase client obtained", flush=True)
            sys.stdout.flush()
            
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            print(f"[SIGNUP] Supabase response received", flush=True)
            sys.stdout.flush()
            print(f"[SIGNUP]   - User: {response.user is not None}", flush=True)
            sys.stdout.flush()
            print(f"[SIGNUP]   - Session: {response.session is not None}", flush=True)
            sys.stdout.flush()
            
            if response.user:
                print(f"[SIGNUP] User created: {response.user.id}", flush=True)
                sys.stdout.flush()
                
                if response.session:
                    print("[SIGNUP] Session created, user auto-confirmed", flush=True)
                    sys.stdout.flush()
                    self.is_authenticated = True
                    self.user_email = email
                    self.user_id = response.user.id
                    self.access_token = response.session.access_token
                    self.success_message = "Account created successfully! Redirecting to dashboard..."
                    print("[SIGNUP] ✓ Signup successful, redirecting to dashboard", flush=True)
                    sys.stdout.flush()
                    print("=" * 80, flush=True)
                    sys.stdout.flush()
                    return rx.redirect("/dashboard")
                else:
                    print("[SIGNUP] No session, email confirmation required", flush=True)
                    sys.stdout.flush()
                    self.success_message = "Account created! Please check your email to verify your account before signing in."
                    self.user_email = email
                    print("[SIGNUP] ✓ Signup successful, awaiting email confirmation", flush=True)
                    sys.stdout.flush()
                    print("=" * 80, flush=True)
                    sys.stdout.flush()
            else:
                print("[SIGNUP ERROR] No user in response", flush=True)
                sys.stdout.flush()
                self.error_message = "Failed to create account"
                print("=" * 80, flush=True)
                sys.stdout.flush()
        except Exception as e:
            print(f"[SIGNUP ERROR] Exception occurred: {e}", flush=True)
            sys.stdout.flush()
            import traceback
            traceback.print_exc()
            sys.stdout.flush()
            self.error_message = "An error occurred during sign up. Please try again."
            print("=" * 80, flush=True)
            sys.stdout.flush()
        finally:
            self.is_loading = False

    async def sign_in(self, form_data: dict):
        self.is_loading = True
        self.clear_messages()
        
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        
        if not email or not password:
            self.error_message = "Email and password are required"
            self.is_loading = False
            return
        
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                self.is_authenticated = True
                self.user_email = email
                self.user_id = response.user.id
                self.access_token = response.session.access_token
                self.success_message = "Successfully logged in!"
                
                # Sync subscription status from Stripe on login
                await self._sync_subscription_status()
                
                return rx.redirect("/dashboard")
            else:
                self.error_message = "Invalid credentials"
        except Exception as e:
            self.error_message = "An error occurred during sign in. Please try again."
        finally:
            self.is_loading = False
    
    async def _sync_subscription_status(self):
        """Sync subscription status from Stripe to local database on login"""
        try:
            from .services.stripe_service import get_subscription_details
            from datetime import datetime
            
            print(f"[AUTH] Syncing subscription status for user {self.user_id}", flush=True)
            sys.stdout.flush()
            
            supabase = get_supabase_client(self.access_token)
            
            # Get user's subscription from database
            result = supabase.table("user_subscriptions").select("stripe_subscription_id").eq("user_id", self.user_id).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"[AUTH] No subscription record found", flush=True)
                sys.stdout.flush()
                return
            
            subscription_id = result.data[0].get("stripe_subscription_id")
            
            if not subscription_id:
                print(f"[AUTH] No Stripe subscription ID", flush=True)
                sys.stdout.flush()
                return
            
            # Fetch current status from Stripe
            stripe_details = get_subscription_details(subscription_id)
            
            if not stripe_details:
                print(f"[AUTH] Failed to fetch Stripe subscription details", flush=True)
                sys.stdout.flush()
                return
            
            # Update local database with Stripe status
            update_data = {
                "subscription_status": stripe_details["status"],
                "current_period_start": datetime.fromtimestamp(stripe_details["current_period_start"]).isoformat(),
                "current_period_end": datetime.fromtimestamp(stripe_details["current_period_end"]).isoformat(),
                "cancel_at_period_end": stripe_details["cancel_at_period_end"],
            }
            
            # If subscription is cancelled or expired, downgrade to free tier
            if stripe_details["status"] in ["canceled", "unpaid", "incomplete_expired"]:
                free_tier = supabase.table("plan_tiers").select("*").eq("tier_name", "free").execute()
                if free_tier.data and len(free_tier.data) > 0:
                    tier = free_tier.data[0]
                    update_data["plan_tier_id"] = tier["id"]
                    update_data["subscribed_tvl_limit"] = tier["max_tvl"]
                    update_data["subscribed_position_limit"] = tier["max_positions"]
                    update_data["stripe_subscription_id"] = None
                    print(f"[AUTH] ✓ Downgraded to free tier (status: {stripe_details['status']})", flush=True)
                    sys.stdout.flush()
            
            supabase.table("user_subscriptions").update(update_data).eq("user_id", self.user_id).execute()
            
            print(f"[AUTH] ✓ Subscription status synced: {stripe_details['status']}", flush=True)
            sys.stdout.flush()
            
        except Exception as e:
            print(f"[AUTH] Error syncing subscription status: {e}", flush=True)
            sys.stdout.flush()
            import traceback
            traceback.print_exc()
            sys.stdout.flush()

    def sign_out(self):
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            self.is_authenticated = False
            self.user_email = ""
            self.user_id = ""
            self.access_token = ""
            self.success_message = "Successfully logged out"
            # Force full page reload to clear all state and prevent cross-user contamination
            return rx.redirect("/", external=True)
        except Exception as e:
            self.error_message = "An error occurred during sign out. Please try again."
