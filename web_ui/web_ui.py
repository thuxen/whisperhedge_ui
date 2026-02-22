import reflex as rx
from .pages import (
    login_page,
    signup_page,
    forgot_password_page,
    auth_callback_page,
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
from .state import AuthState


# Analytics scripts that will be injected into the head of every page
analytics_scripts = [
    # Google Analytics
    rx.script(src="https://www.googletagmanager.com/gtag/js?id=G-V3S6FLHXV8", custom_attrs={"async": True}),
    rx.script("""
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-V3S6FLHXV8');
    """),
    # Mixpanel
    rx.script("""
        (function(e,c){if(!c.__SV){var l,h;window.mixpanel=c;c._i=[];c.init=function(q,r,f){function t(d,a){var g=a.split(".");2==g.length&&(d=d[g[0]],a=g[1]);d[a]=function(){d.push([a].concat(Array.prototype.slice.call(arguments,0)))}}var b=c;"undefined"!==typeof f?b=c[f]=[]:f="mixpanel";b.people=b.people||[];b.toString=function(d){var a="mixpanel";"mixpanel"!==f&&(a+="."+f);d||(a+=" (stub)");return a};b.people.toString=function(){return b.toString(1)+".people (stub)"};l="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders start_session_recording stop_session_recording people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
        for(h=0;h<l.length;h++)t(b,l[h]);var n="set set_once union unset remove delete".split(" ");b.get_group=function(){function d(p){a[p]=function(){b.push([g,[p].concat(Array.prototype.slice.call(arguments,0))])}}for(var a={},g=["get_group"].concat(Array.prototype.slice.call(arguments,0)),m=0;m<n.length;m++)d(n[m]);return a};c._i.push([q,r,f])};c.__SV=1.2;var k=e.createElement("script");k.type="text/javascript";k.async=!0;k.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?MIXPANEL_CUSTOM_LIB_URL:"file:"===
        e.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";e=e.getElementsByTagName("script")[0];e.parentNode.insertBefore(k,e)}})(document,window.mixpanel||[])
        
        mixpanel.init('2d6698da226871e8b48d1c63a9cc242e', {
            autocapture: true,
            record_sessions_percent: 100,
        })
    """),
]

app = rx.App(head_components=analytics_scripts)
app.add_page(landing_page, route="/", image="/favicon.ico")
app.add_page(login_page, route="/login", image="/favicon.ico")
app.add_page(signup_page, route="/signup", image="/favicon.ico")
app.add_page(forgot_password_page, route="/forgot-password", image="/favicon.ico")
app.add_page(auth_callback_page, route="/auth/callback", on_load=AuthState.handle_magic_link_callback, image="/favicon.ico")
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
