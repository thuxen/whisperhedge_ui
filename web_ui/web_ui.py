import reflex as rx
from .pages import login_page, signup_page, dashboard_page
from .branding import brand_logo, BrandConfig


def index() -> rx.Component:
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


app = rx.App()
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(dashboard_page, route="/dashboard")
