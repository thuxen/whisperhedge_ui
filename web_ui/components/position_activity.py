"""Activity dialog component for displaying LP position logs/trades"""
import reflex as rx
from ..lp_position_state import LPPositionState


def activity_tab_button(label: str, tab_id: str, icon: str) -> rx.Component:
    """Tab button for activity dialog navigation"""
    is_active = LPPositionState.activity_tab == tab_id
    
    return rx.box(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(label, size="2", weight="medium"),
            spacing="2",
            align="center",
        ),
        on_click=lambda: LPPositionState.set_activity_tab(tab_id),
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


def trades_tab_content() -> rx.Component:
    """Trades tab showing hedge execution history"""
    return rx.vstack(
        rx.text(
            "Recent Hedge Trades",
            size="4",
            weight="bold",
            margin_bottom="1rem",
        ),
        
        # Table header
        rx.box(
            rx.grid(
                rx.text("Date/Time", size="2", weight="bold", color="var(--gray-11)"),
                rx.text("Action", size="2", weight="bold", color="var(--gray-11)"),
                rx.text("Asset", size="2", weight="bold", color="var(--gray-11)"),
                rx.text("Size", size="2", weight="bold", color="var(--gray-11)"),
                rx.text("Price", size="2", weight="bold", color="var(--gray-11)"),
                rx.text("Value", size="2", weight="bold", color="var(--gray-11)"),
                columns="6",
                spacing="3",
                width="100%",
            ),
            padding="0.75rem 1rem",
            background="var(--gray-3)",
            border_radius="8px 8px 0 0",
            width="100%",
        ),
        
        # Sample trade rows
        rx.vstack(
            # Trade 1
            rx.box(
                rx.grid(
                    rx.text("Feb 17, 10:15 AM", size="2"),
                    rx.badge("Open", color_scheme="blue", size="1"),
                    rx.text("ETH-PERP", size="2", weight="medium"),
                    rx.text("-2.5 ETH", size="2"),
                    rx.text("$2,845.30", size="2"),
                    rx.text("$7,113.25", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 2
            rx.box(
                rx.grid(
                    rx.text("Feb 17, 08:42 AM", size="2"),
                    rx.badge("Adjust", color_scheme="purple", size="1"),
                    rx.text("ETH-PERP", size="2", weight="medium"),
                    rx.text("+0.8 ETH", size="2"),
                    rx.text("$2,838.15", size="2"),
                    rx.text("$2,270.52", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 3
            rx.box(
                rx.grid(
                    rx.text("Feb 16, 11:20 PM", size="2"),
                    rx.badge("Adjust", color_scheme="purple", size="1"),
                    rx.text("WBTC-PERP", size="2", weight="medium"),
                    rx.text("-0.15 BTC", size="2"),
                    rx.text("$51,240.00", size="2"),
                    rx.text("$7,686.00", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 4
            rx.box(
                rx.grid(
                    rx.text("Feb 16, 06:15 PM", size="2"),
                    rx.badge("Open", color_scheme="blue", size="1"),
                    rx.text("WBTC-PERP", size="2", weight="medium"),
                    rx.text("-1.2 BTC", size="2"),
                    rx.text("$51,180.50", size="2"),
                    rx.text("$61,416.60", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 5
            rx.box(
                rx.grid(
                    rx.text("Feb 16, 02:30 PM", size="2"),
                    rx.badge("Close", color_scheme="gray", size="1"),
                    rx.text("ETH-PERP", size="2", weight="medium"),
                    rx.text("+1.5 ETH", size="2"),
                    rx.text("$2,822.40", size="2"),
                    rx.text("$4,233.60", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 6
            rx.box(
                rx.grid(
                    rx.text("Feb 16, 09:45 AM", size="2"),
                    rx.badge("Adjust", color_scheme="purple", size="1"),
                    rx.text("ETH-PERP", size="2", weight="medium"),
                    rx.text("-0.5 ETH", size="2"),
                    rx.text("$2,815.20", size="2"),
                    rx.text("$1,407.60", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                border_bottom="1px solid var(--gray-4)",
                width="100%",
            ),
            
            # Trade 7
            rx.box(
                rx.grid(
                    rx.text("Feb 15, 07:20 PM", size="2"),
                    rx.badge("Open", color_scheme="blue", size="1"),
                    rx.text("ETH-PERP", size="2", weight="medium"),
                    rx.text("-3.2 ETH", size="2"),
                    rx.text("$2,808.90", size="2"),
                    rx.text("$8,988.48", size="2"),
                    columns="6",
                    spacing="3",
                    width="100%",
                ),
                padding="0.75rem 1rem",
                width="100%",
            ),
            
            spacing="0",
            width="100%",
            background="var(--gray-1)",
            border_radius="0 0 8px 8px",
            border="1px solid var(--gray-4)",
            border_top="none",
        ),
        
        rx.text(
            "Showing last 7 trades • Data synced from QuestDB",
            size="1",
            color="var(--gray-9)",
            margin_top="0.5rem",
        ),
        
        spacing="3",
        width="100%",
    )


def hedge_settings_tab_content() -> rx.Component:
    """Hedge settings tab showing position configuration (read-only)"""
    return rx.vstack(
        rx.hstack(
            rx.text(
                "Hedge Configuration",
                size="4",
                weight="bold",
            ),
            rx.spacer(),
            rx.badge(
                "Read-Only",
                color_scheme="gray",
                size="1",
            ),
            width="100%",
            align="center",
            margin_bottom="1rem",
        ),
        
        rx.text(
            "Data fetched from QuestDB",
            size="1",
            color="var(--gray-9)",
            margin_bottom="1rem",
        ),
        
        # Settings grid
        rx.vstack(
            rx.grid(
                # Row 1
                rx.vstack(
                    rx.hstack(
                        rx.text("Target Hedge Ratio", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Desired hedge ratio as percentage of position value.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("85%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Hedge Mode", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Static = Fixed ratio. Dynamic = Auto-adjusts based on market.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.badge("Dynamic (Balanced)", color_scheme="purple", size="1"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Tokens Hedged", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Which tokens in the position are being hedged.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("Both", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Rebalance Cooldown", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Minimum time between hedge adjustments.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("8h", size="2", weight="medium"),
                    spacing="1",
                ),
                columns="4",
                spacing="3",
                width="100%",
            ),
            
            rx.divider(margin_y="1rem"),
            
            rx.text("Advanced Parameters", size="3", weight="bold", margin_bottom="0.5rem"),
            
            rx.grid(
                # Row 2
                rx.vstack(
                    rx.hstack(
                        rx.text("Delta Drift", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="How much position delta can drift before rebalancing.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("38%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Down Threshold", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Price drop % that triggers hedge adjustment.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("6.5%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Bounce Threshold", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Price recovery % that triggers hedge reduction.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("3.8%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Lookback Hours", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="How far back to look for momentum before hedging.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("6h", size="2", weight="medium"),
                    spacing="1",
                ),
                columns="4",
                spacing="3",
                width="100%",
            ),
            
            rx.grid(
                # Row 3
                rx.vstack(
                    rx.hstack(
                        rx.text("Min Drift % Capital", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Minimum drift size before hedging (as % of position).",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("6%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Max Hedge Drift", size="1", color="gray"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Maximum allowed delta drift before forcing a hedge.",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text("50%", size="2", weight="medium"),
                    spacing="1",
                ),
                rx.spacer(),
                rx.spacer(),
                columns="4",
                spacing="3",
                width="100%",
                margin_top="0.5rem",
            ),
            
            spacing="2",
            width="100%",
            padding="1rem",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        
        spacing="3",
        width="100%",
    )


def activity_log_tab_content() -> rx.Component:
    """Activity log tab showing system events and logs"""
    return rx.vstack(
        rx.text(
            "Activity Log",
            size="4",
            weight="bold",
            margin_bottom="1rem",
        ),
        
        # Log entries
        rx.vstack(
            # Log 1
            rx.hstack(
                rx.text("10:15 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Info", color_scheme="blue", size="1"),
                rx.text(
                    "Position monitoring cycle started for ETH/WBTC pool",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 2
            rx.hstack(
                rx.text("10:15 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Success", color_scheme="green", size="1"),
                rx.text(
                    "Hedge position opened: -2.5 ETH at $2,845.30",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 3
            rx.hstack(
                rx.text("10:14 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Info", color_scheme="blue", size="1"),
                rx.text(
                    "Delta drift detected: 42% (threshold: 38%)",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 4
            rx.hstack(
                rx.text("08:42 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Success", color_scheme="green", size="1"),
                rx.text(
                    "Hedge adjustment executed: +0.8 ETH at $2,838.15",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 5
            rx.hstack(
                rx.text("08:41 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Warning", color_scheme="yellow", size="1"),
                rx.text(
                    "Price bounce detected: +4.2% recovery from local low",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 6
            rx.hstack(
                rx.text("06:20 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Info", color_scheme="blue", size="1"),
                rx.text(
                    "API health check: Hyperliquid connection stable",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 7
            rx.hstack(
                rx.text("02:30 AM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Info", color_scheme="blue", size="1"),
                rx.text(
                    "Position value updated: $68,429.85 (LP + Hedge)",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 8
            rx.hstack(
                rx.text("11:20 PM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Success", color_scheme="green", size="1"),
                rx.text(
                    "Rebalance completed: WBTC hedge adjusted -0.15 BTC",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 9
            rx.hstack(
                rx.text("11:18 PM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Warning", color_scheme="yellow", size="1"),
                rx.text(
                    "Funding rate spike detected: -0.08% (8hr rate)",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 10
            rx.hstack(
                rx.text("06:15 PM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Success", color_scheme="green", size="1"),
                rx.text(
                    "New hedge position opened: -1.2 WBTC at $51,180.50",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 11
            rx.hstack(
                rx.text("06:14 PM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Info", color_scheme="blue", size="1"),
                rx.text(
                    "Dynamic profile 'Balanced' parameters loaded",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            # Log 12
            rx.hstack(
                rx.text("02:30 PM", size="1", color="var(--gray-9)", min_width="70px"),
                rx.badge("Error", color_scheme="red", size="1"),
                rx.text(
                    "Temporary API timeout - retrying in 30s (attempt 1/3)",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            
            spacing="3",
            width="100%",
        ),
        
        rx.text(
            "Showing last 12 log entries • Real-time sync from QuestDB",
            size="1",
            color="var(--gray-9)",
            margin_top="1rem",
        ),
        
        spacing="3",
        width="100%",
    )


def position_activity_dialog() -> rx.Component:
    """Display activity/logs for a specific LP position with tabbed navigation"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header with title and close button
                rx.hstack(
                    rx.dialog.title("Position Activity"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="1",
                            on_click=LPPositionState.close_activity_dialog,
                        )
                    ),
                    width="100%",
                    align="center",
                ),
                
                # Tab navigation
                rx.hstack(
                    activity_tab_button("Trades", "trades", "arrow-left-right"),
                    activity_tab_button("Hedge Settings", "settings", "settings"),
                    activity_tab_button("Activity Log", "logs", "list"),
                    spacing="2",
                    width="100%",
                    margin_bottom="1.5rem",
                ),
                
                # Tab content
                rx.box(
                    rx.cond(
                        LPPositionState.activity_tab == "trades",
                        trades_tab_content(),
                    ),
                    rx.cond(
                        LPPositionState.activity_tab == "settings",
                        hedge_settings_tab_content(),
                    ),
                    rx.cond(
                        LPPositionState.activity_tab == "logs",
                        activity_log_tab_content(),
                    ),
                    width="100%",
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="900px",
            padding="2rem",
        ),
        open=LPPositionState.show_activity_dialog,
    )
