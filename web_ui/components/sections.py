import reflex as rx
from .api_keys import api_keys_component


def overview_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Overview", size="7", margin_bottom="1rem"),
        
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("Total Value Locked", size="2", color="gray"),
                    rx.heading("$0.00", size="6"),
                    rx.text("+0.00%", size="2", color="green"),
                    spacing="2",
                    align_items="start",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.text("Active Positions", size="2", color="gray"),
                    rx.heading("0", size="6"),
                    rx.text("No active positions", size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.text("Bot Status", size="2", color="gray"),
                    rx.heading("Inactive", size="6"),
                    rx.badge("Configure API keys to start", color_scheme="orange"),
                    spacing="2",
                    align_items="start",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.text("24h PnL", size="2", color="gray"),
                    rx.heading("$0.00", size="6"),
                    rx.text("No trading activity", size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
            ),
            columns="2",
            spacing="4",
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Recent Activity", size="5"),
                rx.text(
                    "No recent activity. Configure your API keys to get started.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
            ),
            margin_top="2rem",
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def lp_positions_section() -> rx.Component:
    from .lp_positions import lp_positions_component
    return lp_positions_component()


def bot_status_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Bot Status", size="7", margin_bottom="1rem"),
        
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.heading("Hedging Bot", size="5"),
                    rx.spacer(),
                    rx.badge("Inactive", color_scheme="gray"),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    "Configure your API keys to activate the hedging bot.",
                    size="3",
                    color="gray",
                ),
                rx.divider(margin_top="1rem", margin_bottom="1rem"),
                rx.vstack(
                    rx.text("Bot Features:", size="3", weight="bold"),
                    rx.text("• Automated hedging strategies", size="2", color="gray"),
                    rx.text("• Real-time position monitoring", size="2", color="gray"),
                    rx.text("• Risk management controls", size="2", color="gray"),
                    rx.text("• Performance analytics", size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
                spacing="3",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def settings_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Settings", size="7", margin_bottom="1rem"),
        
        rx.card(
            rx.vstack(
                rx.heading("Account Settings", size="5"),
                rx.text(
                    "Manage your account preferences and security settings.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Bot Configuration", size="5"),
                rx.text(
                    "Configure hedging strategies, risk parameters, and trading preferences.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
            ),
            margin_top="1rem",
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def api_keys_section() -> rx.Component:
    return rx.vstack(
        rx.heading("API Keys", size="7", margin_bottom="1rem"),
        api_keys_component(),
        spacing="4",
        width="100%",
    )
