import reflex as rx
from ..branding import brand_logo, BrandConfig


def whitelabel_landing() -> rx.Component:
    """
    Simple landing page for whitelabel partners
    
    Keep this minimal and generic for partners to customize.
    """
    return rx.container(
        rx.vstack(
            brand_logo(size="landing", margin_bottom="2rem"),
            rx.text(
                BrandConfig.TAGLINE,
                size="5",
                color="gray",
                margin_bottom="3rem",
            ),
            rx.hstack(
                rx.link(
                    rx.button("Sign In", size="3"),
                    href="/login",
                ),
                rx.link(
                    rx.button("Create Account", size="3", variant="soft"),
                    href="/signup",
                ),
                spacing="4",
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        ),
    )
