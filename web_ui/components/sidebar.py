import reflex as rx
from ..state import AuthState
from ..config import AppConfig
from ..branding import brand_logo


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
        background=rx.cond(is_active, "var(--accent-3)", "transparent"),
        color=rx.cond(is_active, "var(--accent-11)", "var(--gray-11)"),
        cursor="pointer",
        _hover={
            "background": rx.cond(is_active, "var(--accent-4)", "var(--gray-3)"),
        },
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                brand_logo(size="sidebar", margin_bottom="0.5rem"),
                rx.text("Dashboard", size="2", color="gray"),
                spacing="1",
                align_items="start",
                width="100%",
                padding_bottom="1rem",
                border_bottom="1px solid var(--gray-5)",
            ),
            
            rx.vstack(
                sidebar_item("Overview", "overview", "layout-dashboard"),
                sidebar_item("API Keys", "api_keys", "key"),
                sidebar_item("LP Positions", "lp_positions", "coins"),
                sidebar_item("Bot Status", "bot_status", "activity"),
                sidebar_item("Settings", "settings", "settings"),
                spacing="2",
                width="100%",
                margin_top="1.5rem",
            ),
            
            rx.spacer(),
            
            rx.vstack(
                rx.divider(),
                rx.hstack(
                    rx.vstack(
                        rx.text(AuthState.user_email, size="2", weight="bold"),
                        rx.text("Logged in", size="1", color="gray"),
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
        border_right="1px solid var(--gray-5)",
        position="sticky",
        top="0",
        background="var(--color-panel)",
    )
