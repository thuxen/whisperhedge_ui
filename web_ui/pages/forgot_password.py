import reflex as rx
from ..state import AuthState
from ..branding import brand_logo, COLORS


def forgot_password_page() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                brand_logo(size="landing", margin_bottom="1rem"),
                rx.text("Reset your password", size="4", color=COLORS.TEXT_SECONDARY, margin_bottom="2rem"),
            
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
                                rx.text("Email", size="3", weight="bold", color=COLORS.TEXT_PRIMARY),
                            rx.input(
                                placeholder="Enter your email",
                                name="email",
                                type="email",
                                required=True,
                                width="100%",
                            ),
                            
                                rx.button(
                                    "Send Reset Link",
                                    type="submit",
                                    size="3",
                                    width="100%",
                                    margin_top="1.5rem",
                                    loading=AuthState.is_loading,
                                    background=COLORS.BUTTON_PRIMARY_BG,
                                    color=COLORS.BUTTON_PRIMARY_TEXT,
                                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                                ),
                            
                            spacing="2",
                            width="100%",
                        ),
                        on_submit=AuthState.reset_password,
                        reset_on_submit=False,
                    ),
                    
                    rx.divider(margin_top="1.5rem", margin_bottom="1.5rem"),
                    
                        rx.hstack(
                            rx.text("Remember your password?", size="2", color=COLORS.TEXT_SECONDARY),
                            rx.link("Sign in", href="/login", size="2", weight="bold", color=COLORS.ACCENT_PRIMARY),
                        spacing="2",
                        justify="center",
                    ),
                    
                    width="100%",
                ),
                    size="4",
                    max_width="28rem",
                    width="100%",
                    background=COLORS.CARD_BG,
                    style={"border": f"1px solid {COLORS.CARD_BORDER}"},
                ),
            
                spacing="5",
                justify="center",
                align="center",
                min_height="85vh",
                width="100%",
            ),
            size="3",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
        min_height="100vh",
    )
