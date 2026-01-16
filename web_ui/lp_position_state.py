import reflex as rx
from pydantic import BaseModel
from .auth import get_supabase_client


class LPPositionData(BaseModel):
    id: str
    position_name: str
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


class LPPositionState(rx.State):
    lp_positions: list[LPPositionData] = []
    selected_position_id: str = ""
    position_name: str = ""
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
    
    # Loading state
    loading_position_id: str = ""
    is_fetching: bool = False
    
    hedge_ratio: int = 80
    selected_hedge_wallet: str = ""
    _cached_wallets: list[str] = []  # Cache for available wallets
    
    # Dynamic hedging fields
    use_dynamic_hedging: bool = False
    dynamic_profile: str = "balanced"
    rebalance_cooldown_hours: float = 8.0
    delta_drift_threshold_pct: float = 0.38
    down_threshold: float = -0.065
    bounce_threshold: float = -0.038
    
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    def set_position_name(self, value: str):
        self.position_name = value
    
    def set_notes(self, value: str):
        self.notes = value
    
    def toggle_hedge_enabled(self):
        self.hedge_enabled = not self.hedge_enabled
    
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
    
    def set_hedge_wallet(self, value: str):
        self.selected_hedge_wallet = value
    
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
        delta = self.fetched_position_data.get('position_delta', 0.0)
        return delta * (self.hedge_ratio / 100.0)
    
    @rx.var
    def estimated_hedge_token1(self) -> float:
        """Calculate estimated hedge amount for token1"""
        if not self.fetched_position_data or not self.hedge_enabled or not self.hedge_token1:
            return 0.0
        token1_amount = self.fetched_position_data.get('token1_amount', 0.0)
        return token1_amount * (self.hedge_ratio / 100.0)
    
    async def load_wallets(self):
        """Load available API keys for wallet selector"""
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            print(f"DEBUG load_wallets: auth_state.is_authenticated = {auth_state.is_authenticated}")
            print(f"DEBUG load_wallets: auth_state.user_id = {auth_state.user_id}")
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                print("DEBUG load_wallets: Not authenticated")
                return
            
            supabase = get_supabase_client()
            response = supabase.table("user_api_keys").select("id,account_name,exchange").eq("user_id", auth_state.user_id).eq("is_active", True).execute()
            print(f"DEBUG load_wallets: response.data = {response.data}")
            
            if response.data:
                wallets = [f"{key['account_name']} ({key['exchange']})" for key in response.data]
                print(f"DEBUG load_wallets: wallets = {wallets}")
                # Store in cache
                self._cached_wallets = wallets
                # Auto-select first wallet if none selected
                if wallets and not self.selected_hedge_wallet:
                    self.selected_hedge_wallet = wallets[0]
                    print(f"DEBUG load_wallets: Auto-selected wallet = {self.selected_hedge_wallet}")
        except Exception as e:
            print(f"Error loading wallets: {e}")
            import traceback
            traceback.print_exc()
    
    @rx.var
    def available_wallets(self) -> list[str]:
        """Get list of available API keys for wallet selector"""
        print(f"DEBUG available_wallets: Returning cached wallets = {self._cached_wallets}")
        return self._cached_wallets
    
    def clear_form(self):
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

        try:
            # 3. Fetch remote data
            form_data = {
                "network": self.network,
                "nft_id": self.nft_id
            }
            await self.fetch_position_data(form_data)
            await self.load_hedge_config(position_id)
            
            yield rx.toast.success("Position data loaded!", duration=3000)
        except Exception as e:
            yield rx.toast.error(f"Failed to load: {str(e)}", duration=5000)
        finally:
            self.loading_position_id = ""

    def delete_position(self, position_id: str):
        """Immediate feedback handler"""
        self.loading_position_id = position_id
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
            
            supabase = get_supabase_client()
            position = next((p for p in self.lp_positions if p.id == position_id), None)
            position_name = position.position_name if position else "position"
            
            supabase.table("lp_positions").delete().eq("id", position_id).eq("user_id", auth_state.user_id).execute()
            
            await self.load_positions()
            if self.selected_position_id == position_id:
                self.clear_form()
            
            yield rx.toast.success(f"Deleted '{position_name}'!", duration=3000)
        except Exception as e:
            yield rx.toast.error(f"Failed to delete: {str(e)}", duration=5000)
        finally:
            self.is_loading = False
            self.loading_position_id = ""

    async def load_positions(self):
        self.is_loading = True
        self.clear_messages()
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.error_message = "Not authenticated"
                self.is_loading = False
                return
            
            supabase = get_supabase_client()
            
            # Fetch positions for current user
            response = supabase.table("lp_positions").select("*").eq("user_id", auth_state.user_id).execute()
            
            self.lp_positions = []
            if response.data:
                # Fetch config data to merge
                config_response = supabase.table("position_configs").select("*").eq("user_id", auth_state.user_id).execute()
                config_map = {f"{c['network']}_{c['nft_id']}": c for c in config_response.data} if config_response.data else {}
                
                for pos_data in response.data:
                    # Look up config
                    config_key = f"{pos_data['network']}_{pos_data['nft_id']}"
                    config = config_map.get(config_key, {})
                    
                    position = LPPositionData(
                        id=pos_data["id"],
                        position_name=pos_data["position_name"],
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
                        position_size_usd=float(config.get("position_size_usd", 0.0)),
                        position_value_formatted=f"${float(config.get('position_size_usd', 0.0)):,.2f}",
                        hedge_enabled=config.get("hedge_enabled", False),
                        target_hedge_ratio=float(config.get("target_hedge_ratio", 0.0)),
                        hedge_details=f"Hedge: {int(float(config.get('target_hedge_ratio', 0.0)))}%" if config.get("hedge_enabled", False) else "Hedge: Disabled",
                    )
                    self.lp_positions.append(position)
            else:
                self.lp_positions = []
                
        except Exception as e:
            self.error_message = f"Error loading LP positions: {str(e)}"
        finally:
            self.is_loading = False

    async def fetch_position_data(self, form_data: dict):
        """Fetch position data from blockchain before saving"""
        self.clear_messages()
        
        network = form_data.get("network", "ethereum").strip()
        nft_id = form_data.get("nft_id", "").strip()
        
        if not nft_id:
            self.error_message = "NFT ID is required"
            return
        
        try:
            from .blockchain_utils import fetch_uniswap_position
            
            print(f"DEBUG: Fetching position data for NFT ID {nft_id} on {network}")
            
            # Fetch position data directly from blockchain (no API needed)
            self.fetched_position_data = await fetch_uniswap_position(network, nft_id)
            
            # Populate form fields with fetched data
            self.network = network
            self.nft_id = nft_id
            self.pool_address = self.fetched_position_data.get("pool_address", "")
            self.token0_symbol = self.fetched_position_data.get("token0_symbol", "")
            self.token1_symbol = self.fetched_position_data.get("token1_symbol", "")
            self.fee_tier = self.fetched_position_data.get("fee_tier", "")
            self.position_name = self.fetched_position_data.get("position_name", "")
            
            # Check if USD values are available
            if self.fetched_position_data.get("hl_price_available"):
                self.success_message = "Position data fetched with USD values! Review and confirm to save."
            else:
                hl_error = self.fetched_position_data.get("hl_price_error", "")
                self.success_message = f"Position data fetched (no USD values: {hl_error}). Review and confirm to save."
            
            self.show_confirmation = True
            
        except Exception as e:
            self.error_message = f"Error fetching position data: {str(e)}"
        finally:
            pass
    
    async def save_position(self):
        """Save the confirmed position to database"""
        self.is_loading = True
        self.clear_messages()
        
        if not self.position_name:
            self.error_message = "Position name is required"
            self.is_loading = False
            return
        
        if not self.nft_id:
            self.error_message = "NFT ID is required"
            self.is_loading = False
            return
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.error_message = "Not authenticated"
                self.is_loading = False
                return
            
            supabase = get_supabase_client()
            
            # Prepare lp_positions data (legacy table)
            lp_data = {
                "user_id": auth_state.user_id,
                "position_name": self.position_name,
                "network": self.network,
                "nft_id": self.nft_id,
                "pool_address": self.pool_address,
                "token0_symbol": self.token0_symbol,
                "token1_symbol": self.token1_symbol,
                "fee_tier": self.fee_tier,
                "notes": self.notes,
                "is_active": True
            }
            
            # Save to lp_positions table
            if self.is_editing and self.selected_position_id:
                supabase.table("lp_positions").update(lp_data).eq("id", self.selected_position_id).execute()
                position_id = self.selected_position_id
            else:
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
            self.error_message = f"Error saving position: {str(e)}"
            yield rx.toast.error(f"Failed to save: {str(e)}", duration=5000)
        finally:
            self.is_loading = False
    
    async def save_hedge_config(self, user_id: str, position_id: str):
        """Save hedge configuration to position_configs table"""
        try:
            supabase = get_supabase_client()
            
            # Get wallet ID from selected wallet name
            wallet_id = None
            if self.selected_hedge_wallet:
                # Extract account name from "Account Name (Exchange)" format
                account_name = self.selected_hedge_wallet.split(" (")[0]
                wallet_response = supabase.table("user_api_keys").select("id").eq("user_id", user_id).eq("account_name", account_name).execute()
                if wallet_response.data:
                    wallet_id = wallet_response.data[0]["id"]
            
            # Prepare position_configs data
            config_data = {
                "user_id": user_id,
                "position_name": self.position_name,
                "notes": self.notes,
                "status": "active",
                "network": self.network,
                "nft_id": self.nft_id,
                "pool_address": self.pool_address,
                "token0_symbol": self.token0_symbol,
                "token0_address": self.fetched_position_data.get("token0_address", ""),
                "token1_symbol": self.token1_symbol,
                "token1_address": self.fetched_position_data.get("token1_address", ""),
                "fee_tier": int(self.fee_tier) if self.fee_tier and self.fee_tier.isdigit() else 3000,
                "entry_price": self.fetched_position_data.get("current_price", 0),
                "position_size_usd": float(self.fetched_position_data.get("position_value_usd", 0)),
                "hedge_enabled": self.hedge_enabled,
                "hedge_token0": self.hedge_token0,
                "hedge_token1": self.hedge_token1,
                "target_hedge_ratio": float(self.hedge_ratio),
                "hedge_wallet_id": wallet_id,
                "use_dynamic_hedging": self.use_dynamic_hedging,
                "dynamic_profile": self.dynamic_profile,
                "rebalance_cooldown_hours": float(self.rebalance_cooldown_hours),
                "delta_drift_threshold_pct": float(self.delta_drift_threshold_pct),
                "down_threshold": float(self.down_threshold),
                "bounce_threshold": float(self.bounce_threshold),
            }
            
            # Check if config exists for this position
            existing = supabase.table("position_configs").select("id").eq("user_id", user_id).eq("network", self.network).eq("nft_id", self.nft_id).execute()
            
            if existing.data:
                # Update existing config
                supabase.table("position_configs").update(config_data).eq("id", existing.data[0]["id"]).execute()
            else:
                # Insert new config
                supabase.table("position_configs").insert(config_data).execute()
                
        except Exception as e:
            print(f"Error saving hedge config: {e}")
            # Don't fail the whole save if hedge config fails
    
    async def load_hedge_config(self, position_id: str):
        """Load hedge configuration from position_configs table"""
        try:
            supabase = get_supabase_client()
            
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
                if config.get("hedge_wallet_id"):
                    wallet_response = supabase.table("user_api_keys").select("account_name,exchange").eq("id", config["hedge_wallet_id"]).execute()
                    if wallet_response.data:
                        wallet = wallet_response.data[0]
                        self.selected_hedge_wallet = f"{wallet['account_name']} ({wallet['exchange']})"
                
        except Exception as e:
            print(f"Error loading hedge config: {e}")
    
    async def toggle_active(self, position_id: str):
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            supabase = get_supabase_client()
            
            position = next((p for p in self.lp_positions if p.id == position_id), None)
            if position:
                new_status = not position.is_active
                supabase.table("lp_positions").update({"is_active": new_status}).eq("id", position_id).eq("user_id", auth_state.user_id).execute()
                await self.load_positions()
        except Exception as e:
            self.error_message = f"Error toggling status: {str(e)}"
