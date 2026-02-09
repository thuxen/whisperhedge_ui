import reflex as rx
from .api_keys import api_keys_component
from ..overview_state import OverviewState
from ..pages.manage_plan import manage_plan_content


def overview_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Overview", size="7", margin_bottom="1rem"),
        
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.text("LP Positions", size="2", color="gray", weight="medium"),
                    rx.text(OverviewState.lp_positions_display, size="8", weight="bold", color="blue"),
                    rx.text(OverviewState.lp_positions_text, size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
                width="100%",
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("API Keys", size="2", color="gray", weight="medium"),
                    rx.text(OverviewState.api_keys_display, size="8", weight="bold", color="purple"),
                    rx.text(OverviewState.api_keys_text, size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
                width="100%",
            ),
            
            rx.card(
                rx.vstack(
                    rx.text("Total Value of Active Positions", size="2", color="gray", weight="medium"),
                    rx.text(OverviewState.total_value_formatted, size="8", weight="bold", color="green"),
                    rx.text("Liquidity Pool + Hedge Account Values", size="2", color="gray"),
                    spacing="2",
                    align_items="start",
                ),
                width="100%",
            ),
            
            columns="3",
            spacing="4",
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
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text(
                    "This section is under development.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
                align_items="center",
                padding="4rem",
            ),
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def settings_section() -> rx.Component:
    from ..pages.settings import (
        SettingsState,
        profile_section,
        security_section,
        preferences_section,
        danger_zone_section,
    )
    
    return rx.vstack(
        rx.heading("Settings", size="7", margin_bottom="1rem"),
        
        rx.cond(
            SettingsState.success_message != "",
            rx.callout(
                SettingsState.success_message,
                icon="check",
                color_scheme="green",
                margin_bottom="1rem",
            ),
        ),
        rx.cond(
            SettingsState.error_message != "",
            rx.callout(
                SettingsState.error_message,
                icon="alert-triangle",
                color_scheme="red",
                margin_bottom="1rem",
            ),
        ),
        
        profile_section(),
        security_section(),
        preferences_section(),
        danger_zone_section(),
        
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


def faq_section() -> rx.Component:
    return rx.vstack(
        rx.heading("FAQ / Info", size="7", margin_bottom="1rem"),
        
        rx.card(
            rx.vstack(
                rx.heading("Why Dynamic Hedging Beats Full Hedging?", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "In DeFi liquidity provision, full hedging (100% delta-neutral) seems like the ultimate safety net—eliminating all price risk. But in volatile/vol pairs like cbBTC/WETH or AAVE/WETH, assets don't always move in lockstep. Temporary divergences (when one asset outperforms the other) force full hedging to sell winners and buy losers at the worst moments, creating compounding losses known as the 'staircase effect.'",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Our dynamic hedging engine uses real-time indicators like correlation and mean-reversion half-life to detect these trends early, then intentionally under-hedges (e.g., 80–94% instead of 100%) to let a small portion ride the wave. This unhedged slice captures profit from the trend, offsetting impermanent loss and boosting net returns by 10–30% with lower drawdowns.",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "It's not added risk—it's precision engineering that turns market volatility into your advantage, keeping you 80–95% protected while profiting from the 5–20% of time when trends dominate.",
                    size="3",
                    line_height="1.7",
                    weight="medium",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("How does WhisperHedge access my funds?", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "WhisperHedge never touches your LP positions directly. You maintain full custody of your liquidity pool assets on the DeFi protocol of your choice. We only perform hedging operations on Hyperliquid using the API key you provide.",
                    size="3",
                    line_height="1.7",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("What can WhisperHedge do with my API key?", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Your Hyperliquid API key is used exclusively for trading perpetual positions to hedge your LP exposure. The API key permissions are limited to:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Open and close perpetual positions"),
                    rx.list_item("Adjust position sizes and leverage"),
                    rx.list_item("Place and cancel orders"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Critically, the API key cannot:",
                    size="3",
                    line_height="1.7",
                    weight="bold",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Withdraw funds from your account"),
                    rx.list_item("Transfer assets to other addresses"),
                    rx.list_item("Change account settings or permissions"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                rx.text(
                    "Your capital remains secure in your Hyperliquid account at all times. We can only execute trades within the account—never move funds out.",
                    size="3",
                    line_height="1.7",
                    weight="medium",
                    margin_top="0.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def manage_plan_section() -> rx.Component:
    """Manage Plan section for dashboard"""
    return manage_plan_content()
