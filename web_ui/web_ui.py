import reflex as rx
from .pages import login_page, signup_page, dashboard_page, landing_page


app = rx.App()
app.add_page(landing_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(dashboard_page, route="/dashboard")
