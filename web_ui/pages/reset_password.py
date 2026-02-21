import reflex as rx
from ..state import AuthState
from ..branding import brand_logo, COLORS


def reset_password_page() -> rx.Component:
    return rx.box(
        rx.script("""
            window.addEventListener('load', function() {
                console.log('[RESET PASSWORD] Page loaded, extracting tokens from URL hash');
                const hash = window.location.hash.substring(1);
                console.log('[RESET PASSWORD] Hash:', hash ? 'present' : 'empty');
                
                const params = new URLSearchParams(hash);
                const accessToken = params.get('access_token');
                const refreshToken = params.get('refresh_token');
                
                console.log('[RESET PASSWORD] Access token:', accessToken ? 'found' : 'not found');
                console.log('[RESET PASSWORD] Refresh token:', refreshToken ? 'found' : 'not found');
                
                if (accessToken) {
                    const field = document.getElementById('access_token_field');
                    if (field) {
                        field.value = accessToken;
                        console.log('[RESET PASSWORD] Access token set in hidden field');
                    } else {
                        console.error('[RESET PASSWORD] access_token_field not found!');
                    }
                }
                if (refreshToken) {
                    const field = document.getElementById('refresh_token_field');
                    if (field) {
                        field.value = refreshToken;
                        console.log('[RESET PASSWORD] Refresh token set in hidden field');
                    } else {
                        console.error('[RESET PASSWORD] refresh_token_field not found!');
                    }
                }
            });
        """),
        rx.container(
            rx.vstack(
                brand_logo(size="landing", margin_bottom="1rem"),
                rx.text("Set new password", size="4", color=COLORS.TEXT_SECONDARY, margin_bottom="2rem"),
            
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
                                rx.el.input(
                                    type="hidden",
                                    name="access_token",
                                    id="access_token_field",
                                    value=""
                                ),
                                rx.el.input(
                                    type="hidden",
                                    name="refresh_token",
                                    id="refresh_token_field",
                                    value=""
                                ),
                                
                                rx.text("New Password", size="3", weight="bold", color=COLORS.TEXT_PRIMARY),
                            rx.input(
                                placeholder="Enter new password",
                                name="password",
                                type="password",
                                required=True,
                                width="100%",
                            ),
                            
                                rx.text("Confirm Password", size="3", weight="bold", margin_top="1rem", color=COLORS.TEXT_PRIMARY),
                            rx.input(
                                placeholder="Confirm new password",
                                name="confirm_password",
                                type="password",
                                required=True,
                                width="100%",
                            ),
                            
                                rx.text(
                                    "Password must be at least 6 characters",
                                    size="1",
                                    color=COLORS.TEXT_MUTED,
                                    margin_top="0.5rem",
                                ),
                            
                                rx.button(
                                    "Update Password",
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
                        on_submit=AuthState.update_password,
                        reset_on_submit=False,
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
