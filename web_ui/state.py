import reflex as rx
import sys
import os
from .auth import get_supabase_client


class AuthState(rx.State):
    is_authenticated: bool = False
    user_email: str = ""
    user_id: str = ""
    access_token: str = ""  # Store session token for RLS
    error_message: str = ""
    success_message: str = ""
    is_loading: bool = False
    
    # Temporary storage for magic link tokens
    _temp_access_token: str = ""
    _temp_refresh_token: str = ""

    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    async def sign_up(self, form_data: dict):
        """Send magic link for signup (passwordless)"""
        self.is_loading = True
        self.clear_messages()
        
        email = form_data.get("email", "").strip()
        
        print(f"[SIGNUP] Magic link signup for: {email}", flush=True)
        
        if not email:
            self.error_message = "Email is required"
            self.is_loading = False
            return
        
        try:
            supabase = get_supabase_client()
            
            supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "email_redirect_to": f"{os.getenv('SITE_URL', 'http://localhost:3000')}/auth/callback"
                }
            })
            
            self.success_message = "Check your email! We've sent you a magic link to sign up."
            print(f"[SIGNUP] Magic link sent to {email}", flush=True)
            
        except Exception as e:
            print(f"[SIGNUP ERROR] {e}", flush=True)
            self.success_message = "Check your email! We've sent you a magic link to sign up."
        finally:
            self.is_loading = False

    async def sign_in(self, form_data: dict):
        """Send magic link for login (passwordless)"""
        self.is_loading = True
        self.clear_messages()
        
        email = form_data.get("email", "").strip()
        
        print(f"[LOGIN] Magic link login for: {email}", flush=True)
        
        if not email:
            self.error_message = "Email is required"
            self.is_loading = False
            return
        
        try:
            supabase = get_supabase_client()
            
            supabase.auth.sign_in_with_otp({
                "email": email,
                "options": {
                    "email_redirect_to": f"{os.getenv('SITE_URL', 'http://localhost:3000')}/auth/callback"
                }
            })
            
            self.success_message = "Check your email! We've sent you a magic link to sign in."
            print(f"[LOGIN] Magic link sent to {email}", flush=True)
            
        except Exception as e:
            print(f"[LOGIN ERROR] {e}", flush=True)
            self.success_message = "Check your email! We've sent you a magic link to sign in."
        finally:
            self.is_loading = False
    
    async def reset_password(self, form_data: dict):
        """Send magic link (same as sign_in for passwordless)"""
        return await self.sign_in(form_data)
    
    async def handle_magic_link_callback(self):
        """Handle magic link authentication callback using PKCE flow"""
        print("[MAGIC LINK] Callback handler started", flush=True)
        
        try:
            # Get token_hash from query parameters (PKCE flow)
            token_hash = self.router.page.params.get("token_hash", "")
            auth_type = self.router.page.params.get("type", "")
            
            print(f"[MAGIC LINK] Token hash from URL: {bool(token_hash)}", flush=True)
            print(f"[MAGIC LINK] Type: {auth_type}", flush=True)
            
            if not token_hash:
                print("[MAGIC LINK] No token_hash in URL parameters", flush=True)
                self.error_message = "Invalid magic link. Please try again."
                return rx.redirect("/login")
            
            supabase = get_supabase_client()
            
            # Verify OTP using token_hash (PKCE flow)
            print("[MAGIC LINK] Verifying OTP with token_hash", flush=True)
            response = supabase.auth.verify_otp({
                "token_hash": token_hash,
                "type": auth_type if auth_type else "magiclink"
            })
            
            if response and response.user:
                print(f"[MAGIC LINK] User authenticated: {response.user.email}", flush=True)
                
                self.is_authenticated = True
                self.user_email = response.user.email
                self.user_id = response.user.id
                self.access_token = response.session.access_token
                
                # Sync subscription status
                await self._sync_subscription_status()
                
                print("[MAGIC LINK] Redirecting to dashboard", flush=True)
                return rx.redirect("/dashboard")
            else:
                print("[MAGIC LINK] Failed to verify OTP", flush=True)
                self.error_message = "Authentication failed. Please try again."
                return rx.redirect("/login")
                
        except Exception as e:
            print(f"[MAGIC LINK ERROR] {e}", flush=True)
            import traceback
            traceback.print_exc()
            self.error_message = "Authentication failed. Please try again."
            return rx.redirect("/login")
    
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
                "cancel_at_period_end": stripe_details["cancel_at_period_end"],
            }
            
            # Add billing dates if available
            if stripe_details.get("current_period_start"):
                update_data["current_period_start"] = datetime.fromtimestamp(stripe_details["current_period_start"]).isoformat()
            if stripe_details.get("current_period_end"):
                update_data["current_period_end"] = datetime.fromtimestamp(stripe_details["current_period_end"]).isoformat()
            
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

    async def sign_out(self):
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            
            # Clear auth state
            self.is_authenticated = False
            self.user_email = ""
            self.user_id = ""
            self.access_token = ""
            
            # Clear all dashboard state to prevent cross-user contamination
            from web_ui.api_key_state import APIKeyState
            from web_ui.lp_position_state import LPPositionState
            from web_ui.components.plan_status import PlanStatusState
            from web_ui.overview_state import OverviewState
            from web_ui.dashboard_loading_state import DashboardLoadingState
            
            api_key_state = await self.get_state(APIKeyState)
            api_key_state.api_keys = []
            
            lp_position_state = await self.get_state(LPPositionState)
            lp_position_state.lp_positions = []
            lp_position_state._cached_wallets = []
            
            plan_status_state = await self.get_state(PlanStatusState)
            plan_status_state.tier_name = "free"
            
            overview_state = await self.get_state(OverviewState)
            overview_state.total_value = 0.0
            overview_state.total_positions = 0
            
            dashboard_loading_state = await self.get_state(DashboardLoadingState)
            dashboard_loading_state.reset_loading()
            
            return rx.redirect("/")
        except Exception as e:
            self.error_message = "An error occurred during sign out. Please try again."
