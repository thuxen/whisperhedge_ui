import reflex as rx
from ..state import AuthState
from ..branding import brand_logo, COLORS


def auth_callback_page() -> rx.Component:
    """Callback page for magic link authentication"""
    return rx.box(
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
