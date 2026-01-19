import reflex as rx
from ..state import AuthState
from ..branding import brand_logo


def login_page() -> rx.Component:
    return rx.container(
        rx.vstack(
            brand_logo(size="landing", margin_bottom="1rem"),
            rx.text("Sign in to your account", size="4", color="gray", margin_bottom="2rem"),
            
            rx.cond(
                AuthState.error_message != "",
                rx.callout(
                    AuthState.error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    margin_bottom="1rem",
                ),
            ),
            
            rx.cond(
                AuthState.success_message != "",
                rx.callout(
                    AuthState.success_message,
                    icon="check",
                    color_scheme="green",
                    role="alert",
                    margin_bottom="1rem",
                ),
            ),
            
            rx.card(
                rx.vstack(
                    rx.form(
                        rx.vstack(
                            rx.text("Email", size="3", weight="bold"),
                            rx.input(
                                placeholder="Enter your email",
                                name="email",
                                type="email",
                                required=True,
                                width="100%",
                            ),
                            
                            rx.text("Password", size="3", weight="bold", margin_top="1rem"),
                            rx.input(
                                placeholder="Enter your password",
                                name="password",
                                type="password",
                                required=True,
                                width="100%",
                            ),
                            
                            rx.button(
                                "Sign In",
                                type="submit",
                                size="3",
                                width="100%",
                                margin_top="1.5rem",
                                loading=AuthState.is_loading,
                            ),
                            
                            spacing="2",
                            width="100%",
                        ),
                        on_submit=AuthState.sign_in,
                        reset_on_submit=False,
                    ),
                    
                    rx.divider(margin_top="1.5rem", margin_bottom="1.5rem"),
                    
                    rx.hstack(
                        rx.text("Don't have an account?", size="2"),
                        rx.link("Sign up", href="/signup", size="2", weight="bold"),
                        spacing="2",
                        justify="center",
                    ),
                    
                    width="100%",
                ),
                size="4",
                max_width="28rem",
                width="100%",
            ),
            
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
            width="100%",
        ),
        size="3",
    )
