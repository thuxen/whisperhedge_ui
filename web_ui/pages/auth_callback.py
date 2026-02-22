import reflex as rx
from ..state import AuthState
from ..branding import brand_logo, COLORS


def auth_callback_page() -> rx.Component:
    """Callback page for magic link authentication"""
    return rx.box(
        # Client-side script to extract tokens from URL hash and send to backend
        rx.script("""
            (function() {
                console.log('[AUTH CALLBACK] Extracting tokens from URL hash');
                const hash = window.location.hash;
                
                if (hash) {
                    const params = new URLSearchParams(hash.substring(1));
                    const accessToken = params.get('access_token');
                    const refreshToken = params.get('refresh_token');
                    
                    console.log('[AUTH CALLBACK] Access token found:', !!accessToken);
                    console.log('[AUTH CALLBACK] Refresh token found:', !!refreshToken);
                    
                    if (accessToken && refreshToken) {
                        // Store tokens in localStorage for Reflex LocalStorage to retrieve
                        localStorage.setItem('magic_link_access_token', accessToken);
                        localStorage.setItem('magic_link_refresh_token', refreshToken);
                        console.log('[AUTH CALLBACK] Tokens stored in localStorage');
                        
                        // Remove hash and reload to trigger backend handler
                        setTimeout(() => {
                            window.location.href = window.location.pathname;
                        }, 100);
                    } else {
                        console.log('[AUTH CALLBACK] No tokens in URL hash');
                    }
                } else {
                    console.log('[AUTH CALLBACK] No hash fragment in URL');
                }
            })();
        """),
        rx.container(
            rx.vstack(
                brand_logo(size="landing", margin_bottom="2rem"),
                rx.spinner(size="3", margin_bottom="1rem"),
                rx.text(
                    "Logging you in...",
                    size="5",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Please wait while we verify your magic link",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                ),
                spacing="4",
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
