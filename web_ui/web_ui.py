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
    blog_hidden_cost_page,
)
from .pages.manage_plan import manage_plan_page, ManagePlanState
from .pages.payment_success import payment_success_page, PaymentSuccessState
from .pages.settings import settings
from .components import DashboardState


app = rx.App()
app.add_page(landing_page, route="/", image="/favicon.ico")
app.add_page(login_page, route="/login", image="/favicon.ico")
app.add_page(signup_page, route="/signup", image="/favicon.ico")
app.add_page(dashboard_page, route="/dashboard", on_load=DashboardState.on_load, image="/favicon.ico")
app.add_page(manage_plan_page, route="/manage-plan", on_load=ManagePlanState.on_load, image="/favicon.ico")
app.add_page(payment_success_page, route="/payment-success", on_load=PaymentSuccessState.on_load, image="/favicon.ico")
app.add_page(settings, route="/settings", image="/favicon.ico")
app.add_page(privacy_page, route="/privacy", image="/favicon.ico")
app.add_page(terms_page, route="/terms", image="/favicon.ico")
app.add_page(cookies_page, route="/cookies", image="/favicon.ico")
app.add_page(about_page, route="/about", image="/favicon.ico")
app.add_page(contact_page, route="/contact", image="/favicon.ico")
app.add_page(blog_page, route="/blog", image="/favicon.ico")
app.add_page(blog_hidden_cost_page, route="/blog/hidden-cost-of-liquidity", image="/favicon.ico")
