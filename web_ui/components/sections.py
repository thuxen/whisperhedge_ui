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
        rx.heading("Trading Accounts", size="7", margin_bottom="1rem"),
        api_keys_component(),
        spacing="4",
        width="100%",
    )


class FAQState(rx.State):
    """State for FAQ/Help Center tabs"""
    active_tab: str = "faq"
    
    def set_tab(self, tab: str):
        self.active_tab = tab


def faq_content() -> rx.Component:
    """FAQ tab content"""
    return rx.vstack(
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
        
        rx.card(
            rx.vstack(
                rx.heading("What happens if the bot stops working?", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Your LP positions and hedge positions are independent. If WhisperHedge stops operating, your LP positions continue earning fees as normal, and your hedge positions remain open on Hyperliquid. You can manually close or adjust hedge positions at any time through your Hyperliquid account.",
                    size="3",
                    line_height="1.7",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def getting_started_content() -> rx.Component:
    """Getting Started tab content"""
    return rx.vstack(
        rx.card(
            rx.vstack(
                rx.heading("Step 1: Add Your LP Positions", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Navigate to the 'LP Positions' section and connect your wallet. WhisperHedge will automatically detect your active liquidity positions on supported DEXs (Uniswap V3, Aerodrome, PancakeSwap).",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "You can also manually add positions by providing the pool address and position details.",
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
                rx.heading("Step 2: Configure Your Hyperliquid Trading Account", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Create a trade-only API key on Hyperliquid with the following permissions:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Trading enabled"),
                    rx.list_item("Withdrawals DISABLED (critical for security)"),
                    rx.list_item("Transfers DISABLED"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Add your trading account in the 'Trading Accounts' section. WhisperHedge will verify the credentials have proper permissions and sufficient margin.",
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
                rx.heading("Step 3: Fund Your Hyperliquid Account", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Deposit USDC to your Hyperliquid account to use as margin for hedge positions. The recommended margin is 20-30% of your total LP position value to maintain safe leverage ratios.",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Example: If you have $10,000 in LP positions, deposit $2,000-$3,000 USDC to Hyperliquid.",
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
                rx.heading("Step 4: Activate Hedging", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Once your LP positions are added and API key is configured, the bot will automatically begin monitoring your positions and executing hedges based on your plan tier's strategy.",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Monitor your hedge performance in the 'Bot Status' section and adjust your positions as needed.",
                    size="3",
                    line_height="1.7",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def troubleshooting_content() -> rx.Component:
    """Troubleshooting tab content"""
    return rx.vstack(
        rx.card(
            rx.vstack(
                rx.heading("API Key Not Connecting", size="5", weight="bold", color="var(--accent-11)"),
                rx.text("Common issues:", size="3", line_height="1.7", weight="bold", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Verify the API key has trading permissions enabled"),
                    rx.list_item("Ensure withdrawals are disabled on the key"),
                    rx.list_item("Check that you copied the full API secret (no spaces or line breaks)"),
                    rx.list_item("Confirm your Hyperliquid account has sufficient margin"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("LP Position Not Detected", size="5", weight="bold", color="var(--accent-11)"),
                rx.text("Possible solutions:", size="3", line_height="1.7", weight="bold", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Ensure your wallet is connected to the correct network"),
                    rx.list_item("Verify the position is on a supported DEX (Uniswap V3, Aerodrome, PancakeSwap)"),
                    rx.list_item("Check that the position is still active and has liquidity"),
                    rx.list_item("Try manually adding the position using the pool contract address"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Hedge Positions Not Opening", size="5", weight="bold", color="var(--accent-11)"),
                rx.text("Check the following:", size="3", line_height="1.7", weight="bold", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Verify your Hyperliquid account has sufficient USDC margin"),
                    rx.list_item("Ensure the API key permissions are correct"),
                    rx.list_item("Check that the perpetual market exists for your LP pair on Hyperliquid"),
                    rx.list_item("Review the Bot Status section for error messages"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Need More Help?", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "If you're experiencing issues not covered here, please contact support through the dashboard or email support@whisperhedge.com with details about your issue.",
                    size="3",
                    line_height="1.7",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def api_docs_content() -> rx.Component:
    """API Documentation tab content"""
    return rx.vstack(
        rx.card(
            rx.vstack(
                rx.heading("Hyperliquid API Key Setup", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "To create a trade-only API key on Hyperliquid:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.ordered_list(
                    rx.list_item("Log into your Hyperliquid account"),
                    rx.list_item("Navigate to Settings → API Keys"),
                    rx.list_item("Click 'Create New API Key'"),
                    rx.list_item("Enable 'Trading' permission"),
                    rx.list_item("Ensure 'Withdrawals' and 'Transfers' are DISABLED"),
                    rx.list_item("Copy both the API Key and Secret"),
                    rx.list_item("Store the secret securely (it won't be shown again)"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Required API Permissions", size="5", weight="bold", color="var(--accent-11)"),
                rx.text("Enabled:", size="3", line_height="1.7", weight="bold", color="green", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Trading (required)"),
                    rx.list_item("Read account data (required)"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                    margin_bottom="1rem",
                ),
                rx.text("Disabled:", size="3", line_height="1.7", weight="bold", color="red", margin_bottom="0.5rem"),
                rx.unordered_list(
                    rx.list_item("Withdrawals (must be disabled)"),
                    rx.list_item("Transfers (must be disabled)"),
                    rx.list_item("Account modifications (must be disabled)"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Supported DEX Protocols", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "WhisperHedge currently supports LP positions on:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Uniswap V3 (Ethereum, Arbitrum, Optimism, Base, Polygon)"),
                    rx.list_item("Aerodrome (Base)"),
                    rx.list_item("PancakeSwap V3 (BSC, Ethereum)"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def best_practices_content() -> rx.Component:
    """Best Practices tab content"""
    return rx.vstack(
        rx.card(
            rx.vstack(
                rx.heading("Optimal Margin Allocation", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Maintain 20-30% of your LP position value as margin on Hyperliquid. This provides:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Safe leverage ratios (typically 3-5x)"),
                    rx.list_item("Buffer for market volatility"),
                    rx.list_item("Room for position adjustments"),
                    rx.list_item("Protection against liquidation risk"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Position Monitoring", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Regularly check your dashboard to:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Verify hedge ratios are within expected ranges"),
                    rx.list_item("Monitor funding rates on perpetual positions"),
                    rx.list_item("Ensure LP positions are still in range"),
                    rx.list_item("Check margin levels remain healthy (>50% of initial)"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("Risk Management", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Follow these guidelines to minimize risk:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Start with smaller positions to test the system"),
                    rx.list_item("Never use API keys with withdrawal permissions"),
                    rx.list_item("Keep emergency margin available for volatile markets"),
                    rx.list_item("Understand the correlation between your LP pair assets"),
                    rx.list_item("Monitor funding costs vs LP fee earnings"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        rx.card(
            rx.vstack(
                rx.heading("When to Adjust Positions", size="5", weight="bold", color="var(--accent-11)"),
                rx.text(
                    "Consider manually adjusting when:",
                    size="3",
                    line_height="1.7",
                    margin_bottom="0.5rem",
                ),
                rx.unordered_list(
                    rx.list_item("Your LP position moves out of range"),
                    rx.list_item("Funding rates become excessively negative"),
                    rx.list_item("Market volatility spikes significantly"),
                    rx.list_item("You're approaching liquidation levels"),
                    size="3",
                    spacing="2",
                    margin_left="1.5rem",
                ),
                spacing="2",
                align_items="start",
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def help_tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    """Tab button for help center navigation"""
    is_active = FAQState.active_tab == tab_id
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(label, size="2", weight="medium"),
            spacing="2",
            align="center",
        ),
        on_click=lambda: FAQState.set_tab(tab_id),
        padding="0.75rem 1rem",
        border_radius="0.5rem",
        background=rx.cond(is_active, "var(--accent-3)", "transparent"),
        color=rx.cond(is_active, "var(--accent-11)", "var(--gray-11)"),
        border=rx.cond(is_active, "1px solid var(--accent-6)", "1px solid transparent"),
        cursor="pointer",
        _hover={
            "background": rx.cond(is_active, "var(--accent-4)", "var(--gray-3)"),
        },
    )


def faq_section() -> rx.Component:
    """Enhanced FAQ/Help Center with categorized tabs"""
    return rx.vstack(
        rx.heading("Help Center", size="7", margin_bottom="1rem"),
        
        # Tab navigation
        rx.hstack(
            help_tab_button("FAQ", "faq", "help-circle"),
            help_tab_button("Getting Started", "getting_started", "rocket"),
            help_tab_button("Troubleshooting", "troubleshooting", "wrench"),
            help_tab_button("API Docs", "api_docs", "code"),
            help_tab_button("Best Practices", "best_practices", "shield-check"),
            spacing="2",
            width="100%",
            margin_bottom="1.5rem",
            flex_wrap="wrap",
        ),
        
        # Tab content
        rx.box(
            rx.cond(
                FAQState.active_tab == "faq",
                faq_content(),
            ),
            rx.cond(
                FAQState.active_tab == "getting_started",
                getting_started_content(),
            ),
            rx.cond(
                FAQState.active_tab == "troubleshooting",
                troubleshooting_content(),
            ),
            rx.cond(
                FAQState.active_tab == "api_docs",
                api_docs_content(),
            ),
            rx.cond(
                FAQState.active_tab == "best_practices",
                best_practices_content(),
            ),
            width="100%",
        ),
        
        spacing="4",
        width="100%",
    )


def manage_plan_section() -> rx.Component:
    """Manage Plan section for dashboard"""
    from ..pages.manage_plan import ManagePlanState
    return rx.fragment(
        manage_plan_content(),
        on_mount=ManagePlanState.sync_from_plan_status,
    )
