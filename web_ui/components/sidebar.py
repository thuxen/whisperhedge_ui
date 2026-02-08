import reflex as rx
from ..state import AuthState
from ..config import AppConfig
from ..branding import brand_logo, COLORS
from .plan_status import plan_status_widget


class DashboardState(rx.State):
    active_section: str = "api_keys"
    payment_processing: bool = False
    payment_success_message: str = ""
    
    def set_section(self, section: str):
        self.active_section = section
    
    async def on_load(self):
        """Check for Stripe redirect and process payment if needed"""
        import sys
        import os
        
        # Check for stripe_session_id in URL params
        stripe_session_id = self.router.page.params.get("stripe_session_id", "")
        
        if stripe_session_id:
            print("=" * 80, flush=True)
            sys.stdout.flush()
            print(f"[DASHBOARD] Stripe redirect detected with session_id: {stripe_session_id}", flush=True)
            sys.stdout.flush()
            
            self.payment_processing = True
            
            try:
                # Import payment processing function
                from ..pages.payment_success import PaymentSuccessState
                
                # Get payment success state and trigger processing
                payment_state = await self.get_state(PaymentSuccessState)
                await payment_state.trigger_payment_processing(stripe_session_id)
                
                print(f"[DASHBOARD] Payment processing completed successfully", flush=True)
                sys.stdout.flush()
                
                self.payment_success_message = "Payment successful! Your plan has been upgraded."
                
                # Redirect to clean URL without session_id after 2 seconds
                yield rx.call_script(
                    "setTimeout(() => { window.location.href = '/dashboard?payment_success=true'; }, 2000);"
                )
                
            except Exception as e:
                print(f"[DASHBOARD ERROR] Payment processing failed: {e}", flush=True)
                sys.stdout.flush()
                import traceback
                traceback.print_exc()
                sys.stdout.flush()
                
                self.payment_success_message = f"Payment processing error: {str(e)}"
            
            finally:
                self.payment_processing = False


def sidebar_item(label: str, section: str, icon: str = "circle") -> rx.Component:
    """Sidebar navigation item"""
    is_active = DashboardState.active_section == section
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(label, size="3"),
            spacing="3",
            align="center",
        ),
        on_click=lambda: DashboardState.set_section(section),
        padding="0.75rem 1rem",
        border_radius="0.5rem",
        background=rx.cond(is_active, COLORS.ACCENT_PRIMARY, "transparent"),
        color=rx.cond(is_active, COLORS.TEXT_PRIMARY, COLORS.TEXT_SECONDARY),
        cursor="pointer",
        _hover={
            "background": rx.cond(is_active, COLORS.ACCENT_PRIMARY_HOVER, COLORS.BACKGROUND_ELEVATED),
        },
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                brand_logo(size="sidebar", margin_bottom="0.5rem"),
                rx.text("Dashboard", size="2", color=COLORS.TEXT_MUTED),
                spacing="1",
                align_items="start",
                width="100%",
                padding_bottom="1rem",
                border_bottom=f"1px solid {COLORS.BORDER_DEFAULT}",
            ),
            
            rx.vstack(
                sidebar_item("Overview", "overview", "layout-dashboard"),
                sidebar_item("API Keys", "api_keys", "key"),
                sidebar_item("LP Positions", "lp_positions", "coins"),
                sidebar_item("Bot Status", "bot_status", "activity"),
                sidebar_item("Manage Plan", "manage_plan", "credit-card"),
                sidebar_item("FAQ / Info", "faq", "info"),
                spacing="2",
                width="100%",
                margin_top="1.5rem",
            ),
            
            rx.spacer(),
            
            # Plan status widget
            plan_status_widget(),
            
            rx.vstack(
                rx.divider(),
                rx.hstack(
                    rx.vstack(
                        rx.text(AuthState.user_email, size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                        rx.text("Logged in", size="1", color=COLORS.TEXT_MUTED),
                        spacing="0",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.icon("log-out", size=16),
                        on_click=AuthState.sign_out,
                        variant="ghost",
                        size="2",
                        color_scheme="red",
                    ),
                    width="100%",
                    align="center",
                ),
                spacing="3",
                width="100%",
            ),
            
            spacing="4",
            height="100%",
            width="100%",
            padding="1.5rem",
        ),
        width="280px",
        height="100vh",
        border_right=f"1px solid {COLORS.BORDER_DEFAULT}",
        position="sticky",
        top="0",
        background=COLORS.BACKGROUND_SURFACE,
    )
