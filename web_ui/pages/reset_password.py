import reflex as rx
from ..state import AuthState
from ..branding import brand_logo, COLORS


def reset_password_page() -> rx.Component:
    return rx.box(
        rx.script("""
            function extractTokens() {
                // Try hash first
                const hash = window.location.hash.substring(1);
                let params = new URLSearchParams(hash);
                let accessToken = params.get('access_token');
                let refreshToken = params.get('refresh_token');
                
                // If not in hash, try query string
                if (!accessToken || !refreshToken) {
                    const query = window.location.search.substring(1);
                    params = new URLSearchParams(query);
                    accessToken = accessToken || params.get('access_token');
                    refreshToken = refreshToken || params.get('refresh_token');
                }
                
                console.log('[RESET PASSWORD] Tokens extracted:', {
                    access: !!accessToken,
                    refresh: !!refreshToken,
                    hash: window.location.hash,
                    query: window.location.search
                });
                
                return { accessToken, refreshToken };
            }
            
            function setTokens() {
                const { accessToken, refreshToken } = extractTokens();
                const accessField = document.getElementById('access_token_field');
                const refreshField = document.getElementById('refresh_token_field');
                
                if (accessField && refreshField) {
                    if (accessToken) {
                        accessField.value = accessToken;
                        console.log('[RESET PASSWORD] Set access token');
                    }
                    if (refreshToken) {
                        refreshField.value = refreshToken;
                        console.log('[RESET PASSWORD] Set refresh token');
                    }
                    // Also store in sessionStorage as backup
                    if (accessToken && refreshToken) {
                        sessionStorage.setItem('reset_access_token', accessToken);
                        sessionStorage.setItem('reset_refresh_token', refreshToken);
                        console.log('[RESET PASSWORD] Tokens stored in sessionStorage');
                    }
                    return true;
                }
                console.warn('[RESET PASSWORD] Hidden input fields not found');
                return false;
            }
            
            // Run when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', function() {
                    setTokens();
                });
            } else {
                setTokens();
            }
            
            // Retry a few times in case inputs are rendered later
            let attempts = 0;
            const maxAttempts = 10;
            const interval = setInterval(() => {
                if (setTokens() || attempts >= maxAttempts) {
                    clearInterval(interval);
                }
                attempts++;
            }, 200);
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
                                rx.input(type="hidden", id="access_token_field", name="access_token", value=""),
                                rx.input(type="hidden", id="refresh_token_field", name="refresh_token", value=""),
                                
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
