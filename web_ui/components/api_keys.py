import reflex as rx
from ..api_key_state import APIKeyState, APIKeyData


def api_key_card(key: APIKeyData) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text(key.account_name, size="4", weight="bold"),
                    rx.hstack(
                        rx.text(key.exchange.title(), size="2", color="gray"),
                        rx.cond(
                            key.is_master_account,
                            rx.badge("Master Account", size="1", color_scheme="blue"),
                            rx.badge("Sub-Account", size="1", color_scheme="purple"),
                        ),
                        spacing="2",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        "Edit",
                        size="2",
                        variant="soft",
                        on_click=lambda: APIKeyState.edit_api_key(key.id),
                        loading=APIKeyState.loading_key_id == key.id,
                    ),
                    rx.button(
                        "Delete",
                        size="2",
                        variant="soft",
                        color_scheme="red",
                        on_click=lambda: APIKeyState.delete_api_key(key.id),
                        loading=APIKeyState.loading_key_id == key.id,
                    ),
                    spacing="2",
                ),
                width="100%",
                align="center",
            ),
            rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
            rx.vstack(
                rx.cond(
                    key.wallet_address != "",
                    rx.text("Wallet: " + key.wallet_address[:10] + "..." + key.wallet_address[-8:], size="2", color="gray"),
                ),
                # Subaccount name hidden from UI
                # rx.cond(
                #     key.subaccount_name != "",
                #     rx.text("Subaccount: " + key.subaccount_name, size="2", color="gray"),
                # ),
                rx.cond(
                    key.notes != "",
                    rx.text("Notes: " + key.notes, size="2", color="gray"),
                ),
                # API Key Assignment Status
                rx.hstack(
                    rx.text("API key assigned:", size="2", color="gray"),
                    rx.cond(
                        key.is_in_use,
                        rx.badge(
                            "In Use",
                            color_scheme="red",
                            size="1",
                        ),
                        rx.badge(
                            "Available",
                            color_scheme="green",
                            size="1",
                        ),
                    ),
                    spacing="2",
                    align_items="center",
                ),
                # Show position name on separate line if in use
                rx.cond(
                    key.is_in_use & (key.used_by_position != ""),
                    rx.text(
                        "Used by: " + key.used_by_position,
                        size="2",
                        color="gray",
                        font_style="italic",
                    ),
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            rx.divider(margin_top="0.5rem", margin_bottom="0.5rem"),
            rx.hstack(
                rx.button(
                    rx.cond(
                        key.balance_loading,
                        rx.spinner(size="1"),
                        "Check Balance",
                    ),
                    size="2",
                    variant="soft",
                    color_scheme="green",
                    on_click=lambda: APIKeyState.fetch_balance(key.id),
                    loading=key.balance_loading,
                    disabled=key.balance_loading,
                ),
                rx.cond(
                    key.account_value > 0,
                    rx.vstack(
                        rx.text(f"Account Value: ${key.account_value:,.2f}", size="2", weight="bold"),
                        rx.text(f"Available: ${key.available_balance:,.2f}", size="2", color="gray"),
                        spacing="0",
                        align_items="start",
                    ),
                ),
                rx.cond(
                    key.balance_error != "",
                    rx.text(key.balance_error, size="2", color="red"),
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        width="100%",
    )


def api_keys_component() -> rx.Component:
    return rx.vstack(
        # Error dialog for in-use keys - blocks deletion
        rx.alert_dialog.root(
            rx.alert_dialog.content(
                rx.alert_dialog.title("❌ Cannot Delete API Key"),
                rx.alert_dialog.description(
                    rx.vstack(
                        rx.text(
                            f"This API key is currently assigned to position '{APIKeyState.key_to_delete_position}'.",
                            size="3",
                        ),
                        rx.text(
                            "Before deleting this API key, you must:",
                            size="3",
                            weight="bold",
                            margin_top="1rem",
                        ),
                        rx.text(
                            "• Go to LP Positions and unassign this key (select 'None' from dropdown), OR",
                            size="3",
                        ),
                        rx.text(
                            "• Delete the LP position entirely",
                            size="3",
                        ),
                        spacing="2",
                        align_items="start",
                    ),
                ),
                rx.flex(
                    rx.alert_dialog.action(
                        rx.button(
                            "OK",
                            variant="soft",
                            color_scheme="blue",
                            on_click=APIKeyState.cancel_delete,
                        ),
                    ),
                    spacing="3",
                    justify="end",
                ),
            ),
            open=APIKeyState.show_delete_confirmation,
        ),
        
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.heading("API Keys", size="6"),
                    rx.spacer(),
                    rx.cond(
                        APIKeyState.is_editing,
                        rx.button(
                            "Cancel",
                            size="2",
                            variant="soft",
                            color_scheme="gray",
                            on_click=APIKeyState.clear_form,
                        ),
                    ),
                    width="100%",
                    align="center",
                ),
                rx.vstack(
                    rx.text(
                        "Manage your exchange API credentials for hedging operations.",
                        size="2",
                        color="gray",
                    ),
                    rx.text(
                        "• Each LP position requires its own dedicated API key",
                        size="2",
                        color="gray",
                    ),
                    rx.text(
                        "• Verify your credentials are working by clicking 'Check Balance' on any key",
                        size="2",
                        color="gray",
                    ),
                    rx.text(
                        "• Ensure you select the correct account type (Master Account for main wallets, or uncheck for vault/sub-accounts)",
                        size="2",
                        color="gray",
                    ),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            width="100%",
        ),
        
        rx.cond(
            APIKeyState.error_message != "",
            rx.callout(
                APIKeyState.error_message,
                icon="triangle_alert",
                color_scheme="red",
                role="alert",
            ),
        ),
        
        rx.cond(
            APIKeyState.success_message != "",
            rx.callout(
                APIKeyState.success_message,
                icon="check",
                color_scheme="green",
                role="alert",
            ),
        ),
        
        rx.cond(
            APIKeyState.api_keys.length() > 0,
            rx.grid(
                rx.foreach(APIKeyState.api_keys, api_key_card),
                columns="3",
                spacing="3",
                width="100%",
            ),
        ),
        
        rx.center(
            rx.card(
                rx.vstack(
                    rx.heading(
                        rx.cond(
                            APIKeyState.is_editing,
                            "Edit API Key",
                            "Add New API Key",
                        ),
                        size="5",
                    ),
                
                rx.form(
                    rx.vstack(
                        rx.vstack(
                            rx.text("Account Name", size="2", weight="bold"),
                            rx.input(
                                placeholder="e.g., Main Trading Account",
                                name="account_name",
                                type="text",
                                required=True,
                                max_width="500px",
                                default_value=APIKeyState.account_name,
                            ),
                            rx.text(
                                "A friendly name to identify this API key",
                                size="1",
                                color="gray",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.vstack(
                            rx.text("Exchange", size="2", weight="bold"),
                            rx.select(
                                ["hyperliquid", "binance (coming soon)", "lighter (coming soon)"],
                                placeholder="Select exchange",
                                name="exchange",
                                default_value=APIKeyState.exchange,
                                on_change=APIKeyState.set_exchange,
                                max_width="300px",
                            ),
                            rx.text(
                                "The exchange where this API key will be used",
                                size="1",
                                color="gray",
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.cond(
                            APIKeyState.exchange != "hyperliquid",
                            rx.vstack(
                                rx.text("API Key", size="2", weight="bold"),
                                rx.input(
                                    placeholder="Enter your API Key",
                                    name="api_key",
                                    type="text",
                                    required=True,
                                    width="100%",
                                    default_value=APIKeyState.api_key,
                                ),
                                width="100%",
                                spacing="1",
                            ),
                        ),
                        
                        rx.vstack(
                            rx.hstack(
                                rx.text(
                                    rx.cond(
                                        APIKeyState.exchange == "hyperliquid",
                                        "API Secret",
                                        "API Secret",
                                    ),
                                    size="2",
                                    weight="bold",
                                ),
                                rx.spacer(),
                                rx.button(
                                    rx.cond(APIKeyState.show_api_secret, "Hide", "Show"),
                                    size="1",
                                    variant="ghost",
                                    type="button",
                                    on_click=APIKeyState.toggle_secret_visibility,
                                ),
                                width="100%",
                                align="center",
                            ),
                            rx.input(
                                placeholder=rx.cond(
                                    APIKeyState.exchange == "hyperliquid",
                                    "Enter your Hyperliquid API Secret",
                                    "Enter your API Secret",
                                ),
                                name="api_secret",
                                type=rx.cond(APIKeyState.show_api_secret, "text", "password"),
                                required=True,
                                max_width="50%",
                                default_value=APIKeyState.api_secret,
                            ),
                            rx.cond(
                                APIKeyState.exchange == "hyperliquid",
                                rx.text(
                                    "For Hyperliquid, only the API Secret is required (no API Key needed)",
                                    size="1",
                                    color="gray",
                                ),
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        rx.cond(
                            APIKeyState.exchange == "hyperliquid",
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Wallet Address", size="2", weight="bold"),
                                    rx.input(
                                        placeholder="0x...",
                                        name="wallet_address",
                                        type="text",
                                        required=True,
                                        max_width="50%",
                                        default_value=APIKeyState.wallet_address,
                                    ),
                                    rx.text(
                                        "Your Hyperliquid wallet address (needed for balance/position queries)",
                                        size="1",
                                        color="gray",
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                
                                rx.vstack(
                                    rx.checkbox(
                                        "Master Account (Default Trading Address)",
                                        checked=APIKeyState.is_master_account,
                                        on_change=APIKeyState.set_is_master_account,
                                    ),
                                    rx.input(
                                        type="hidden",
                                        name="is_master_account",
                                        value=rx.cond(APIKeyState.is_master_account, "true", "false"),
                                    ),
                                    rx.text(
                                        "Check if this is your main wallet. Uncheck if trading with a vault/sub-account.",
                                        size="1",
                                        color="gray",
                                    ),
                                    width="100%",
                                    spacing="1",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        
                        # Subaccount Name field hidden from UI
                        # rx.vstack(
                        #     rx.text("Subaccount Name (Optional)", size="2", weight="bold"),
                        #     rx.input(
                        #         placeholder="e.g., default, trading, hedging",
                        #         name="subaccount_name",
                        #         type="text",
                        #         max_width="400px",
                        #         default_value=APIKeyState.subaccount_name,
                        #     ),
                        #     width="100%",
                        #     spacing="1",
                        # ),
                        
                        # Private Key field hidden from UI
                        # rx.vstack(
                        #     rx.hstack(
                        #         rx.text("Private Key (Optional)", size="2", weight="bold"),
                        #         rx.spacer(),
                        #         rx.button(
                        #             rx.cond(APIKeyState.show_private_key, "Hide", "Show"),
                        #             size="1",
                        #             variant="ghost",
                        #             on_click=APIKeyState.toggle_private_key_visibility,
                        #         ),
                        #         width="100%",
                        #         align="center",
                        #     ),
                        #     rx.input(
                        #         placeholder="For future use",
                        #         name="private_key",
                        #         type=rx.cond(APIKeyState.show_private_key, "text", "password"),
                        #         width="100%",
                        #         default_value=APIKeyState.private_key,
                        #     ),
                        #     width="100%",
                        #     spacing="1",
                        # ),
                        
                        rx.vstack(
                            rx.text("Notes (Optional)", size="2", weight="bold"),
                            rx.text_area(
                                placeholder="Any additional notes about this configuration",
                                name="notes",
                                width="100%",
                                default_value=APIKeyState.notes,
                            ),
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Show different button layouts based on edit mode
                        rx.cond(
                            APIKeyState.is_editing,
                            # Edit mode: Cancel and Update buttons
                            rx.hstack(
                                rx.button(
                                    "Cancel",
                                    size="3",
                                    variant="soft",
                                    color_scheme="gray",
                                    type="button",
                                    on_click=APIKeyState.cancel_edit,
                                    width="50%",
                                ),
                                rx.button(
                                    "Update API Key",
                                    type="submit",
                                    size="3",
                                    variant="soft",
                                    color_scheme="blue",
                                    width="50%",
                                    loading=APIKeyState.is_loading,
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            # Add mode: Single Add button
                            rx.button(
                                "Add API Key",
                                type="submit",
                                size="3",
                                variant="soft",
                                color_scheme="blue",
                                width="100%",
                                loading=APIKeyState.is_loading,
                            ),
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=APIKeyState.save_api_keys_handler,
                    reset_on_submit=True,
                ),
                
                rx.divider(margin_top="1.5rem", margin_bottom="1.5rem"),
                
                rx.vstack(
                    rx.text("Security Information", size="2", weight="bold"),
                    rx.text("• All sensitive data is encrypted before storage", size="1", color="gray"),
                    rx.text("• Keys are only accessible to your account", size="1", color="gray"),
                    rx.text("• You can manage multiple accounts and subaccounts", size="1", color="gray"),
                    spacing="1",
                    align_items="start",
                    width="100%",
                ),
                
                    spacing="3",
                    width="100%",
                ),
                width="100%",
            ),
            width="70%",
        ),
        
        spacing="4",
        width="100%",
    )
