import reflex as rx
from ..lp_position_state import LPPositionState, LPPositionData
from ..config import AppConfig
from .position_chart import position_value_chart
from .position_activity import position_activity_dialog


def range_position_visual(position: LPPositionData) -> rx.Component:
    """Create visual representation of position within LP range - Metrix Finance style
    
    The bar represents the full LP range with bounds at the edges.
    Current price position is calculated from distance_to_lower_pct.
    Position = distance_to_lower / (distance_to_lower + distance_to_upper) * 100
    """
    
    return rx.cond(
        position.metrics.utilization_pct != None,
        rx.vstack(
            rx.hstack(
                rx.text("Range Position", size="1", color="gray", weight="medium"),
                rx.badge(
                    rx.cond(
                        (position.metrics.utilization_pct >= 0) & (position.metrics.utilization_pct <= 100),
                        "IN RANGE",
                        "OUT OF RANGE"
                    ),
                    color_scheme=rx.cond(
                        (position.metrics.utilization_pct >= 0) & (position.metrics.utilization_pct <= 100),
                        "green",
                        "red"
                    ),
                    variant="soft",
                    size="1",
                ),
                spacing="2",
                align_items="center",
            ),
            rx.box(
                rx.vstack(
                    # Custom range bar with dots (Metrix Finance style)
                    rx.box(
                        # Background bar
                        rx.box(
                            # Gradient bar background
                            rx.box(
                                width="100%",
                                height="6px",
                                background="linear-gradient(to right, rgba(239, 68, 68, 0.3), rgba(234, 179, 8, 0.3), rgba(34, 197, 94, 0.3), rgba(234, 179, 8, 0.3), rgba(239, 68, 68, 0.3))",
                                border_radius="3px",
                            ),
                            # Position dots container
                            rx.box(
                                # Lower bound dot (purple)
                                rx.box(
                                    width="10px",
                                    height="10px",
                                    border_radius="50%",
                                    background="rgba(168, 85, 247, 0.8)",
                                    border="2px solid rgba(168, 85, 247, 1)",
                                    position="absolute",
                                    left="0",
                                    top="-2px",
                                ),
                                # Current position dot (green if in range, red if out)
                                # Position calculated as: distance_to_lower / (distance_to_lower + distance_to_upper) * 100
                                rx.box(
                                    width="12px",
                                    height="12px",
                                    border_radius="50%",
                                    background=rx.cond(
                                        (position.metrics.utilization_pct >= 0) & (position.metrics.utilization_pct <= 100),
                                        "rgba(34, 197, 94, 0.9)",
                                        "rgba(239, 68, 68, 0.9)"
                                    ),
                                    border=rx.cond(
                                        (position.metrics.utilization_pct >= 0) & (position.metrics.utilization_pct <= 100),
                                        "2px solid rgba(34, 197, 94, 1)",
                                        "2px solid rgba(239, 68, 68, 1)"
                                    ),
                                    position="absolute",
                                    left=rx.cond(
                                        position.metrics.distance_to_lower_pct < 0,
                                        "-6px",
                                        rx.cond(
                                            position.metrics.distance_to_upper_pct < 0,
                                            "calc(100% - 6px)",
                                            f"calc({(position.metrics.distance_to_lower_pct / (position.metrics.distance_to_lower_pct + position.metrics.distance_to_upper_pct) * 100)}% - 6px)"
                                        )
                                    ),
                                    top="-3px",
                                    z_index="2",
                                ),
                                # Upper bound dot (purple)
                                rx.box(
                                    width="10px",
                                    height="10px",
                                    border_radius="50%",
                                    background="rgba(168, 85, 247, 0.8)",
                                    border="2px solid rgba(168, 85, 247, 1)",
                                    position="absolute",
                                    right="0",
                                    top="-2px",
                                ),
                                position="relative",
                                width="100%",
                                height="6px",
                            ),
                            position="relative",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.5rem 0",
                    ),
                    spacing="1",
                    width="100%",
                ),
                width="100%",
            ),
            # Distance to bounds
            rx.hstack(
                rx.text(
                    f"Lower: {position.metrics.distance_to_lower_pct:.1f}%",
                    size="1",
                    color="gray",
                ),
                rx.text("•", size="1", color="gray"),
                rx.text(
                    f"Upper: {position.metrics.distance_to_upper_pct:.1f}%",
                    size="1",
                    color="gray",
                ),
                spacing="1",
                justify="center",
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        rx.vstack(
            rx.text("Range Position", size="1", color="gray", weight="medium"),
            rx.text("N/A", size="2", color="gray"),
            spacing="1",
            align_items="start",
        ),
    )


def lp_position_card(position: LPPositionData) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(position.position_name, size="4", weight="bold"),
                    rx.hstack(
                        rx.badge(
                            position.protocol.replace("_", " ").title() + " (" + position.network.title() + ")",
                            color_scheme="gray",
                            variant="soft"
                        ),
                        rx.badge(
                            rx.cond(position.hedge_enabled, "Hedge Active", "Hedge Inactive"),
                            color_scheme=rx.cond(position.hedge_enabled, "green", "red"),
                            variant="surface",
                        ),
                        rx.badge(
                            rx.cond(position.use_dynamic_hedging, "Dynamic", "Static"),
                            color_scheme=rx.cond(position.use_dynamic_hedging, "purple", "blue"),
                            variant="soft",
                        ),
                        spacing="2",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.hstack(
                        rx.button(
                            "Activity",
                            size="2",
                            variant="soft",
                            color_scheme="purple",
                            on_click=lambda: LPPositionState.open_activity_dialog(position.position_config_id),
                        ),
                        rx.button(
                            "View Chart",
                            size="2",
                            variant="soft",
                            color_scheme="green",
                            on_click=lambda: LPPositionState.load_chart_data(position.position_config_id, 24),
                        ),
                        rx.button(
                            rx.icon("eye", size=16),
                            "View Settings",
                            size="2",
                            variant="soft",
                            color_scheme="gray",
                            on_click=lambda: LPPositionState.open_settings_dialog(position.position_config_id),
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        rx.button(
                            "Edit",
                            size="2",
                            variant="soft",
                            color_scheme="blue",
                            on_click=lambda: LPPositionState.edit_position(position.id),
                            loading=LPPositionState.loading_position_id == position.id,
                        ),
                        rx.button(
                            "Delete",
                            size="2",
                            variant="soft",
                            color_scheme="red",
                            on_click=lambda: LPPositionState.open_delete_dialog(position.id),
                            loading=LPPositionState.loading_position_id == position.id,
                        ),
                        spacing="2",
                        justify="end",
                        width="100%",
                    ),
                    spacing="2",
                    align_items="end",
                ),
                width="100%",
                align="center",
            ),
            
            rx.divider(margin_top="0.75rem", margin_bottom="0.75rem"),
            
            rx.grid(
                # Row 1, Col 1: Total Position
                rx.vstack(
                    rx.hstack(
                        rx.text("Total Position", size="1", color="gray", weight="medium"),
                        rx.tooltip(
                            rx.icon("info", size=12, color="gray"),
                            content="Total Position = LP Position (including fees) + Trading Account Balance",
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    rx.text(position.total_value_formatted, size="6", weight="bold", color="green"),
                    rx.hstack(
                        rx.text("LP:", size="1", color="gray"),
                        rx.text(position.position_value_formatted, size="2", weight="medium"),
                        rx.cond(
                            position.api_account_value > 0,
                            rx.hstack(
                                rx.text("•", size="1", color="gray"),
                                rx.text("Hedge:", size="1", color="gray"),
                                rx.text(f"${position.api_account_value:,.2f}", size="2", weight="medium"),
                                spacing="1",
                            ),
                        ),
                        spacing="1",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                # Row 1, Col 2: PnL
                rx.vstack(
                    rx.text("PnL", size="1", color="gray", weight="medium"),
                    rx.cond(
                        position.metrics.current_pnl != None,
                        rx.vstack(
                            # Total PnL with percentage
                            rx.hstack(
                                rx.text(
                                    rx.cond(
                                        position.metrics.current_pnl >= 0,
                                        f"+${position.metrics.current_pnl:,.2f}",
                                        f"-${abs(position.metrics.current_pnl):,.2f}",
                                    ),
                                    size="4",
                                    weight="bold",
                                    color=rx.cond(position.metrics.current_pnl >= 0, "green", "red"),
                                ),
                                rx.text(
                                    rx.cond(
                                        position.metrics.pnl_percentage >= 0,
                                        f"(+{position.metrics.pnl_percentage:.1f}%)",
                                        f"({position.metrics.pnl_percentage:.1f}%)",
                                    ),
                                    size="2",
                                    color=rx.cond(position.metrics.pnl_percentage >= 0, "green", "red"),
                                ),
                                spacing="1",
                                align_items="baseline",
                            ),
                            # LP and Hedge breakdown
                            rx.hstack(
                                rx.text("LP:", size="1", color="gray"),
                                rx.text(
                                    rx.cond(
                                        position.metrics.lp_pnl_usd >= 0,
                                        f"+${position.metrics.lp_pnl_usd:,.2f}",
                                        f"-${abs(position.metrics.lp_pnl_usd):,.2f}",
                                    ),
                                    size="1",
                                    weight="medium",
                                    color=rx.cond(position.metrics.lp_pnl_usd >= 0, "green", "red"),
                                ),
                                rx.text(
                                    rx.cond(
                                        position.metrics.lp_pnl_pct >= 0,
                                        f"(+{position.metrics.lp_pnl_pct:.1f}%)",
                                        f"({position.metrics.lp_pnl_pct:.1f}%)",
                                    ),
                                    size="1",
                                    color=rx.cond(position.metrics.lp_pnl_pct >= 0, "green", "red"),
                                ),
                                rx.text("•", size="1", color="gray"),
                                rx.text("Hedge:", size="1", color="gray"),
                                rx.text(
                                    rx.cond(
                                        position.metrics.hedge_pnl_usd >= 0,
                                        f"+${position.metrics.hedge_pnl_usd:,.2f}",
                                        f"-${abs(position.metrics.hedge_pnl_usd):,.2f}",
                                    ),
                                    size="1",
                                    weight="medium",
                                    color=rx.cond(position.metrics.hedge_pnl_usd >= 0, "green", "red"),
                                ),
                                rx.text(
                                    rx.cond(
                                        position.metrics.hedge_pnl_pct >= 0,
                                        f"(+{position.metrics.hedge_pnl_pct:.1f}%)",
                                        f"({position.metrics.hedge_pnl_pct:.1f}%)",
                                    ),
                                    size="1",
                                    color=rx.cond(position.metrics.hedge_pnl_pct >= 0, "green", "red"),
                                ),
                                spacing="1",
                            ),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.text("N/A", size="2", color="gray"),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                # Row 2, Col 1: Impermanent Loss
                rx.vstack(
                    rx.text("Impermanent Loss", size="1", color="gray", weight="medium"),
                    rx.cond(
                        position.metrics.il_usd != None,
                        rx.vstack(
                            rx.text(
                                rx.cond(
                                    position.metrics.il_usd >= 0,
                                    f"+${position.metrics.il_usd:,.2f}",
                                    f"-${abs(position.metrics.il_usd):,.2f}",
                                ),
                                size="4",
                                weight="bold",
                                color=rx.cond(position.metrics.il_usd >= 0, "green", "red"),
                            ),
                            rx.text(
                                rx.cond(
                                    position.metrics.il_pct >= 0,
                                    f"+{position.metrics.il_pct:.1f}%",
                                    f"{position.metrics.il_pct:.1f}%",
                                ),
                                size="2",
                                color=rx.cond(position.metrics.il_pct >= 0, "green", "red"),
                            ),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.text("N/A", size="2", color="gray"),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                # Row 2, Col 2: Range Position
                range_position_visual(position),
                # Row 3, Col 1: APR
                rx.vstack(
                    rx.text("APR", size="1", color="gray", weight="medium"),
                    rx.cond(
                        position.metrics.apr != None,
                        rx.vstack(
                            rx.text(
                                rx.cond(
                                    position.metrics.apr >= 0,
                                    f"+{position.metrics.apr:,.1f}%",
                                    f"{position.metrics.apr:,.1f}%",
                                ),
                                size="4",
                                weight="bold",
                                color=rx.cond(position.metrics.apr >= 0, "green", "red"),
                            ),
                            rx.text(
                                f"{position.metrics.position_age_days} days",
                                size="1",
                                color="gray",
                            ),
                            spacing="1",
                            align_items="start",
                        ),
                        rx.text("N/A", size="2", color="gray"),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                # Row 3, Col 2: Empty (for future metric)
                rx.box(),
                columns="2",
                spacing="4",
                width="100%",
            ),
            
            rx.box(height="0.5rem"),
            
            # Status row
            rx.hstack(
                rx.text("Last Check:", size="1", color="gray"),
                rx.text(
                    position.last_hedge_execution,
                    size="1",
                    weight="medium",
                    color=rx.cond(position.last_hedge_execution == "Never", "gray", "green"),
                ),
                spacing="1",
                align_items="center",
            ),
            
            rx.box(height="0.5rem"),
            
            rx.grid(
                rx.vstack(
                    rx.text("Pair", size="1", color="gray"),
                    rx.text(rx.cond((position.token0_symbol != "") & (position.token1_symbol != ""), position.token0_symbol + "/" + position.token1_symbol, "-"), size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("NFT ID", size="1", color="gray"),
                    rx.text(position.nft_id, size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Trading Account", size="1", color="gray"),
                    rx.text(rx.cond(position.api_key_name != "", position.api_key_name, "Not assigned"), size="2", weight="medium"),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("Network", size="1", color="gray"),
                    rx.text(position.network.title(), size="2", weight="medium"),
                    spacing="1",
                ),
                columns="4",
                spacing="4",
                width="100%",
            ),
            
            rx.cond(
                position.notes != "",
                rx.box(
                    rx.text("Notes: " + position.notes, size="1", color="gray", font_style="italic"),
                    margin_top="0.75rem",
                    padding_top="0.5rem",
                    border_top="1px dashed var(--gray-4)",
                    width="100%",
                ),
            ),
            
            spacing="1",
            width="100%",
        ),
        width="100%",
        size="3",
    )


def lp_positions_component() -> rx.Component:
    return rx.fragment(
        # Toast provider for notifications
        rx.toast.provider(),
        
        # Delete confirmation dialog
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("⚠️ Delete LP Position"),
                rx.alert_dialog.description(
                    "Are you sure you want to delete this LP position? This action cannot be undone.",
                    size="3",
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=LPPositionState.cancel_delete,
                        ),
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Delete",
                            variant="solid",
                            color_scheme="red",
                            on_click=LPPositionState.delete_position,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                ),
            ),
            open=LPPositionState.show_delete_dialog,
        ),
        
        # Position activity dialog
        position_activity_dialog(),
        
        # Position value chart dialog
        position_value_chart(),
        
        # Auto-refresh position status every 60 seconds
        rx.moment(
            interval=60000,  # 60 seconds
            on_change=LPPositionState.refresh_position_status,
        ),
        
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.heading("LP Positions", size="6"),
                    rx.spacer(),
                    rx.button(
                        rx.icon("refresh-cw", size=16),
                        "Refresh",
                        size="2",
                        variant="soft",
                        color_scheme="blue",
                        on_click=LPPositionState.load_positions,
                        loading=LPPositionState.is_loading,
                    ),
                    width="100%",
                    align="center",
                    margin_bottom="1rem",
                ),
                
                rx.cond(
                    LPPositionState.error_message != "",
                    rx.callout(
                        LPPositionState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                        margin_bottom="1rem",
                    ),
                ),
                
                rx.cond(
                    LPPositionState.success_message != "",
                    rx.callout(
                        LPPositionState.success_message,
                        icon="check",
                        color_scheme="green",
                        role="status",
                        margin_bottom="1rem",
                    ),
                ),
                
                rx.cond(
                    LPPositionState.is_loading,
                    rx.spinner(size="3"),
                    rx.vstack(
                        rx.cond(
                            LPPositionState.lp_positions.length() > 0,
                            rx.grid(
                                rx.foreach(LPPositionState.lp_positions, lp_position_card),
                                columns="2",
                                spacing="3",
                                width="100%",
                            ),
                            rx.box(
                                rx.text(
                                    "No LP positions added yet. Add your first position below.",
                                    size="2",
                                    color="gray",
                                ),
                                padding="2rem",
                                text_align="center",
                            ),
                        ),
                        width="100%",
                    ),
                ),
            ),
        ),
        
        rx.divider(margin_top="2rem", margin_bottom="2rem"),
        
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading(
                rx.cond(
                    LPPositionState.is_editing,
                    "Edit LP Position",
                    "Add New LP Position",
                ),
                size="5",
                margin_bottom="1rem",
            ),
            
            rx.cond(
                LPPositionState.is_editing,
                rx.button(
                    "Cancel Edit",
                    size="2",
                    variant="soft",
                    color_scheme="gray",
                    on_click=LPPositionState.clear_form,
                    margin_bottom="1rem",
                ),
            ),
            
            rx.cond(
                ~LPPositionState.show_confirmation,
                # Step 1: Simple form to fetch position data
                rx.form(
                    rx.vstack(
                        rx.vstack(
                            rx.text("Protocol", size="2", weight="bold"),
                            rx.select.root(
                                rx.select.trigger(placeholder="Select protocol"),
                                rx.select.content(
                                    rx.select.item("Uniswap V3", value="uniswap_v3"),
                                ),
                                name="protocol",
                                default_value=LPPositionState.protocol,
                                max_width="250px",
                            ),
                            rx.text(
                                "The DEX protocol (more protocols coming soon)",
                                size="1",
                                color="gray",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.vstack(
                            rx.text("Network", size="2", weight="bold"),
                            rx.select(
                                ["ethereum", "arbitrum", "base", "polygon", "optimism"],
                                placeholder="Select network",
                                name="network",
                                default_value=LPPositionState.network,
                                max_width="250px",
                            ),
                            rx.text(
                                "The blockchain network where your LP position exists",
                                size="1",
                                color="gray",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.vstack(
                            rx.text("NFT ID", size="2", weight="bold"),
                            rx.input(
                                placeholder="e.g., 123456",
                                name="nft_id",
                                type="text",
                                required=True,
                                max_width="200px",
                                default_value=LPPositionState.nft_id,
                            ),
                            rx.text(
                                "The NFT position ID for the selected protocol",
                                size="1",
                                color="gray",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.button(
                            "Fetch Position Data",
                            type="submit",
                            size="3",
                            variant="soft",
                            color_scheme="blue",
                            width="100%",
                            loading=LPPositionState.is_fetching,
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=LPPositionState.fetch_position_data_handler,
                    reset_on_submit=False,
                    width="100%",
                ),
                
                # Step 2: Show fetched data and allow confirmation/editing
                rx.vstack(
                    # Position Details - Metadata Only
                    rx.card(
                        rx.vstack(
                            rx.heading("Position Details", size="4", margin_bottom="1rem"),
                            
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Protocol:", weight="bold", size="2"),
                                    rx.text(LPPositionState.protocol.replace("_", " ").title(), size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Network:", weight="bold", size="2"),
                                    rx.text(LPPositionState.network.title(), size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("NFT ID:", weight="bold", size="2"),
                                    rx.text(LPPositionState.nft_id, size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Pair:", weight="bold", size="2"),
                                    rx.text(LPPositionState.token0_symbol + "/" + LPPositionState.token1_symbol, size="2"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Pool:", weight="bold", size="2"),
                                    rx.text(LPPositionState.pool_address, size="2", color="gray"),
                                    rx.icon_button(
                                        rx.icon("clipboard", size=14),
                                        size="1",
                                        variant="ghost",
                                        on_click=rx.set_clipboard(LPPositionState.pool_address),
                                    ),
                                    spacing="2",
                                ),
                                spacing="2",
                                align_items="start",
                                width="100%",
                            ),
                            
                            spacing="3",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    
                    # LP Position & Value - All Financial Data
                    rx.cond(
                        LPPositionState.fetched_position_data.get("hl_price_available", False),
                        rx.card(
                            rx.vstack(
                                rx.text("💰 LP Position & Value", size="4", weight="bold"),
                                rx.divider(),
                                
                                # Price Range
                                rx.hstack(
                                    rx.text("Price Range:", weight="bold", size="2"),
                                    rx.cond(
                                        LPPositionState.fetched_position_data.get("hl_price_available", False),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('pa_usd', 0):.2f} - ${LPPositionState.fetched_position_data.get('pb_usd', 0):.2f}", size="2"),
                                        rx.text(f"{LPPositionState.fetched_position_data.get('pa', 0):.6f} - {LPPositionState.fetched_position_data.get('pb', 0):.6f} (ratio)", size="2", color="gray"),
                                    ),
                                    rx.cond(
                                        LPPositionState.fetched_position_data.get("in_range", False),
                                        rx.badge("In Range", color_scheme="green", size="1"),
                                        rx.badge("Out of Range", color_scheme="red", size="1"),
                                    ),
                                    spacing="2",
                                ),
                                
                                rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                
                                # Current Prices
                                rx.text("Current Prices:", weight="bold", size="2"),
                                rx.hstack(
                                    rx.text(f"{LPPositionState.token0_symbol}: ${LPPositionState.fetched_position_data.get('token0_price_usd', 0):.2f}", size="2"),
                                    rx.text("|", color="gray"),
                                    rx.text(f"{LPPositionState.token1_symbol}: ${LPPositionState.fetched_position_data.get('token1_price_usd', 0):.2f}", size="2"),
                                    spacing="2",
                                ),
                                
                                rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                
                                # Position Breakdown
                                rx.text("Position:", weight="bold", size="2"),
                                rx.vstack(
                                    rx.hstack(
                                        rx.text(f"{LPPositionState.token0_symbol}:", weight="bold", size="2", min_width="60px"),
                                        rx.text(f"{LPPositionState.fetched_position_data.get('token0_amount', 0):.6f}", size="2", min_width="120px", text_align="right"),
                                        rx.text("@", color="gray", size="2", min_width="20px", text_align="center"),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('token0_price_usd', 0):.2f}", size="2", min_width="80px", text_align="right"),
                                        rx.text("=", color="gray", size="2", min_width="20px", text_align="center"),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('token0_amount_usd', 0):,.2f}", size="2", color="green", min_width="100px", text_align="right"),
                                        rx.text(f"({LPPositionState.fetched_position_data.get('token0_pct', 0):.1f}%)", size="2", color="gray", min_width="60px"),
                                        spacing="2",
                                    ),
                                    rx.hstack(
                                        rx.text(f"{LPPositionState.token1_symbol}:", weight="bold", size="2", min_width="60px"),
                                        rx.text(f"{LPPositionState.fetched_position_data.get('token1_amount', 0):.6f}", size="2", min_width="120px", text_align="right"),
                                        rx.text("@", color="gray", size="2", min_width="20px", text_align="center"),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('token1_price_usd', 0):.2f}", size="2", min_width="80px", text_align="right"),
                                        rx.text("=", color="gray", size="2", min_width="20px", text_align="center"),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('token1_amount_usd', 0):,.2f}", size="2", color="green", min_width="100px", text_align="right"),
                                        rx.text(f"({LPPositionState.fetched_position_data.get('token1_pct', 0):.1f}%)", size="2", color="gray", min_width="60px"),
                                        spacing="2",
                                    ),
                                    spacing="1",
                                    align_items="start",
                                ),
                                
                                rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                
                                # Total LP Value
                                rx.hstack(
                                    rx.text("Total LP Value:", weight="bold", size="3"),
                                    rx.text(f"${LPPositionState.fetched_position_data.get('position_value_usd', 0):,.2f}", size="3", weight="bold", color="green"),
                                    spacing="2",
                                ),
                                
                                spacing="3",
                                align_items="start",
                                width="100%",
                            ),
                            width="100%",
                        ),
                    ),
                    
                    # Hedging Balance Recommendation Card
                    rx.cond(
                        LPPositionState.fetched_position_data.get("hl_price_available", False),
                        rx.card(
                            rx.vstack(
                                rx.hstack(
                                    rx.text("💡", size="5"),
                                    rx.text("Hedging Balance Recommendation", size="4", weight="bold"),
                                    spacing="2",
                                    align_items="center",
                                ),
                                rx.divider(),
                                rx.vstack(
                                    rx.text("Recommended balance for your Hyperliquid account:", size="2"),
                                    rx.text(
                                        f"${LPPositionState.recommended_balance_range['min']:,.0f} - ${LPPositionState.recommended_balance_range['max']:,.0f}",
                                        size="5",
                                        weight="bold",
                                        color="blue",
                                    ),
                                    rx.text(
                                        LPPositionState.recommended_balance_range['description'],
                                        size="1",
                                        color="gray",
                                    ),
                                    rx.text(
                                        "Ensure your account is funded before enabling hedging.",
                                        size="2",
                                        weight="medium",
                                        color="orange",
                                    ),
                                    spacing="2",
                                    align_items="start",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            style={"background": "var(--accent-2)", "border": "2px solid var(--accent-6)"},
                            width="100%",
                        ),
                    ),
                    
                    # Hedge Configuration Section
                    rx.cond(
                        LPPositionState.fetched_position_data.get("hl_price_available", False),
                        rx.vstack(
                            rx.divider(margin_top="1rem", margin_bottom="1rem"),
                            rx.text("⚙️ Hedge Configuration", size="4", weight="bold"),
                            
                            rx.card(
                                rx.vstack(
                                    rx.hstack(
                                        rx.checkbox(
                                            checked=LPPositionState.hedge_enabled,
                                            on_change=LPPositionState.toggle_hedge_enabled,
                                        ),
                                        rx.text("Enable Hedging", size="3", weight="bold"),
                                        spacing="2",
                                        align_items="center",
                                    ),
                                    
                                    rx.vstack(
                                        rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                            
                                            rx.vstack(
                                                rx.text("Trading Account", size="2", weight="bold"),
                                                rx.select(
                                                    LPPositionState.available_wallets,
                                                    value=LPPositionState.selected_hedge_wallet,
                                                    on_change=LPPositionState.set_hedge_wallet,
                                                    placeholder="Select trading account for hedging",
                                                    on_mount=LPPositionState.load_wallets,
                                                ),
                                                rx.text(
                                                    "Hyperliquid wallet for hedge trades",
                                                    size="1",
                                                    color="gray",
                                                ),
                                                # Balance display
                                                rx.cond(
                                                    LPPositionState.selected_hedge_wallet != "",
                                                    rx.cond(
                                                        LPPositionState.balance_loading,
                                                        rx.hstack(
                                                            rx.spinner(size="1"),
                                                            rx.text("Loading balance...", size="1", color="gray"),
                                                            spacing="2",
                                                            align_items="center",
                                                        ),
                                                        rx.cond(
                                                            LPPositionState.balance_error != "",
                                                            rx.text(
                                                                LPPositionState.balance_error,
                                                                size="1",
                                                                color="red",
                                                            ),
                                                            rx.cond(
                                                                LPPositionState.selected_wallet_balance > 0,
                                                                rx.vstack(
                                                                    rx.hstack(
                                                                        rx.text("Account Value:", size="1", weight="bold"),
                                                                        rx.text(f"${LPPositionState.selected_wallet_balance:,.2f}", size="1", color="green"),
                                                                        spacing="2",
                                                                    ),
                                                                    rx.hstack(
                                                                        rx.text("Available:", size="1", weight="bold"),
                                                                        rx.text(f"${LPPositionState.selected_wallet_available:,.2f}", size="1", color="blue"),
                                                                        spacing="2",
                                                                    ),
                                                                    spacing="0",
                                                                    align_items="start",
                                                                ),
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                                # Balance status indicator
                                                rx.cond(
                                                    LPPositionState.balance_status_for_position["status"] == "success",
                                                    rx.text(
                                                        LPPositionState.balance_status_for_position["message"],
                                                        size="1",
                                                        color="green",
                                                        weight="bold",
                                                    ),
                                                    rx.cond(
                                                        LPPositionState.balance_status_for_position["status"] == "insufficient",
                                                        rx.text(
                                                            LPPositionState.balance_status_for_position["message"],
                                                            size="1",
                                                            color="red",
                                                            weight="bold",
                                                        ),
                                                        rx.cond(
                                                            LPPositionState.balance_status_for_position["status"] == "warning",
                                                            rx.text(
                                                                LPPositionState.balance_status_for_position["message"],
                                                                size="1",
                                                                color="orange",
                                                            ),
                                                        ),
                                                    ),
                                                ),
                                                spacing="1",
                                                width="100%",
                                            ),
                                            
                                            rx.vstack(
                                                rx.text("Hedge Strategy Type", size="2", weight="bold"),
                                                rx.select(
                                                    ["Static", "Dynamic"],
                                                    value=LPPositionState.hedge_strategy_type_display,
                                                    on_change=LPPositionState.set_hedge_strategy_type,
                                                    placeholder="Select strategy type",
                                                ),
                                                rx.cond(
                                                    LPPositionState.use_dynamic_hedging,
                                                    rx.text("Dynamic hedging adjusts ratio based on market conditions", size="1", color="blue"),
                                                    rx.text("Static hedge maintains a fixed ratio", size="1", color="gray"),
                                                ),
                                                spacing="1",
                                                width="100%",
                                            ),
                                            
                                            # Conditional: Static Hedge Ratio Selection
                                            rx.cond(
                                                ~LPPositionState.use_dynamic_hedging,
                                                rx.vstack(
                                                    rx.text("Hedge Ratio", size="2", weight="bold"),
                                                    rx.select(
                                                        ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
                                                        value=LPPositionState.hedge_ratio_display,
                                                        on_change=LPPositionState.set_hedge_ratio,
                                                        placeholder="Select hedge ratio",
                                                    ),
                                                    rx.text(f"Hedge at {LPPositionState.hedge_ratio}% of position exposure", size="1", color="gray"),
                                                    spacing="1",
                                                    width="100%",
                                                ),
                                            ),
                                            
                                            # Dynamic Hedging Configuration
                                            rx.cond(
                                                LPPositionState.use_dynamic_hedging,
                                                rx.vstack(
                                                    rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                                    rx.text("🎯 Dynamic Hedging Profile", size="2", weight="bold", color="blue"),
                                                    
                                                    rx.vstack(
                                                        rx.text("Profile", size="2", weight="bold"),
                                                        rx.radio_group.root(
                                                            rx.vstack(
                                                                # Balanced
                                                                rx.hstack(
                                                                    rx.radio_group.item(value="balanced"),
                                                                    rx.vstack(
                                                                        rx.hstack(
                                                                            rx.text("Balanced", size="2", weight="bold"),
                                                                            rx.badge("Default", color_scheme="blue", variant="soft", size="1"),
                                                                            spacing="2",
                                                                        ),
                                                                        rx.text(
                                                                            "Recommended for most users. Dynamically adjusts hedging between 45%–100% based on market conditions.",
                                                                            size="1",
                                                                            color="gray",
                                                                        ),
                                                                        spacing="1",
                                                                        align_items="start",
                                                                    ),
                                                                    spacing="3",
                                                                    align_items="start",
                                                                    width="100%",
                                                                ),
                                                                # Moderate Bullish
                                                                rx.hstack(
                                                                    rx.radio_group.item(value="moderate_bullish"),
                                                                    rx.vstack(
                                                                        rx.text("Moderate Bullish", size="2", weight="bold"),
                                                                        rx.text(
                                                                            "Leans slightly bullish. Keeps more exposure to the volatile asset during trends.",
                                                                            size="1",
                                                                            color="gray",
                                                                        ),
                                                                        spacing="1",
                                                                        align_items="start",
                                                                    ),
                                                                    spacing="3",
                                                                    align_items="start",
                                                                    width="100%",
                                                                ),
                                                                # Aggressive Bullish
                                                                rx.hstack(
                                                                    rx.radio_group.item(value="aggressive_bullish"),
                                                                    rx.vstack(
                                                                        rx.text("Aggressive Bullish", size="2", weight="bold"),
                                                                        rx.text(
                                                                            "Strong bullish tilt. Significantly under-hedges to maximize potential gains.",
                                                                            size="1",
                                                                            color="gray",
                                                                        ),
                                                                        spacing="1",
                                                                        align_items="start",
                                                                    ),
                                                                    spacing="3",
                                                                    align_items="start",
                                                                    width="100%",
                                                                ),
                                                                # Moderate Bearish
                                                                rx.hstack(
                                                                    rx.radio_group.item(value="moderate_bearish"),
                                                                    rx.vstack(
                                                                        rx.text("Moderate Bearish", size="2", weight="bold"),
                                                                        rx.text(
                                                                            "Leans defensive. Increases hedging during uncertain markets.",
                                                                            size="1",
                                                                            color="gray",
                                                                        ),
                                                                        spacing="1",
                                                                        align_items="start",
                                                                    ),
                                                                    spacing="3",
                                                                    align_items="start",
                                                                    width="100%",
                                                                ),
                                                                # Full Protection
                                                                rx.hstack(
                                                                    rx.radio_group.item(value="full_protection"),
                                                                    rx.vstack(
                                                                        rx.text("Full Protection", size="2", weight="bold"),
                                                                        rx.text(
                                                                            "Maximum safety mode. Stays near 100% hedged in almost all conditions.",
                                                                            size="1",
                                                                            color="gray",
                                                                        ),
                                                                        spacing="1",
                                                                        align_items="start",
                                                                    ),
                                                                    spacing="3",
                                                                    align_items="start",
                                                                    width="100%",
                                                                ),
                                                                spacing="2",
                                                                width="100%",
                                                            ),
                                                            value=LPPositionState.dynamic_profile,
                                                            on_change=LPPositionState.set_dynamic_profile,
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    
                                                    spacing="2",
                                                    width="100%",
                                                ),
                                            ),
                                            
                                            # Advanced Parameters for Static Hedging
                                            rx.cond(
                                                ~LPPositionState.use_dynamic_hedging,
                                                rx.vstack(
                                                    rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                                    rx.text("⚙️ Advanced Parameters", size="2", weight="bold"),
                                                    rx.hstack(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Rebalance Cooldown", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="Minimum time to wait between hedge rebalances. Prevents over-trading. Lower = more responsive but higher fees. Higher = fewer trades but may miss optimal rebalances.",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["1 hour", "2 hours", "4 hours", "6 hours", "8 hours", "12 hours", "24 hours", "36 hours"],
                                                                value=LPPositionState.rebalance_cooldown_display,
                                                                on_change=LPPositionState.set_rebalance_cooldown,
                                                                placeholder="Select cooldown",
                                                            ),
                                                            rx.text("Minimum time between rebalances", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Delta Drift Threshold", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="How much your position delta can drift before triggering a rebalance. Low = rebalance often (tight hedge). High = rebalance rarely (loose hedge). Medium is recommended for most positions.",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["Low (14%)", "Medium (38%)", "High (58%)", "Very High (80%)"],
                                                                value="Medium (38%)",
                                                                on_change=LPPositionState.set_delta_drift_threshold,
                                                                placeholder="Select threshold",
                                                            ),
                                                            rx.text("Sensitivity to position drift", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    rx.hstack(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Down Threshold", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="Price drop % that triggers hedge adjustment. Used to detect significant downward moves. Aggressive = react to small moves. Conservative = wait for larger moves before adjusting.",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["Aggressive (-3.2%)", "Moderate (-5.5%)", "Conservative (-6.5%)", "Very Conservative (-15%)"],
                                                                value="Conservative (-6.5%)",
                                                                on_change=LPPositionState.set_down_threshold,
                                                                placeholder="Select threshold",
                                                            ),
                                                            rx.text("Trigger for downward moves", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Bounce Threshold", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="Price recovery % after a drop that triggers hedge reduction. Detects bounce-back moves. Aggressive = reduce hedge quickly on small bounces. Conservative = wait for stronger recovery.",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["Aggressive (-1.9%)", "Moderate (-3.2%)", "Conservative (-3.8%)", "Very Conservative (-7.5%)"],
                                                                value="Conservative (-3.8%)",
                                                                on_change=LPPositionState.set_bounce_threshold,
                                                                placeholder="Select threshold",
                                                            ),
                                                            rx.text("Trigger for bounce recovery", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    
                                                    rx.hstack(
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Lookback Hours", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="Pullback filter: How far back to look for momentum before hedging. Conservative=12h (more forgiving of trends), Balanced=6h, Aggressive=4h (quicker reaction)",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["Aggressive (4h)", "Balanced (6h)", "Conservative (12h)"],
                                                                value="Balanced (6h)",
                                                                on_change=LPPositionState.set_lookback_hours,
                                                                placeholder="Select lookback",
                                                            ),
                                                            rx.text("Momentum analysis window", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        rx.vstack(
                                                            rx.hstack(
                                                                rx.text("Min Drift % of Capital", size="1"),
                                                                rx.tooltip(
                                                                    rx.icon("info", size=14, color="gray"),
                                                                    content="Safety: Minimum drift size before hedging (as % of position). Conservative=10% (fewer tiny trades), Balanced=6%, Aggressive=4% (capture more small moves)",
                                                                ),
                                                                spacing="1",
                                                                align_items="center",
                                                            ),
                                                            rx.select(
                                                                ["Aggressive (4%)", "Balanced (6%)", "Conservative (10%)"],
                                                                value="Balanced (6%)",
                                                                on_change=LPPositionState.set_drift_min_pct_of_capital,
                                                                placeholder="Select min drift",
                                                            ),
                                                            rx.text("Minimum position size threshold", size="1", color="gray"),
                                                            spacing="1",
                                                            width="100%",
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    
                                                    rx.vstack(
                                                        rx.hstack(
                                                            rx.text("Max Hedge Drift %", size="1"),
                                                            rx.tooltip(
                                                                rx.icon("info", size=14, color="gray"),
                                                                content="Safety: Maximum allowed delta drift before forcing a hedge. Conservative=70% (more drift allowed), Balanced=50%, Aggressive=40% (more frequent protection)",
                                                            ),
                                                            spacing="1",
                                                            align_items="center",
                                                        ),
                                                        rx.select(
                                                            ["Aggressive (40%)", "Balanced (50%)", "Conservative (70%)"],
                                                            value="Balanced (50%)",
                                                            on_change=LPPositionState.set_max_hedge_drift_pct,
                                                            placeholder="Select max drift",
                                                        ),
                                                        rx.text("Maximum drift before forced hedge", size="1", color="gray"),
                                                        spacing="1",
                                                        width="100%",
                                                    ),
                                                    
                                                    spacing="2",
                                                    width="100%",
                                                ),
                                            ),
                                            
                                            rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                            
                                            rx.vstack(
                                                rx.text("📊 Estimated Hedges", size="2", weight="bold", color="blue"),
                                                rx.cond(
                                                    LPPositionState.use_dynamic_hedging,
                                                    rx.text(
                                                        "Not available with dynamic hedging",
                                                        size="2",
                                                        color="gray",
                                                        font_style="italic",
                                                    ),
                                                    rx.vstack(
                                                        rx.cond(
                                                            LPPositionState.hedge_token0,
                                                            rx.hstack(
                                                                rx.text(f"{LPPositionState.token0_symbol} Short:", weight="bold", size="2"),
                                                                rx.text(f"{LPPositionState.estimated_hedge_token0:.6f}", size="2", color="orange"),
                                                                spacing="2",
                                                            ),
                                                        ),
                                                        rx.cond(
                                                            LPPositionState.hedge_token1,
                                                            rx.hstack(
                                                                rx.text(f"{LPPositionState.token1_symbol} Short:", weight="bold", size="2"),
                                                                rx.text(f"{LPPositionState.estimated_hedge_token1:.6f}", size="2", color="orange"),
                                                                spacing="2",
                                                            ),
                                                        ),
                                                        rx.text(
                                                            f"Opens {LPPositionState.hedge_ratio}% hedge shorts on selected assets",
                                                            size="1",
                                                            color="gray",
                                                        ),
                                                        spacing="1",
                                                        width="100%",
                                                    ),
                                                ),
                                                spacing="1",
                                                width="100%",
                                            ),
                                            
                                            spacing="3",
                                            width="100%",
                                        ),
                                    
                                    spacing="2",
                                    width="100%",
                                ),
                                width="100%",
                            ),
                            
                            spacing="2",
                            width="100%",
                        ),
                    ),
                    
                    rx.vstack(
                        rx.text("Position Name", size="2", weight="bold"),
                        rx.input(
                            placeholder="e.g., ETH/USDC Main Position",
                            value=LPPositionState.position_name,
                            on_change=LPPositionState.set_position_name,
                            width="100%",
                        ),
                        rx.text(
                            "You can customize the position name",
                            size="1",
                            color="gray",
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    
                    rx.vstack(
                        rx.text("Notes (Optional)", size="2", weight="bold"),
                        rx.text_area(
                            placeholder="Any additional notes about this position",
                            value=LPPositionState.notes,
                            on_change=LPPositionState.set_notes,
                            width="100%",
                        ),
                        width="100%",
                        spacing="1",
                    ),
                    
                    rx.hstack(
                        rx.button(
                            "Cancel",
                            size="3",
                            variant="soft",
                            color_scheme="gray",
                            on_click=LPPositionState.clear_form,
                            width="50%",
                        ),
                        rx.button(
                            "Save Position",
                            size="3",
                            variant="soft",
                            color_scheme="blue",
                            on_click=LPPositionState.save_position_handler,
                            width="50%",
                            loading=LPPositionState.is_loading,
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
            ),
        
                width="100%",
                spacing="3",
            ),
            width="75%",
        ),
        width="100%",
    ),
    
    # Disable Hedge Confirmation Dialog
    rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.text("⚠️", size="6"),
                    rx.text("Disable Hedging?", size="5", weight="bold"),
                    spacing="2",
                    align_items="center",
                ),
                rx.divider(),
                rx.vstack(
                    rx.text("Important:", weight="bold", size="3", color="orange"),
                    rx.text(
                        "Disabling hedging will stop automatic rebalancing, but your existing hedge positions on Hyperliquid will remain open.",
                        size="2",
                    ),
                    rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                    rx.text("Recommended Actions:", weight="bold", size="3"),
                    rx.vstack(
                        rx.hstack(
                            rx.text("✓", color="green", weight="bold"),
                            rx.text("Keep hedge positions open if you still have LP exposure", size="2"),
                            spacing="2",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.text("✓", color="green", weight="bold"),
                            rx.text("Only close hedge positions AFTER withdrawing all LP liquidity", size="2"),
                            spacing="2",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.text("✓", color="green", weight="bold"),
                            rx.text("Manually close positions on Hyperliquid when ready", size="2"),
                            spacing="2",
                            align_items="start",
                        ),
                        spacing="2",
                        align_items="start",
                    ),
                    spacing="3",
                    align_items="start",
                ),
                rx.divider(),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=LPPositionState.cancel_disable_hedging,
                        ),
                    ),
                    rx.dialog.close(
                        rx.button(
                            "Disable Hedging",
                            color_scheme="orange",
                            on_click=LPPositionState.confirm_disable_hedging,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            max_width="500px",
        ),
        open=LPPositionState.show_disable_hedge_dialog,
    ),
    
    # Settings Dialog
    rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.text("Hedging Settings", size="5", weight="bold"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.icon_button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            on_click=LPPositionState.close_settings_dialog,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.divider(),
                
                # Find the selected position
                rx.foreach(
                    LPPositionState.lp_positions,
                    lambda pos: rx.cond(
                        pos.position_config_id == LPPositionState.selected_settings_position_id,
                        rx.vstack(
                            # Position name
                            rx.text(pos.position_name, size="3", weight="medium", color="gray"),
                            
                            rx.box(height="0.5rem"),
                            
                            # Current Applied Settings Section
                            rx.cond(
                                LPPositionState.regime_data_available,
                                rx.vstack(
                                    rx.text("Current Applied Settings", size="3", weight="bold", color="blue"),
                                    rx.text(f"Last updated: {LPPositionState.regime_timestamp}", size="1", color="gray"),
                                    
                                    # Regime Classification
                                    rx.box(
                                        rx.vstack(
                                            rx.text("Regime Classification", size="2", weight="medium"),
                                            rx.grid(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Funding Regime", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Current funding rate regime classification. Positive Strong/Mild = longs pay shorts (favorable for hedging). Neutral = balanced. Negative = shorts pay longs (costly for hedging). Affects hedge ratio adjustments.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_funding_regime, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Profile", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Active dynamic hedging profile. Balanced = neutral approach. Moderate/Aggressive Bullish = under-hedge for upside. Moderate Bearish = over-hedge for protection. Full Protection = maximum hedging. Determines base hedge strategy.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_profile_name, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                columns="4",
                                                spacing="6",
                                                width="100%",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="0.75rem",
                                        background="var(--blue-2)",
                                        border_radius="8px",
                                    ),
                                    
                                    # Applied Config Values
                                    rx.box(
                                        rx.vstack(
                                            rx.text("Applied Config Values", size="2", weight="medium"),
                                            rx.grid(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Target Hedge Ratio", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Percentage of LP position to hedge with short positions. 100% = fully hedged (delta neutral), 0% = no hedge (full exposure). Dynamic profiles adjust this based on market conditions.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_target_ratio_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Delta Drift", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="How much your position delta can drift before triggering a rebalance. Low = rebalance often (tight hedge), High = rebalance rarely (loose hedge). Standard tiers: Low (14%), Medium (38%), High (58%), Very High (80%). Dynamic profiles may use different values.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_delta_drift_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Rebalance Cooldown", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Minimum time to wait between hedge rebalances. Prevents over-trading. Lower = more responsive but higher fees. Higher = fewer trades but may miss optimal rebalances.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_cooldown_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Down Threshold", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Price drop % that triggers hedge adjustment. Used to detect significant downward moves. Standard tiers: Aggressive (-3.2%), Moderate (-5.5%), Conservative (-6.5%), Very Conservative (-15%). Dynamic profiles may use different values.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_down_threshold_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Bounce Threshold", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Price recovery % after a drop that triggers hedge reduction. Detects bounce-back moves. Standard tiers: Aggressive (-1.9%), Moderate (-3.2%), Conservative (-3.8%), Very Conservative (-7.5%). Dynamic profiles may use different values.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_bounce_threshold_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Lookback Hours", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Pullback filter: How far back to look for momentum before hedging. Standard tiers: Aggressive (4h), Balanced (6h), Conservative (12h). Dynamic profiles may use different values.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_lookback_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                columns="4",
                                                spacing="6",
                                                width="100%",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="0.75rem",
                                        background="var(--gray-2)",
                                        border_radius="8px",
                                    ),
                                    
                                    # Core Market Indicators
                                    rx.box(
                                        rx.vstack(
                                            rx.text("Core Market Indicators", size="2", weight="medium"),
                                            rx.grid(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Correlation (7d)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="7-day correlation between token prices. Values near 1.0 = prices move together (low hedge needed). Near 0 = uncorrelated. Near -1.0 = inverse relationship (high hedge needed). Used to calculate optimal hedge ratio.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(f"{LPPositionState.regime_corr_returns_7d:.4f}", size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Vol Ratio", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Ratio of token0 volatility to token1 volatility. Higher ratio = token0 is more volatile. Used with correlation to calculate minimum variance hedge ratio (MVHR). Helps determine optimal hedge size.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(f"{LPPositionState.regime_vol_ratio:.4f}", size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Funding Rate (daily)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Daily perpetual futures funding rate. Positive = longs pay shorts (you earn for hedging). Negative = shorts pay longs (you pay for hedging). Affects profitability of maintaining hedge positions.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_funding_rate_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("MRHL (hours)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Mean Reversion Half-Life: Time it takes for price to revert halfway back after a move. Lower = faster mean reversion (good for aggressive hedging). Higher = slower reversion (trend-following). Helps detect market regime.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(f"{LPPositionState.regime_mrhl_hours:.2f}", size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                columns="4",
                                                spacing="6",
                                                width="100%",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="0.75rem",
                                        background="var(--gray-2)",
                                        border_radius="8px",
                                    ),
                                    
                                    # Volatility Metrics
                                    rx.box(
                                        rx.vstack(
                                            rx.text("Volatility Metrics", size="2", weight="medium"),
                                            rx.grid(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Token0 Std Dev (7d)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Standard deviation of token0 price returns over 7 days. Measures token0 volatility. Higher = more volatile. Used to calculate volatility ratio and optimal hedge size.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(f"{LPPositionState.regime_std_token0_7d:.4f}", size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Token1 Std Dev (7d)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Standard deviation of token1 price returns over 7 days. Measures token1 volatility. Higher = more volatile. Used to calculate volatility ratio and optimal hedge size.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(f"{LPPositionState.regime_std_token1_7d:.4f}", size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("ARV 7d", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Annualized Realized Volatility over 7 days. Measures actual price movement volatility, annualized for comparison. Higher ARV = more volatile market. Helps assess risk and adjust hedging strategy.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_arv_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                columns="4",
                                                spacing="6",
                                                width="100%",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="0.75rem",
                                        background="var(--gray-2)",
                                        border_radius="8px",
                                    ),
                                    
                                    # Pool Metrics
                                    rx.box(
                                        rx.vstack(
                                            rx.text("Pool Metrics", size="2", weight="medium"),
                                            rx.grid(
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Pool TVL", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Total Value Locked in the liquidity pool. Higher TVL = more liquidity, lower slippage, more stable pool. Indicates pool health and trading efficiency.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_pool_tvl_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Pool Volume (24h)", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="24-hour trading volume in the pool. Higher volume = more active trading, better fee generation. Indicates pool activity and liquidity utilization.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_pool_volume_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                rx.vstack(
                                                    rx.hstack(
                                                        rx.text("Volume/TVL Ratio", size="1", color="gray"),
                                                        rx.tooltip(
                                                            rx.icon("info", size=12, color="gray"),
                                                            content="Ratio of 24h volume to total value locked. Higher ratio = more efficient capital usage, better fee generation per dollar locked. Indicates pool efficiency and profitability.",
                                                        ),
                                                        spacing="1",
                                                        align_items="center",
                                                    ),
                                                    rx.text(LPPositionState.regime_volume_tvl_ratio_display, size="2", weight="medium"),
                                                    spacing="1",
                                                    align_items="start",
                                                ),
                                                columns="4",
                                                spacing="6",
                                                width="100%",
                                            ),
                                            spacing="2",
                                        ),
                                        padding="0.75rem",
                                        background="var(--gray-2)",
                                        border_radius="8px",
                                    ),
                                    
                                    spacing="2",
                                    width="100%",
                                ),
                                rx.box(),
                            ),
                            
                            rx.divider(margin_top="1rem"),
                            
                            rx.hstack(
                                rx.dialog.close(
                                    rx.button(
                                        "Close",
                                        variant="soft",
                                        color_scheme="gray",
                                        on_click=LPPositionState.close_settings_dialog,
                                    ),
                                ),
                                justify="end",
                                width="100%",
                            ),
                            
                            spacing="3",
                            width="100%",
                        ),
                        rx.box(),  # Empty box if not the selected position
                    ),
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="900px",
        ),
        open=LPPositionState.show_settings_dialog,
    ),
    )
