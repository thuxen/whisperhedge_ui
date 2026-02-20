import reflex as rx
from ..lp_position_state import LPPositionState, LPPositionData
from ..config import AppConfig
from .position_chart import position_value_chart
from .position_activity import position_activity_dialog


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
                        spacing="2",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
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
                ),
                width="100%",
                align="center",
            ),
            
            rx.divider(margin_top="0.75rem", margin_bottom="0.75rem"),
            
            rx.grid(
                rx.vstack(
                    rx.text("Total Value (LP + Hedge Account)", size="1", color="gray", weight="medium"),
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
                rx.vstack(
                    rx.text("Status", size="1", color="gray", weight="medium"),
                    rx.hstack(
                        rx.text("Last Check:", size="2", color="gray"),
                        rx.text(
                            position.last_hedge_execution,
                            size="2",
                            weight="medium",
                            color=rx.cond(position.last_hedge_execution == "Never", "gray", "green"),
                        ),
                        spacing="1",
                        align_items="center",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                columns="2",
                spacing="4",
                width="100%",
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
                    rx.text("API Key", size="1", color="gray"),
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
            
            rx.box(height="0.5rem"),
            
            rx.vstack(
                rx.text("Hedging Settings", size="1", color="gray", weight="bold"),
                rx.grid(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Tokens Hedged", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Which tokens in the position are being hedged. Can hedge one or both tokens depending on strategy.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(
                            rx.cond(
                                position.hedge_enabled,
                                "Enabled",
                                "Disabled"
                            ),
                            size="2",
                            weight="medium"
                        ),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Target Ratio", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Desired hedge ratio as percentage of position value. 80% = hedge 80% of exposure, leaving 20% unhedged.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(position.target_hedge_ratio.to(str) + "%", size="2", weight="medium"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Hedge Mode", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Static = Fixed hedge ratio. Dynamic = Automatic adjustments based on market conditions using selected profile.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.badge(
                            rx.cond(
                                position.use_dynamic_hedging,
                                "Dynamic (" + position.dynamic_profile + ")",
                                "Static"
                            ),
                            color_scheme=rx.cond(position.use_dynamic_hedging, "purple", "blue"),
                            size="1",
                        ),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Rebalance Cooldown", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Minimum time between hedge adjustments. Prevents excessive trading while maintaining hedge effectiveness.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(position.rebalance_cooldown_hours.to(str) + "h", size="2", weight="medium"),
                        spacing="1",
                    ),
                    columns="4",
                    spacing="3",
                    width="100%",
                ),
                rx.grid(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Delta Drift", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="How much your position delta can drift before triggering a rebalance. Low = rebalance often (tight hedge). High = rebalance rarely (loose hedge).",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(position.delta_drift_threshold_pct.to(str) + "%", size="2", weight="medium"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Down Threshold", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Price drop % that triggers hedge adjustment. Used to detect significant downward moves. Aggressive = react to small moves. Conservative = wait for larger moves.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text((position.down_threshold * 100).to(str) + "%", size="2", weight="medium"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Bounce Threshold", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Price recovery % after a drop that triggers hedge reduction. Detects bounce-back moves. Aggressive = reduce hedge quickly on small bounces.",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text((position.bounce_threshold * 100).to(str) + "%", size="2", weight="medium"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Lookback Hours", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Pullback filter: How far back to look for momentum before hedging. Conservative=12h (more forgiving), Balanced=6h, Aggressive=4h (quicker reaction).",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(position.lookback_hours.to(str) + "h", size="2", weight="medium"),
                        spacing="1",
                    ),
                    columns="4",
                    spacing="3",
                    width="100%",
                    margin_top="0.5rem",
                ),
                rx.grid(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Min Drift % Capital", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Safety: Minimum drift size before hedging (as % of position). Conservative=10% (fewer tiny trades), Balanced=6%, Aggressive=4% (capture more small moves).",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text((position.drift_min_pct_of_capital * 100).to(str) + "%", size="2", weight="medium"),
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.text("Max Hedge Drift", size="1", color="gray"),
                            rx.tooltip(
                                rx.icon("info", size=12, color="gray"),
                                content="Safety: Maximum allowed delta drift before forcing a hedge. Conservative=70% (more drift allowed), Balanced=50%, Aggressive=40% (more frequent protection).",
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text((position.max_hedge_drift_pct * 100).to(str) + "%", size="2", weight="medium"),
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
                padding="0.75rem",
                background="var(--gray-2)",
                border_radius="8px",
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
                        "Refresh Status",
                        size="2",
                        variant="soft",
                        color_scheme="blue",
                        on_click=LPPositionState.refresh_position_status,
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
                                    rx.text("Pool:", weight="bold", size="2"),
                                    rx.text(LPPositionState.pool_address, size="2", color="gray"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.text("Pair:", weight="bold", size="2"),
                                    rx.text(LPPositionState.token0_symbol + "/" + LPPositionState.token1_symbol, size="2"),
                                    spacing="2",
                                ),
                                rx.text("Current Prices:", weight="bold", size="2"),
                                rx.cond(
                                    LPPositionState.fetched_position_data.get("hl_price_available", False),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token0_symbol}:", weight="bold", size="2"),
                                            rx.text(f"${LPPositionState.fetched_position_data.get('token0_price_usd', 0):.2f}", size="2"),
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token1_symbol}:", weight="bold", size="2"),
                                            rx.text(f"${LPPositionState.fetched_position_data.get('token1_price_usd', 0):.2f}", size="2"),
                                            spacing="2",
                                        ),
                                        spacing="1",
                                        align_items="start",
                                    ),
                                    rx.text(f"{LPPositionState.fetched_position_data.get('current_price', 0):.6f} (ratio)", size="2", color="gray"),
                                ),
                                rx.hstack(
                                    rx.text("Price Range:", weight="bold", size="2"),
                                    rx.cond(
                                        LPPositionState.fetched_position_data.get("hl_price_available", False),
                                        rx.text(f"${LPPositionState.fetched_position_data.get('pa_usd', 0):.2f} - ${LPPositionState.fetched_position_data.get('pb_usd', 0):.2f} USD", size="2"),
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
                                rx.text("📦 LP Exposure", size="3", weight="bold"),
                                rx.cond(
                                    LPPositionState.fetched_position_data.get("hl_price_available", False),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token0_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token0_amount', 0):.6f}", size="2"),
                                            rx.text(f"(${LPPositionState.fetched_position_data.get('token0_amount_usd', 0):,.2f})", size="2", color="green"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token0_pct', 0):.1f}%", size="2", color="gray"),
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token1_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token1_amount', 0):.6f}", size="2"),
                                            rx.text(f"(${LPPositionState.fetched_position_data.get('token1_amount_usd', 0):,.2f})", size="2", color="green"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token1_pct', 0):.1f}%", size="2", color="gray"),
                                            spacing="2",
                                        ),
                                        spacing="1",
                                        align_items="start",
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token0_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token0_amount', 0):.6f}", size="2"),
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token1_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token1_amount', 0):.6f}", size="2"),
                                            spacing="2",
                                        ),
                                        spacing="1",
                                        align_items="start",
                                    ),
                                ),
                                # Show USD values if available
                                rx.cond(
                                    LPPositionState.fetched_position_data.get("hl_price_available", False),
                                    rx.vstack(
                                        rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                        rx.text("💰 Position Value (Hyperliquid Prices)", size="2", weight="bold", color="green"),
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token0_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token0_amount', 0):.6f} @ ${LPPositionState.fetched_position_data.get('token0_price_usd', 0):.4f} = ${LPPositionState.fetched_position_data.get('token0_amount_usd', 0):,.2f}", size="2"),
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.text(f"{LPPositionState.token1_symbol}:", weight="bold", size="2"),
                                            rx.text(f"{LPPositionState.fetched_position_data.get('token1_amount', 0):.6f} @ ${LPPositionState.fetched_position_data.get('token1_price_usd', 0):.4f} = ${LPPositionState.fetched_position_data.get('token1_amount_usd', 0):,.2f}", size="2"),
                                            spacing="2",
                                        ),
                                        rx.hstack(
                                            rx.text("Total Value:", weight="bold", size="2"),
                                            rx.text(f"${LPPositionState.fetched_position_data.get('position_value_usd', 0):,.2f}", size="2", weight="bold", color="green"),
                                            spacing="2",
                                        ),
                                        spacing="2",
                                        align_items="start",
                                        width="100%",
                                    ),
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
                                                rx.text("API Key", size="2", weight="bold"),
                                                rx.select(
                                                    LPPositionState.available_wallets,
                                                    value=LPPositionState.selected_hedge_wallet,
                                                    on_change=LPPositionState.set_hedge_wallet,
                                                    placeholder="Select API key for hedging",
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
                                                spacing="1",
                                                width="100%",
                                            ),
                                            
                                            rx.vstack(
                                                rx.text("Hedge Strategy", size="2", weight="bold"),
                                                rx.select(
                                                    ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "Dynamic"],
                                                    value=LPPositionState.hedge_ratio_display,
                                                    on_change=LPPositionState.set_hedge_ratio,
                                                    placeholder="Select hedge strategy",
                                                ),
                                                rx.cond(
                                                    LPPositionState.use_dynamic_hedging,
                                                    rx.text("Dynamic hedging adjusts ratio based on market conditions", size="1", color="blue"),
                                                    rx.text(f"Static hedge at {LPPositionState.hedge_ratio}% of position exposure", size="1", color="gray"),
                                                ),
                                                spacing="1",
                                                width="100%",
                                            ),
                                            
                                            # Dynamic Hedging Configuration
                                            rx.cond(
                                                LPPositionState.use_dynamic_hedging,
                                                rx.vstack(
                                                    rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
                                                    rx.text("🎯 Dynamic Hedging Profile", size="2", weight="bold", color="blue"),
                                                    
                                                    rx.vstack(
                                                        rx.text("Profile", size="2", weight="bold"),
                                                        rx.select(
                                                            ["balanced", "whisper_dynamic", "aggressive_upside", "aggressive_downside", "volatility_adaptive"],
                                                            value=LPPositionState.dynamic_profile,
                                                            on_change=LPPositionState.set_dynamic_profile,
                                                            placeholder="Select profile",
                                                        ),
                                                        rx.match(
                                                            LPPositionState.dynamic_profile,
                                                            ("balanced", rx.text("Standard delta-neutral hedging with moderate adjustments", size="1", color="gray")),
                                                            ("whisper_dynamic", rx.text("Whisper Capital's proprietary dynamic hedging algorithm", size="1", color="blue")),
                                                            ("aggressive_upside", rx.text("Reduce hedge on upward moves to capture more gains", size="1", color="gray")),
                                                            ("aggressive_downside", rx.text("Increase hedge on downward moves for protection", size="1", color="gray")),
                                                            ("volatility_adaptive", rx.text("Adjust based on implied/realized volatility", size="1", color="gray")),
                                                            rx.text("Select a profile", size="1", color="gray"),
                                                        ),
                                                        spacing="1",
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
    )
