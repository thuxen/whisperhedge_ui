import reflex as rx
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
        
        email = form_data.get("email", "")
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
                return rx.redirect("/dashboard")
            else:
                self.error_message = "Invalid credentials"
        except Exception as e:
            self.error_message = "An error occurred during sign in. Please try again."
        finally:
            self.is_loading = False

    def sign_out(self):
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            self.is_authenticated = False
            self.user_email = ""
            self.user_id = ""
            self.access_token = ""
            self.success_message = "Successfully logged out"
            return rx.redirect("/")
        except Exception as e:
            self.error_message = "An error occurred during sign out. Please try again."
