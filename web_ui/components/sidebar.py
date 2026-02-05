import reflex as rx
from ..state import AuthState
from ..config import AppConfig
from ..branding import brand_logo, COLORS
from .plan_status import plan_status_widget


class DashboardState(rx.State):
    active_section: str = "api_keys"
    
    def set_section(self, section: str):
        self.active_section = section


def sidebar_item(label: str, section: str, icon: str = "circle") -> rx.Component:
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
                sidebar_item("FAQ / Info", "faq", "info"),
                sidebar_item("Settings", "settings", "settings"),
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
