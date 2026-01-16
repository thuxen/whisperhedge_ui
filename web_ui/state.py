import reflex as rx
from .auth import get_supabase_client


class AuthState(rx.State):
    is_authenticated: bool = False
    user_email: str = ""
    user_id: str = ""
    error_message: str = ""
    success_message: str = ""
    is_loading: bool = False

    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    async def sign_up(self, form_data: dict):
        self.is_loading = True
        self.clear_messages()
        
        email = form_data.get("email", "")
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")
        
        if not email or not password:
            self.error_message = "Email and password are required"
            self.is_loading = False
            return
        
        if password != confirm_password:
            self.error_message = "Passwords do not match"
            self.is_loading = False
            return
        
        if len(password) < 6:
            self.error_message = "Password must be at least 6 characters"
            self.is_loading = False
            return
        
        try:
            supabase = get_supabase_client()
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                if response.session:
                    self.is_authenticated = True
                    self.user_email = email
                    self.user_id = response.user.id
                    self.success_message = "Account created successfully! Redirecting to dashboard..."
                    return rx.redirect("/dashboard")
                else:
                    self.success_message = "Account created! Please check your email to verify your account before signing in."
                    self.user_email = email
            else:
                self.error_message = "Failed to create account"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
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
                self.success_message = "Successfully logged in!"
                return rx.redirect("/dashboard")
            else:
                self.error_message = "Invalid credentials"
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
        finally:
            self.is_loading = False

    def sign_out(self):
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
            self.is_authenticated = False
            self.user_email = ""
            self.user_id = ""
            self.success_message = "Successfully logged out"
            return rx.redirect("/")
        except Exception as e:
            self.error_message = f"Error signing out: {str(e)}"
