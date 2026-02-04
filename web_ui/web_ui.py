import reflex as rx
from .pages import (
    login_page,
    signup_page,
    dashboard_page,
    landing_page,
    privacy_page,
    terms_page,
    cookies_page,
    about_page,
    contact_page,
    blog_page,
)


app = rx.App()
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(privacy_page, route="/privacy")
app.add_page(terms_page, route="/terms")
app.add_page(cookies_page, route="/cookies")
app.add_page(about_page, route="/about")
app.add_page(contact_page, route="/contact")
app.add_page(blog_page, route="/blog")
