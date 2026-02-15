import reflex as rx
from pydantic import BaseModel
from .auth import get_supabase_client


class LPPositionData(BaseModel):
    id: str
    position_config_id: str = ""
    position_name: str
    protocol: str = "uniswap_v3"
    network: str
    nft_id: str
    pool_address: str = ""
    token0_symbol: str = ""
    token1_symbol: str = ""
    fee_tier: str = ""
    is_active: bool = True
    notes: str = ""
    created_at: str = ""
    # New fields for display
    position_size_usd: float = 0.0
    position_value_formatted: str = "$0.00"
    hedge_enabled: bool = False
    target_hedge_ratio: float = 0.0
    hedge_details: str = "Disabled"
    api_key_name: str = ""
    api_account_value: float = 0.0
    total_value_usd: float = 0.0
    total_value_formatted: str = "$0.00"
    hedge_token0: bool = True
    hedge_token1: bool = True
    use_dynamic_hedging: bool = False
    dynamic_profile: str = "balanced"
    rebalance_cooldown_hours: float = 8.0
    delta_drift_threshold_pct: float = 0.38
    down_threshold: float = -0.065
    bounce_threshold: float = -0.038
    lookback_hours: float = 6.0
    drift_min_pct_of_capital: float = 0.06
    max_hedge_drift_pct: float = 0.50
    last_hedge_execution: str = "Never"


class LPPositionState(rx.State):
    lp_positions: list[LPPositionData] = []
    selected_position_id: str = ""
    position_name: str = ""
    
    # Delete confirmation dialog
    show_delete_dialog: bool = False
    position_to_delete: str = ""
    protocol: str = "uniswap_v3"
    network: str = "ethereum"
    nft_id: str = ""
    pool_address: str = ""
    token0_symbol: str = ""
    token1_symbol: str = ""
    fee_tier: str = ""
    notes: str = ""
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    is_editing: bool = False
    show_confirmation: bool = False
    fetched_position_data: dict = {}
    
    # Hedge configuration fields
    hedge_enabled: bool = False
    hedge_token0: bool = True
    hedge_token1: bool = True
    selected_api_key_id: str = ""
    
    # Loading state
    loading_position_id: str = ""
    is_fetching: bool = False
    
    # Chart data
    chart_data: list = []
    chart_loading: bool = False
    chart_hours: int = 24
    selected_chart_position_id: str = ""
    show_chart: bool = False
    
    # Activity dialog
    show_activity_dialog: bool = False
    selected_activity_position_id: str = ""
    
    # Temporary state for fetch handler
    _fetch_protocol: str = ""
    _fetch_network: str = ""
    _fetch_nft_id: str = ""
    
    hedge_ratio: int = 80
    selected_hedge_wallet: str = ""
    _cached_wallets: list[str] = []  # Cache for available wallets
    
    # Balance tracking for selected API key
    selected_wallet_balance: float = 0.0
    selected_wallet_available: float = 0.0
    balance_loading: bool = False
    balance_error: str = ""
    
    # Dynamic hedging fields
    use_dynamic_hedging: bool = False
    dynamic_profile: str = "balanced"
    rebalance_cooldown_hours: float = 8.0
    delta_drift_threshold_pct: float = 0.38
    down_threshold: float = -0.065
    bounce_threshold: float = -0.038
    lookback_hours: float = 6.0
    drift_min_pct_of_capital: float = 0.06
    max_hedge_drift_pct: float = 0.50
    
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    def set_position_name(self, value: str):
        self.position_name = value
    
    def set_notes(self, value: str):
        self.notes = value
    
    def toggle_hedge_token0(self):
        self.hedge_token0 = not self.hedge_token0
    
    def toggle_hedge_token1(self):
        self.hedge_token1 = not self.hedge_token1
    
    def set_hedge_ratio(self, value: str):
        # Dynamic is represented as 0 internally
        if value == "Dynamic":
            self.hedge_ratio = 0
            self.use_dynamic_hedging = True
        else:
            self.hedge_ratio = int(value)
            self.use_dynamic_hedging = False
    
    def toggle_hedge_enabled(self, value: bool):
        """Handle hedge enabled toggle with validation"""
        if value:  # User is trying to enable hedging
            # Check if API key is assigned
            if not self.selected_hedge_wallet or self.selected_hedge_wallet == "None":
                self.error_message = "Please assign an API key before enabling hedging"
                return rx.toast.error("API key required to enable hedging", duration=5000)
            
            # Enable immediately with warning toast
            self.hedge_enabled = True
            return rx.toast.warning("Hedging enabled - live trades will be placed when you save", duration=5000)
        else:  # User is disabling hedging
            self.hedge_enabled = False
    
    async def set_hedge_wallet(self, wallet: str):
        self.selected_hedge_wallet = wallet
        
        # If None is selected, clear the balance and return
        if wallet == "None":
            self.selected_wallet_balance = 0.0
            return
        
        await self.fetch_wallet_balance()
    
    def set_dynamic_profile(self, value: str):
        self.dynamic_profile = value
    
    def set_rebalance_cooldown(self, value: str):
        # Parse "X hour(s)" format
        hours = float(value.split()[0])
        self.rebalance_cooldown_hours = hours
    
    def set_delta_drift_threshold(self, value: str):
        # Parse "Level (XX%)" format
        mapping = {
            "Low (14%)": 0.14,
            "Medium (38%)": 0.38,
            "High (58%)": 0.58,
            "Very High (80%)": 0.80
        }
        # Handle both dropdown format and direct percentage strings
        if value in mapping:
            self.delta_drift_threshold_pct = mapping[value]
        else:
            # Try to parse as percentage string (e.g., "0.3%")
            try:
                self.delta_drift_threshold_pct = float(value.rstrip('%')) / 100.0
            except:
                self.delta_drift_threshold_pct = 0.38
    
    def set_down_threshold(self, value: str):
        # Parse "Level (-X.X%)" format
        mapping = {
            "Aggressive (-3.2%)": -0.032,
            "Moderate (-5.5%)": -0.055,
            "Conservative (-6.5%)": -0.065,
            "Very Conservative (-15%)": -0.15
        }
        self.down_threshold = mapping.get(value, -0.065)
    
    def set_bounce_threshold(self, value: str):
        # Parse "Level (-X.X%)" format
        mapping = {
            "Aggressive (-1.9%)": -0.019,
            "Moderate (-3.2%)": -0.032,
            "Conservative (-3.8%)": -0.038,
            "Very Conservative (-7.5%)": -0.075
        }
        self.bounce_threshold = mapping.get(value, -0.038)
    
    def set_lookback_hours(self, value: str):
        # Parse "Level (Xh)" format
        mapping = {
            "Aggressive (4h)": 4.0,
            "Balanced (6h)": 6.0,
            "Conservative (12h)": 12.0
        }
        self.lookback_hours = mapping.get(value, 6.0)
    
    def set_drift_min_pct_of_capital(self, value: str):
        # Parse "Level (X%)" format
        mapping = {
            "Aggressive (4%)": 0.04,
            "Balanced (6%)": 0.06,
            "Conservative (10%)": 0.10
        }
        self.drift_min_pct_of_capital = mapping.get(value, 0.06)
    
    def set_max_hedge_drift_pct(self, value: str):
        # Parse "Level (X%)" format
        mapping = {
            "Aggressive (40%)": 0.40,
            "Balanced (50%)": 0.50,
            "Conservative (70%)": 0.70
        }
        self.max_hedge_drift_pct = mapping.get(value, 0.50)
    
    @rx.var
    def hedge_ratio_display(self) -> str:
        """Display value for hedge ratio dropdown"""
        if self.hedge_ratio == 0:
            return "Dynamic"
        return str(self.hedge_ratio)
    
    @rx.var
    def rebalance_cooldown_display(self) -> str:
        """Display value for rebalance cooldown dropdown"""
        hours = int(self.rebalance_cooldown_hours)
        if hours == 1:
            return "1 hour"
        return f"{hours} hours"
    
    @rx.var
    def estimated_hedge_token0(self) -> float:
        """Calculate estimated hedge amount for token0"""
        if not self.fetched_position_data or not self.hedge_enabled or not self.hedge_token0:
            return 0.0
        # Use delta if available (for in-range positions), otherwise use token0_amount
        delta = self.fetched_position_data.get('delta', 0.0)
        if delta == 0.0:
            delta = self.fetched_position_data.get('token0_amount', 0.0)
        return delta * (self.hedge_ratio / 100.0)
    
    @rx.var
    def estimated_hedge_token1(self) -> float:
        """Calculate estimated hedge amount for token1"""
        if not self.fetched_position_data or not self.hedge_enabled or not self.hedge_token1:
            return 0.0
        token1_amount = self.fetched_position_data.get('token1_amount', 0.0)
        return token1_amount * (self.hedge_ratio / 100.0)
    
    async def load_wallets(self):
        """Load available API keys for wallet selector - called on mount"""
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            
            # Get all active API keys
            response = supabase.table("user_api_keys").select("id,account_name,exchange").eq("user_id", auth_state.user_id).eq("is_active", True).execute()
            
            if response.data:
                # Get API keys that are already in use by other positions
                used_keys_response = supabase.table("position_configs").select("hl_api_key_id").eq("user_id", auth_state.user_id).execute()
                used_key_ids = {config["hl_api_key_id"] for config in used_keys_response.data if config.get("hl_api_key_id")}
                
                # When editing, allow the current position's API key to appear
                current_position_key_id = None
                if self.is_editing and self.selected_position_id:
                    current_config = supabase.table("position_configs").select("hl_api_key_id").eq("user_id", auth_state.user_id).eq("network", self.network).eq("nft_id", self.nft_id).execute()
                    if current_config.data and current_config.data[0].get("hl_api_key_id"):
                        current_position_key_id = current_config.data[0]["hl_api_key_id"]
                
                # Filter out used keys (except the current position's key when editing)
                available_keys = [
                    key for key in response.data 
                    if key["id"] not in used_key_ids or key["id"] == current_position_key_id
                ]
                
                # Add None option to allow unassigning API keys
                wallets = ["None"] + [f"{key['account_name']} ({key['exchange']})" for key in available_keys]
                # Store in cache for immediate use
                self._cached_wallets = wallets
                # Auto-select first wallet if none selected (skip None)
                if wallets and not self.selected_hedge_wallet and len(wallets) > 1:
                    self.selected_hedge_wallet = wallets[1]  # Select first actual wallet, not None
                    # Auto-fetch balance for the selected wallet
                    await self.fetch_wallet_balance()
            
            # Mark wallets as loaded for dashboard loading state
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_wallets_loaded()
        except Exception as e:
            # Mark as loaded even on error to prevent infinite loading
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_wallets_loaded()
            pass
    
    @rx.var
    def available_wallets(self) -> list[str]:
        """Get list of available API keys for wallet selector"""
        return self._cached_wallets
    
    async def fetch_wallet_balance(self):
        """Fetch balance for selected wallet"""
        try:
            from web_ui.state import AuthState
            from web_ui.hl_utils import get_hl_account_balance
            
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            if not self.selected_hedge_wallet:
                return
            
            self.balance_loading = True
            self.balance_error = ""
            self.selected_wallet_balance = 0.0
            self.selected_wallet_available = 0.0
            
            supabase = get_supabase_client(auth_state.access_token)
            
            # Extract account name from "Account Name (exchange)" format
            account_name = self.selected_hedge_wallet.split(" (")[0]
            
            # Get API key details
            response = supabase.table("user_api_keys").select("*").eq("user_id", auth_state.user_id).eq("account_name", account_name).execute()
            
            if response.data and len(response.data) > 0:
                key_data = response.data[0]
                
                if key_data.get("exchange", "").lower() == "hyperliquid":
                    wallet_address = key_data.get("wallet_address")
                    
                    if wallet_address:
                        # Fetch balance using wallet address
                        balance_info = get_hl_account_balance(wallet_address)
                        
                        if balance_info:
                            self.selected_wallet_balance = balance_info['account_value']
                            self.selected_wallet_available = balance_info['available']
                            
                            # Save balance to database
                            try:
                                supabase.table("user_api_keys").update({
                                    "account_value": balance_info['account_value'],
                                    "available_balance": balance_info['available']
                                }).eq("id", key_data["id"]).execute()
                            except Exception as e:
                                print(f"Failed to save balance to database: {e}")
                        else:
                            self.balance_error = "Failed to fetch balance"
                    else:
                        self.balance_error = "No wallet address"
                else:
                    self.balance_error = "Only Hyperliquid supported"
            else:
                self.balance_error = "API key not found"
            
            self.balance_loading = False
            
        except Exception as e:
            self.balance_loading = False
            self.balance_error = f"Error: {str(e)}"
    
    def clear_form(self):
        """Clear all form fields"""
        self.selected_position_id = ""
        self.position_name = ""
        self.network = "ethereum"
        self.nft_id = ""
        self.pool_address = ""
        self.token0_symbol = ""
        self.token1_symbol = ""
        self.fee_tier = ""
        self.notes = ""
        self.is_editing = False
        self.show_confirmation = False
        self.fetched_position_data = {}
        
        # Clear hedge configuration
        self.hedge_enabled = False
        self.hedge_token0 = True
        self.hedge_token1 = True
        self.selected_api_key_id = ""
        
        # Clear balance tracking
        self.selected_wallet_balance = 0.0
        self.selected_wallet_available = 0.0
        self.balance_loading = False
        self.balance_error = ""
        
    async def check_api_key_availability(self, api_key_id: str) -> bool:
        """Check if API key is available (not used by another position)"""
        if not api_key_id:
            return True  # No API key selected is always allowed
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return False
            
            supabase = get_supabase_client(auth_state.access_token)
            
            # Check if this API key is already used by another position
            try:
                result = supabase.table("position_configs").select("id").eq("hl_api_key_id", api_key_id).execute()
                
                # If editing, allow the same API key for the same position
                if self.is_editing and self.selected_position_id:
                    # Check if the existing usage is by this same position
                    existing_result = supabase.table("position_configs").select("id").eq("hl_api_key_id", api_key_id).eq("position_name", self.position_name).execute()
                    return len(existing_result.data) > 0
                
                # For new positions, API key must not be used by any other position
                return len(result.data) == 0
            except Exception as table_error:
                # If position_configs table doesn't exist, assume API key is available
                print(f"Warning: position_configs table not accessible: {table_error}")
                return True
            
        except Exception as e:
            print(f"Error checking API key availability: {e}")
            return False
    
    def edit_position(self, position_id: str):
        """Immediate feedback handler"""
        # Set loading state immediately
        self.loading_position_id = position_id
        
        # Return toast and chain to async worker (no args needed now)
        return [
            rx.toast.info("Loading position data...", duration=5000),
            LPPositionState.fetch_data_worker
        ]

    async def fetch_data_worker(self):
        """Async worker that uses state instead of args"""
        if not self.loading_position_id:
            return
            
        position_id = self.loading_position_id
        
        # 1. Find position locally
        position = next((p for p in self.lp_positions if p.id == position_id), None)
        if not position:
            self.loading_position_id = ""
            yield rx.toast.error("Position not found", duration=3000)
            return

        # 2. Update form fields
        self.selected_position_id = position_id
        self.position_name = position.position_name
        self.network = position.network
        self.nft_id = position.nft_id
        self.pool_address = position.pool_address
        self.token0_symbol = position.token0_symbol
        self.token1_symbol = position.token1_symbol
        self.fee_tier = position.fee_tier
        self.notes = position.notes
        self.is_editing = True
        self.show_confirmation = True  # Show the full position form

        try:
            # 3. Load available API keys
            await self.load_wallets()
            
            # 4. Fetch fresh blockchain data
            from .blockchain_utils import fetch_uniswap_position
            
            self.fetched_position_data = await fetch_uniswap_position(self.network, self.nft_id)
            
            # Update fields with fresh blockchain data if available
            if self.fetched_position_data:
                self.pool_address = self.fetched_position_data.get("pool_address", self.pool_address)
                self.token0_symbol = self.fetched_position_data.get("token0_symbol", self.token0_symbol)
                self.token1_symbol = self.fetched_position_data.get("token1_symbol", self.token1_symbol)
                self.fee_tier = self.fetched_position_data.get("fee_tier", self.fee_tier)
            
            # 5. Load hedge configuration
            await self.load_hedge_config(position_id)
            
            yield rx.toast.success("Position loaded for editing!", duration=3000)
        except Exception as e:
            yield rx.toast.error(f"Failed to load: {str(e)}", duration=5000)
        finally:
            self.loading_position_id = ""

    def open_delete_dialog(self, position_id: str):
        """Open confirmation dialog before deleting"""
        self.position_to_delete = position_id
        self.show_delete_dialog = True
    
    def cancel_delete(self):
        """Cancel deletion and close dialog"""
        self.show_delete_dialog = False
        self.position_to_delete = ""
    
    def delete_position(self):
        """Confirmed deletion - immediate feedback handler"""
        self.loading_position_id = self.position_to_delete
        self.show_delete_dialog = False
        return [
            rx.toast.info("Deleting position...", duration=5000),
            LPPositionState.delete_worker
        ]

    async def delete_worker(self):
        """Async worker that uses state instead of args"""
        if not self.loading_position_id:
            return

        position_id = self.loading_position_id
        self.is_loading = True
        self.clear_messages()
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                yield rx.toast.error("Not authenticated", duration=3000)
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            position = next((p for p in self.lp_positions if p.id == position_id), None)
            position_name = position.position_name if position else "position"
            
            supabase.table("lp_positions").delete().eq("id", position_id).eq("user_id", auth_state.user_id).execute()
            
            await self.load_positions()
            if self.selected_position_id == position_id:
                self.clear_form()
            
            yield rx.toast.success(f"Deleted '{position_name}'!", duration=3000)
        except Exception as e:
            yield rx.toast.error("Failed to delete position. Please try again.", duration=5000)
        finally:
            self.is_loading = False
            self.loading_position_id = ""

    async def refresh_position_status(self):
        """Lightweight refresh of position status without full reload"""
        try:
            print("[REFRESH STATUS] Starting position status refresh", flush=True)
            
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                print("[REFRESH STATUS] Not authenticated, skipping refresh", flush=True)
                return
            
            # Only update last_hedge_execution for existing positions
            for position in self.lp_positions:
                if position.position_config_id:
                    try:
                        from .config import AppConfig
                        from .supabase_client import get_supabase_client
                        from .questdb_utils import get_last_hedge_execution, format_time_ago
                        from .address_utils import normalize_address_for_storage
                        last_hedge_dt = get_last_hedge_execution(position.position_config_id)
                        new_status = format_time_ago(last_hedge_dt)
                        
                        # Only log if status changed
                        if position.last_hedge_execution != new_status:
                            print(f"[REFRESH STATUS] Position {position.position_name}: {position.last_hedge_execution} -> {new_status}", flush=True)
                            position.last_hedge_execution = new_status
                    except Exception as e:
                        print(f"[REFRESH STATUS] Error refreshing position {position.position_config_id}: {e}", flush=True)
            
            print("[REFRESH STATUS] Refresh complete", flush=True)
        except Exception as e:
            print(f"[REFRESH STATUS ERROR] {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    async def load_positions(self):
        print("\n=== LOAD_POSITIONS START ===")
        
        self.is_loading = True
        self.clear_messages()
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            print(f"Auth state: authenticated={auth_state.is_authenticated}, user_id={auth_state.user_id}")
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.error_message = "Not authenticated"
                self.is_loading = False
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            
            # Fetch positions for current user
            print(f"Fetching lp_positions for user_id={auth_state.user_id}")
            response = supabase.table("lp_positions").select("*").eq("user_id", auth_state.user_id).execute()
            print(f"lp_positions response: {len(response.data) if response.data else 0} positions found")
            
            self.lp_positions = []
            if response.data:
                # Fetch config data to merge
                print(f"Fetching position_configs for user_id={auth_state.user_id}")
                config_response = supabase.table("position_configs").select("*").eq("user_id", auth_state.user_id).execute()
                print(f"position_configs response: {len(config_response.data) if config_response.data else 0} configs found")
                
                # Build config map using protocol, network, and nft_id (actual columns in database)
                config_map = {}
                if config_response.data:
                    for c in config_response.data:
                        protocol = c.get('protocol', 'uniswap_v3')
                        nft_id = c.get('nft_id', '')
                        print(f"Config: protocol={protocol}, network={c.get('network')}, nft_id={nft_id}")
                        if nft_id:
                            config_map[f"{protocol}_{c['network']}_{nft_id}"] = c
                print(f"Built config_map with {len(config_map)} entries")
                
                # Fetch API keys to get account names and balances
                api_keys_response = supabase.table("user_api_keys").select("id, account_name, account_value, available_balance").eq("user_id", auth_state.user_id).execute()
                api_key_map = {k["id"]: {"name": k["account_name"], "balance": float(k.get("account_value", 0.0))} for k in api_keys_response.data} if api_keys_response.data else {}
                
                for pos_data in response.data:
                    # Look up config
                    protocol = pos_data.get('protocol', 'uniswap_v3')
                    config_key = f"{protocol}_{pos_data['network']}_{pos_data['nft_id']}"
                    config = config_map.get(config_key, {})
                    print(f"Position: network={pos_data['network']}, nft_id={pos_data['nft_id']}, config_found={bool(config)}")
                    
                    # Get API key name and balance if assigned
                    api_key_id = config.get("hl_api_key_id", "")
                    api_key_info = api_key_map.get(api_key_id, {"name": "", "balance": 0.0})
                    api_key_name = api_key_info["name"]
                    api_account_value = api_key_info["balance"]
                    
                    # Get LP value from QuestDB (most accurate, updated by hedging bot)
                    # Fall back to database value only if QuestDB has no data (new positions)
                    position_size_usd = float(config.get("position_size_usd", 0.0))  # Fallback value
                    last_hedge_time_str = "Never"
                    
                    if config.get("id"):
                        try:
                            from web_ui.questdb_utils import get_latest_position_values, get_last_hedge_execution, format_time_ago
                            
                            # Try to get latest values from QuestDB
                            latest_values = get_latest_position_values(config["id"])
                            if latest_values and latest_values.get('lp_value_usd'):
                                # Use QuestDB value (most accurate)
                                position_size_usd = latest_values['lp_value_usd']
                                
                                # Sync QuestDB value back to Supabase to keep database fresh
                                try:
                                    supabase.table("position_configs").update({
                                        "position_size_usd": position_size_usd
                                    }).eq("id", config["id"]).execute()
                                except Exception as update_error:
                                    print(f"Warning: Failed to sync position_size_usd to Supabase: {update_error}")
                                
                                # Also update hedge account value if available
                                if latest_values.get('hl_account_value'):
                                    api_account_value = latest_values['hl_account_value']
                            
                            # Get last hedge execution time
                            last_hedge_dt = get_last_hedge_execution(config["id"])
                            last_hedge_time_str = format_time_ago(last_hedge_dt)
                        except Exception as e:
                            print(f"Error fetching QuestDB data for position {config.get('id')}: {e}")
                    
                    # Calculate total value (LP position + API account)
                    total_value_usd = position_size_usd + api_account_value
                    
                    position = LPPositionData(
                        id=pos_data["id"],
                        position_config_id=config.get("id", ""),
                        position_name=pos_data["position_name"],
                        protocol=pos_data.get("protocol", "uniswap_v3"),
                        network=pos_data["network"],
                        nft_id=pos_data["nft_id"],
                        pool_address=pos_data.get("pool_address", ""),
                        token0_symbol=pos_data.get("token0_symbol", ""),
                        token1_symbol=pos_data.get("token1_symbol", ""),
                        fee_tier=str(pos_data.get("fee_tier", "")),
                        is_active=pos_data.get("is_active", True),
                        notes=pos_data.get("notes", ""),
                        created_at=pos_data.get("created_at", ""),
                        # Populate new fields from config
                        position_size_usd=position_size_usd,
                        position_value_formatted=f"${position_size_usd:,.2f}",
                        hedge_enabled=config.get("hedge_enabled", False),
                        target_hedge_ratio=float(config.get("target_hedge_ratio", 0.0)),
                        hedge_details=f"Hedge: {int(float(config.get('target_hedge_ratio', 0.0)))}%" if config.get("hedge_enabled", False) else "Hedge: Disabled",
                        api_key_name=api_key_name,
                        api_account_value=api_account_value,
                        total_value_usd=total_value_usd,
                        total_value_formatted=f"${total_value_usd:,.2f}",
                        hedge_token0=config.get("hedge_token0", True),
                        hedge_token1=config.get("hedge_token1", True),
                        use_dynamic_hedging=config.get("use_dynamic_hedging", False),
                        dynamic_profile=config.get("dynamic_profile", "balanced"),
                        rebalance_cooldown_hours=float(config.get("rebalance_cooldown_hours", 8.0)),
                        delta_drift_threshold_pct=float(config.get("delta_drift_threshold_pct", 0.38)),
                        down_threshold=float(config.get("down_threshold", -0.065)),
                        bounce_threshold=float(config.get("bounce_threshold", -0.038)),
                        lookback_hours=float(config.get("lookback_hours", 6.0)),
                        drift_min_pct_of_capital=float(config.get("drift_min_pct_of_capital", 0.06)),
                        max_hedge_drift_pct=float(config.get("max_hedge_drift_pct", 0.50)),
                        last_hedge_execution=last_hedge_time_str,
                    )
                    self.lp_positions.append(position)
            else:
                self.lp_positions = []
                
            print(f"Successfully loaded {len(self.lp_positions)} positions")
            
            print("=== LOAD_POSITIONS END ===\n")
            
            # Update overview stats
            await self._update_overview_stats()
            
            # Mark positions as loaded for dashboard loading state
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_positions_loaded()
        except Exception as e:
            print(f"\n!!! ERROR IN LOAD_POSITIONS !!!")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            print("!!! END ERROR !!!\n")
            self.error_message = f"Failed to load positions: {str(e)}"
            # Mark as loaded even on error to prevent infinite loading
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_positions_loaded()
        finally:
            self.is_loading = False
    
    async def _update_overview_stats(self):
        """Update overview statistics after loading positions"""
        try:
            from web_ui.overview_state import OverviewState
            from web_ui.api_key_state import APIKeyState
            
            overview_state = await self.get_state(OverviewState)
            api_key_state = await self.get_state(APIKeyState)
            
            # Convert positions to dicts for the update method
            positions_data = [
                {
                    'hedge_enabled': pos.hedge_enabled,
                    'total_value_usd': pos.total_value_usd,
                }
                for pos in self.lp_positions
            ]
            
            # Convert API keys to dicts
            api_keys_data = [
                {
                    'is_in_use': key.is_in_use,
                }
                for key in api_key_state.api_keys
            ]
            
            overview_state.update_stats(positions_data, api_keys_data)
        except Exception as e:
            print(f"Error updating overview stats: {e}")

    def fetch_position_data_handler(self, form_data: dict):
        """Immediate feedback handler for fetch position data"""
        # Store form data in state for worker to use
        self._fetch_protocol = form_data.get("protocol", "uniswap_v3").strip()
        self._fetch_network = form_data.get("network", "ethereum").strip()
        self._fetch_nft_id = form_data.get("nft_id", "").strip()
        
        if not self._fetch_nft_id:
            self.error_message = "NFT ID is required"
            return
        
        # Set loading state immediately
        self.is_fetching = True
        
        # Return toast and chain to async worker
        return [
            rx.toast.info("Fetching position data...", duration=5000),
            LPPositionState.fetch_position_data_worker
        ]

    async def fetch_position_data_worker(self):
        """Async worker for fetching position data"""
        try:
            from .blockchain_utils import fetch_uniswap_position
            
            # Fetch position data directly from blockchain (no API needed)
            self.fetched_position_data = await fetch_uniswap_position(self._fetch_network, self._fetch_nft_id)
            
            # Populate form fields with fetched data
            self.protocol = self._fetch_protocol
            self.network = self._fetch_network
            self.nft_id = self._fetch_nft_id
            self.pool_address = self.fetched_position_data.get("pool_address", "")
            self.token0_symbol = self.fetched_position_data.get("token0_symbol", "")
            self.token1_symbol = self.fetched_position_data.get("token1_symbol", "")
            self.fee_tier = self.fetched_position_data.get("fee_tier", "")
            self.position_name = self.fetched_position_data.get("position_name", "")
            
            # Check if USD values are available
            if self.fetched_position_data.get("hl_price_available"):
                self.success_message = "Position data fetched with USD values! Review and confirm to save."
                yield rx.toast.success("Position fetched successfully!", duration=3000)
            else:
                hl_error = self.fetched_position_data.get("hl_price_error", "")
                self.success_message = f"Position data fetched (no USD values: {hl_error}). Review and confirm to save."
                yield rx.toast.warning(f"Position fetched without USD values: {hl_error}", duration=5000)
            
            self.show_confirmation = True
            
        except Exception as e:
            self.error_message = "Failed to fetch position data. Please check the NFT ID and network."
            yield rx.toast.error("Failed to fetch position data. Please check NFT ID/Network.", duration=5000)
        finally:
            self.is_fetching = False
            # Clear temporary state
            self._fetch_network = ""
            self._fetch_nft_id = ""
    
    def save_position_handler(self):
        """Immediate feedback handler for save position"""
        # Validation
        if not self.position_name:
            self.error_message = "Position name is required"
            return
        
        if not self.nft_id:
            self.error_message = "NFT ID is required"
            return
        
        # Check API key availability if hedge is enabled
        if self.hedge_enabled and self.selected_api_key_id:
            # This will be checked asynchronously in the worker
            pass
        
        # Set loading state immediately
        self.is_loading = True
        
        # Return toast and chain to async worker
        return [
            rx.toast.info("Saving position...", duration=5000),
            LPPositionState.save_position_worker
        ]

    async def save_position_worker(self):
        """Async worker for saving position"""
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.error_message = "Not authenticated"
                yield rx.toast.error("Not authenticated", duration=3000)
                return
            
            # Check API key availability if hedge is enabled
            if self.hedge_enabled and self.selected_api_key_id:
                is_available = await self.check_api_key_availability(self.selected_api_key_id)
                if not is_available:
                    self.error_message = "Selected API key is already in use by another position"
                    yield rx.toast.error("API key already in use by another position", duration=5000)
                    return
            
            supabase = get_supabase_client(auth_state.access_token)
            
            # Prepare lp_positions data (legacy table)
            # Normalize pool address for EVM networks
            normalized_pool_address = normalize_address_for_storage(self.pool_address, self.network)
            
            lp_data = {
                "user_id": auth_state.user_id,
                "position_name": self.position_name,
                "protocol": self.protocol,
                "network": self.network,
                "nft_id": self.nft_id,
                "pool_address": normalized_pool_address,
                "token0_symbol": self.token0_symbol,
                "token1_symbol": self.token1_symbol,
                "fee_tier": self.fee_tier,
                "notes": self.notes,
                "is_active": True
            }
            
            # Check if position already exists by unique constraint (user_id, protocol, network, nft_id)
            existing_position = supabase.table("lp_positions").select("id").eq("user_id", auth_state.user_id).eq("protocol", self.protocol).eq("network", self.network).eq("nft_id", self.nft_id).execute()
            
            # Save to lp_positions table
            if existing_position.data:
                # Update existing position
                position_id = existing_position.data[0]["id"]
                supabase.table("lp_positions").update(lp_data).eq("id", position_id).execute()
            else:
                # Insert new position
                result = supabase.table("lp_positions").insert(lp_data).execute()
                position_id = result.data[0]["id"] if result.data else None
            
            # Save hedge configuration to position_configs table
            if position_id:
                await self.save_hedge_config(auth_state.user_id, position_id)
            
            self.success_message = "Position saved successfully!"
            self.clear_form()
            await self.load_positions()
            yield rx.toast.success("Position saved successfully!", duration=3000)
        except Exception as e:
            print(f"Error saving position: {e}")
            import traceback
            traceback.print_exc()
            self.error_message = f"Failed to save position: {str(e)}"
            yield rx.toast.error(f"Failed to save position: {str(e)}", duration=5000)
        finally:
            self.is_loading = False
    
    async def save_hedge_config(self, user_id: str, position_id: str):
        """Save hedge configuration to position_configs table"""
        print("\n=== SAVE_HEDGE_CONFIG START ===")
        print(f"user_id={user_id}, position_id={position_id}")
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            supabase = get_supabase_client(auth_state.access_token)
            
            # Get wallet ID from selected wallet name
            wallet_id = None
            print(f"selected_hedge_wallet={self.selected_hedge_wallet}")
            if self.selected_hedge_wallet and self.selected_hedge_wallet != "None":
                # Extract account name from "Account Name (Exchange)" format
                account_name = self.selected_hedge_wallet.split(" (")[0]
                print(f"Looking up API key: account_name={account_name}")
                wallet_response = supabase.table("user_api_keys").select("id").eq("user_id", user_id).eq("account_name", account_name).execute()
                if wallet_response.data:
                    wallet_id = wallet_response.data[0]["id"]
                    print(f"Found wallet_id={wallet_id}")
                else:
                    print("No wallet found for account_name")
            else:
                print("No wallet selected or 'None' selected - setting wallet_id to NULL")
            
            # Check if config exists to preserve existing values when editing
            print(f"Checking for existing config: protocol={self.protocol}, network={self.network}, nft_id={self.nft_id}")
            existing = supabase.table("position_configs").select("*").eq("user_id", user_id).eq("protocol", self.protocol).eq("network", self.network).eq("nft_id", self.nft_id).execute()
            existing_config = existing.data[0] if existing.data else {}
            print(f"Existing config found: {bool(existing_config)}")
            
            # Prepare position_configs data (matching actual database schema)
            # Normalize addresses for EVM networks
            normalized_pool_address = normalize_address_for_storage(self.pool_address, self.network)
            normalized_token0_address = normalize_address_for_storage(
                self.fetched_position_data.get("token0_address", "") or existing_config.get("token0_address", ""),
                self.network
            )
            normalized_token1_address = normalize_address_for_storage(
                self.fetched_position_data.get("token1_address", "") or existing_config.get("token1_address", ""),
                self.network
            )
            
            config_data = {
                "user_id": user_id,
                "position_name": self.position_name,
                "notes": self.notes,
                "status": "active",
                "protocol": self.protocol,
                "network": self.network,
                "nft_id": self.nft_id,
                "pool_address": normalized_pool_address,
                "token0_symbol": self.token0_symbol,
                "token0_address": normalized_token0_address,
                "token1_symbol": self.token1_symbol,
                "token1_address": normalized_token1_address,
                "fee_tier": int(self.fee_tier) if self.fee_tier and self.fee_tier.isdigit() else 3000,  # INTEGER not VARCHAR
                "entry_price": self.fetched_position_data.get("current_price", 0) or existing_config.get("entry_price", 0),
                "position_size_usd": float(self.fetched_position_data.get("position_value_usd", 0)) or existing_config.get("position_size_usd", 0),
                "pa": self.fetched_position_data.get("pa") or existing_config.get("pa"),
                "pb": self.fetched_position_data.get("pb") or existing_config.get("pb"),
                "hedge_enabled": self.hedge_enabled,
                "hedge_token0": self.hedge_token0,
                "hedge_token1": self.hedge_token1,
                "target_hedge_ratio": float(self.hedge_ratio),  # Schema default is 80.00, store as-is
                "hl_api_key_id": wallet_id,
                "use_dynamic_hedging": self.use_dynamic_hedging,
                "dynamic_profile": self.dynamic_profile,
                "rebalance_cooldown_hours": float(self.rebalance_cooldown_hours),
                "delta_drift_threshold_pct": float(self.delta_drift_threshold_pct),  # Schema default is 0.38, store as-is
                "down_threshold": float(self.down_threshold),
                "bounce_threshold": float(self.bounce_threshold),
                "lookback_hours": float(self.lookback_hours),
                "drift_min_pct_of_capital": float(self.drift_min_pct_of_capital),
                "max_hedge_drift_pct": float(self.max_hedge_drift_pct),
                "hedge_tokens": self.fetched_position_data.get("hedge_tokens", existing_config.get("hedge_tokens", {})),  # JSONB with HL metadata
            }
            
            # Debug: Print numeric values to identify overflow
            print(f"DEBUG - Numeric values:")
            print(f"  entry_price: {config_data.get('entry_price')}")
            print(f"  position_size_usd: {config_data.get('position_size_usd')}")
            print(f"  target_hedge_ratio: {config_data.get('target_hedge_ratio')}")
            print(f"  rebalance_cooldown_hours: {config_data.get('rebalance_cooldown_hours')}")
            print(f"  delta_drift_threshold_pct: {config_data.get('delta_drift_threshold_pct')}")
            print(f"  down_threshold: {config_data.get('down_threshold')}")
            print(f"  bounce_threshold: {config_data.get('bounce_threshold')}")
            print(f"  lookback_hours: {config_data.get('lookback_hours')}")
            print(f"  drift_min_pct_of_capital: {config_data.get('drift_min_pct_of_capital')}")
            print(f"  max_hedge_drift_pct: {config_data.get('max_hedge_drift_pct')}")
            
            # Update or insert based on whether config already exists
            if existing_config:
                # Update existing config
                print(f"Updating existing config id={existing.data[0]['id']}")
                result = supabase.table("position_configs").update(config_data).eq("id", existing.data[0]["id"]).execute()
                print(f"Update result: {result}")
            else:
                # Insert new config
                print(f"Inserting new config with data keys: {list(config_data.keys())}")
                result = supabase.table("position_configs").insert(config_data).execute()
                print(f"Insert result: {result}")
            print("=== SAVE_HEDGE_CONFIG END ===\n")
                
        except Exception as e:
            print(f"\n!!! ERROR IN SAVE_HEDGE_CONFIG !!!")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            print("!!! END ERROR !!!\n")
            # Re-raise to propagate error to parent
            raise Exception(f"Failed to save hedge configuration: {str(e)}")
    
    async def load_hedge_config(self, position_id: str):
        """Load hedge configuration from position_configs table"""
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            supabase = get_supabase_client(auth_state.access_token)
            
            # Get position to find network and nft_id
            position = next((p for p in self.lp_positions if p.id == position_id), None)
            if not position:
                return
            
            # Load config from position_configs
            config_response = supabase.table("position_configs").select("*").eq("network", position.network).eq("nft_id", position.nft_id).execute()
            
            if config_response.data:
                config = config_response.data[0]
                
                # Load hedge settings
                self.hedge_enabled = config.get("hedge_enabled", False)
                self.hedge_token0 = config.get("hedge_token0", True)
                self.hedge_token1 = config.get("hedge_token1", True)
                self.hedge_ratio = int(config.get("target_hedge_ratio", 80))
                self.use_dynamic_hedging = config.get("use_dynamic_hedging", False)
                self.dynamic_profile = config.get("dynamic_profile", "balanced")
                self.rebalance_cooldown_hours = float(config.get("rebalance_cooldown_hours", 8.0))
                self.delta_drift_threshold_pct = float(config.get("delta_drift_threshold_pct", 0.38))
                self.down_threshold = float(config.get("down_threshold", -0.065))
                self.bounce_threshold = float(config.get("bounce_threshold", -0.038))
                
                # Load wallet selection
                if config.get("hl_api_key_id"):
                    wallet_response = supabase.table("user_api_keys").select("account_name,exchange").eq("id", config["hl_api_key_id"]).execute()
                    if wallet_response.data:
                        wallet = wallet_response.data[0]
                        self.selected_hedge_wallet = f"{wallet['account_name']} ({wallet['exchange']})"
                
        except Exception as e:
            pass
    
    async def load_chart_data(self, position_id: str, hours: int = 24):
        """Load chart data for a position from QuestDB"""
        try:
            from web_ui.questdb_utils import get_position_value_history
            
            print(f"\n>>> load_chart_data called with position_id='{position_id}', hours={hours}")
            
            self.chart_loading = True
            self.selected_chart_position_id = position_id
            self.chart_hours = hours
            
            # Fetch data from QuestDB
            print(f">>> Calling get_position_value_history...")
            history = get_position_value_history(position_id, hours)
            
            print(f">>> Received {len(history)} data points from QuestDB")
            print(f">>> Setting chart_data and opening dialog...")
            
            # Format for Reflex charts
            self.chart_data = history
            self.chart_loading = False
            self.show_chart = True
            
            print(f">>> Chart state updated: chart_data length={len(self.chart_data)}, show_chart={self.show_chart}")
            
        except Exception as e:
            print(f"❌ Error loading chart data: {e}")
            import traceback
            traceback.print_exc()
            self.chart_loading = False
            self.chart_data = []
            self.show_chart = False
    
    def set_show_chart(self, value: bool):
        """Setter for show_chart state variable"""
        self.show_chart = value
    
    def close_chart(self):
        """Close the chart dialog"""
        self.show_chart = False
    
    def open_activity_dialog(self, position_id: str):
        """Open activity dialog for a position"""
        self.selected_activity_position_id = position_id
        self.show_activity_dialog = True
    
    def close_activity_dialog(self):
        """Close activity dialog"""
        self.show_activity_dialog = False
        self.selected_activity_position_id = ""
    
    async def toggle_active(self, position_id: str):
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            
            position = next((p for p in self.lp_positions if p.id == position_id), None)
            if position:
                new_status = not position.is_active
                supabase.table("lp_positions").update({"is_active": new_status}).eq("id", position_id).eq("user_id", auth_state.user_id).execute()
                await self.load_positions()
        except Exception as e:
            self.error_message = "Failed to update status. Please try again."
