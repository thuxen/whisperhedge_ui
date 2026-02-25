import reflex as rx
from pydantic import BaseModel
from .auth import get_supabase_client
from .crypto_utils import encrypt_value, decrypt_value
from .hl_utils import get_hl_account_balance
from .address_utils import normalize_address_for_storage


class APIKeyData(BaseModel):
    id: str
    account_name: str
    exchange: str
    api_key: str = ""
    api_secret: str
    is_master_account: bool = True
    wallet_address: str = ""
    subaccount_name: str = ""
    private_key: str = ""
    notes: str = ""
    is_active: bool = True
    created_at: str = ""
    account_value: float = 0.0
    available_balance: float = 0.0
    balance_loading: bool = False
    balance_error: str = ""
    is_in_use: bool = False
    used_by_position: str = ""


class APIKeyState(rx.State):
    api_keys: list[APIKeyData] = []
    selected_key_id: str = ""
    account_name: str = ""
    exchange: str = "hyperliquid"
    api_key: str = ""
    api_secret: str = ""
    is_master_account: bool = True
    wallet_address: str = ""
    subaccount_name: str = ""
    private_key: str = ""
    notes: str = ""
    is_loading: bool = False
    loading_key_id: str = ""  # Track which key is being operated on
    _save_form_data: dict = {}  # Temporary storage for save form data
    error_message: str = ""
    success_message: str = ""
    show_api_secret: bool = False
    show_private_key: bool = False
    is_editing: bool = False
    
    # Delete confirmation for in-use keys
    show_delete_confirmation: bool = False
    key_to_delete: str = ""
    key_to_delete_name: str = ""
    key_to_delete_position: str = ""
    
    def clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    def toggle_secret_visibility(self):
        self.show_api_secret = not self.show_api_secret
    
    def toggle_private_key_visibility(self):
        self.show_private_key = not self.show_private_key
    
    def set_exchange(self, value: str):
        self.exchange = value
    
    def set_is_master_account(self, checked: bool):
        self.is_master_account = checked
        if checked:
            self.wallet_address = ""
    
    def clear_form(self):
        """Clear form and reset to add mode"""
        self.selected_key_id = ""
        self.account_name = ""
        self.exchange = "hyperliquid"
        self.api_key = ""
        self.api_secret = ""
        self.is_master_account = True
        self.wallet_address = ""
        self.subaccount_name = ""
        self.private_key = ""
        self.notes = ""
        self.is_editing = False
        self.show_api_secret = False
        self.show_private_key = False
        self.clear_messages()
    
    def cancel_edit(self):
        """Cancel editing with toast notification"""
        self.clear_form()
        return rx.toast.info("Cancelled editing", duration=2000)
    
    def edit_api_key(self, key_id: str):
        """Immediate feedback handler for editing API key"""
        # Set loading state immediately
        self.loading_key_id = key_id
        
        # Find and populate form data
        key_data = next((k for k in self.api_keys if k.id == key_id), None)
        if key_data:
            self.selected_key_id = key_id
            self.account_name = key_data.account_name
            self.exchange = key_data.exchange
            self.api_key = key_data.api_key
            self.api_secret = key_data.api_secret
            self.is_master_account = key_data.is_master_account
            self.wallet_address = key_data.wallet_address
            self.subaccount_name = key_data.subaccount_name
            self.private_key = key_data.private_key
            self.notes = key_data.notes
            self.is_editing = True
        
        # Clear loading state after a short delay (edit is instant)
        return [
            rx.toast.info("Loading trading account for editing...", duration=1000),
            APIKeyState.clear_edit_loading
        ]
    
    def clear_edit_loading(self):
        """Clear loading state for edit operation"""
        self.loading_key_id = ""
    
    async def load_api_keys(self):
        self.is_loading = True
        self.clear_messages()
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.is_loading = False
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            response = supabase.table("user_api_keys").select("*").eq("user_id", auth_state.user_id).order("created_at", desc=True).execute()
            
            if response.data:
                self.api_keys = []
                for key_data in response.data:
                    # Check if this API key is used by any position
                    try:
                        position_response = supabase.table("position_configs").select("position_name").eq("hl_api_key_id", key_data["id"]).execute()
                        used_by_position = position_response.data[0]["position_name"] if position_response.data else ""
                        is_in_use = len(position_response.data) > 0
                    except Exception as e:
                        # If position_configs table doesn't exist or query fails, assume not in use
                        print(f"Warning: Could not check API key usage: {e}")
                        used_by_position = ""
                        is_in_use = False
                    
                    decrypted_key = APIKeyData(
                        id=key_data["id"],
                        account_name=key_data["account_name"],
                        exchange=key_data["exchange"],
                        api_key=decrypt_value(key_data["api_key"]) if key_data.get("api_key") else "",
                        api_secret=decrypt_value(key_data["api_secret"]),
                        is_master_account=key_data.get("is_master_account", True),
                        wallet_address=key_data.get("wallet_address", ""),
                        subaccount_name=key_data.get("subaccount_name", ""),
                        private_key=decrypt_value(key_data["private_key"]) if key_data.get("private_key") else "",
                        notes=key_data.get("notes", ""),
                        is_active=key_data.get("is_active", True),
                        created_at=key_data["created_at"],
                        is_in_use=is_in_use,
                        used_by_position=used_by_position,
                    )
                    self.api_keys.append(decrypted_key)
            else:
                self.api_keys = []
            
            # Update overview stats
            await self._update_overview_stats()
            
            # Mark API keys as loaded for dashboard loading state
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_api_keys_loaded()
                
        except Exception as e:
            self.error_message = "Failed to load API keys. Please try again."
            # Mark as loaded even on error to prevent infinite loading
            from web_ui.dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_api_keys_loaded()
        finally:
            self.is_loading = False
    
    async def _update_overview_stats(self):
        """Update overview statistics after loading API keys"""
        try:
            from web_ui.overview_state import OverviewState
            from web_ui.lp_position_state import LPPositionState
            
            overview_state = await self.get_state(OverviewState)
            lp_position_state = await self.get_state(LPPositionState)
            
            # Convert positions to dicts for the update method
            positions_data = [
                {
                    'hedge_enabled': pos.hedge_enabled,
                    'total_value_usd': pos.total_value_usd,
                }
                for pos in lp_position_state.lp_positions
            ]
            
            # Convert API keys to dicts
            api_keys_data = [
                {
                    'is_in_use': key.is_in_use,
                }
                for key in self.api_keys
            ]
            
            overview_state.update_stats(positions_data, api_keys_data)
        except Exception as e:
            print(f"Error updating overview stats from API keys: {e}")
    
    def fetch_balance(self, key_id: str):
        """Immediate feedback handler for fetching balance"""
        # Find the key and get account name
        key_data = next((k for k in self.api_keys if k.id == key_id), None)
        if not key_data:
            return
        
        # Set loading state immediately
        key_data.balance_loading = True
        key_data.balance_error = ""
        # Reset balance values to ensure accurate status
        key_data.account_value = 0.0
        key_data.available_balance = 0.0
        
        # Return toast and chain to async worker
        return [
            rx.toast.info(f"Fetching balance for {key_data.account_name}...", duration=5000),
            APIKeyState.fetch_balance_worker
        ]
    
    async def fetch_balance_worker(self):
        """Async worker for fetching balance"""
        try:
            # Find the key that's being loaded
            key_data = next((k for k in self.api_keys if k.balance_loading), None)
            if not key_data:
                return
            
            # Fetch balance from Hyperliquid
            if key_data.exchange.lower() == "hyperliquid":
                if not key_data.wallet_address:
                    key_data.balance_error = "No wallet address"
                    key_data.balance_loading = False
                    return
                
                # Fetch balance using wallet address only (read-only query)
                balance_info = get_hl_account_balance(key_data.wallet_address)
                
                if balance_info:
                    key_data.account_value = balance_info['account_value']
                    key_data.available_balance = balance_info['available']
                    
                    # Save balance to database
                    try:
                        from web_ui.state import AuthState
                        auth_state = await self.get_state(AuthState)
                        supabase = get_supabase_client(auth_state.access_token)
                        
                        supabase.table("user_api_keys").update({
                            "account_value": balance_info['account_value'],
                            "available_balance": balance_info['available']
                        }).eq("id", key_data.id).execute()
                    except Exception as e:
                        print(f"Failed to save balance to database: {e}")
                    
                    yield rx.toast.success(f"Balance fetched for {key_data.account_name}", duration=3000)
                else:
                    # Check if it's likely an invalid API key/wallet
                    if not key_data.wallet_address or len(key_data.wallet_address) < 10:
                        key_data.balance_error = "Invalid wallet address"
                        yield rx.toast.error(f"Invalid wallet address for {key_data.account_name}", duration=5000)
                    else:
                        key_data.balance_error = "Invalid API key or wallet"
                        yield rx.toast.error(f"Invalid API key or wallet address for {key_data.account_name}", duration=5000)
            else:
                key_data.balance_error = "Only Hyperliquid supported"
                yield rx.toast.error("Only Hyperliquid is supported for balance checking", duration=5000)
            
            key_data.balance_loading = False
            
        except Exception as e:
            key_data = next((k for k in self.api_keys if k.balance_loading), None)
            if key_data:
                key_data.balance_loading = False
                key_data.balance_error = f"Error: {str(e)}"
                yield rx.toast.error(f"Error fetching balance: {str(e)}", duration=5000)
    
    def save_api_keys_handler(self, form_data: dict):
        """Immediate feedback handler for saving API keys"""
        # Validation
        account_name = form_data.get("account_name", "").strip()
        exchange = form_data.get("exchange", "hyperliquid").strip()
        api_key = form_data.get("api_key", "").strip()
        api_secret = form_data.get("api_secret", "").strip()
        
        if not account_name:
            self.error_message = "Account name is required"
            return
        
        if not api_secret:
            self.error_message = "API Secret is required"
            return
        
        if exchange == "hyperliquid":
            if not form_data.get("wallet_address", "").strip():
                self.error_message = "Wallet address is required for Hyperliquid (needed for balance/position queries)"
                return
        else:
            if not api_key:
                self.error_message = f"API Key is required for {exchange}"
                return
        
        # Store form data for worker
        self._save_form_data = form_data
        
        # Set loading state immediately
        self.is_loading = True
        
        # Return toast and chain to async worker
        action = "Updating" if self.is_editing else "Saving"
        return [
            rx.toast.info(f"{action} trading account '{account_name}'...", duration=5000),
            APIKeyState.save_api_keys_worker
        ]
    
    async def save_api_keys_worker(self):
        """Async worker for saving API keys"""
        try:
            form_data = self._save_form_data
            
            account_name = form_data.get("account_name", "").strip()
            exchange = form_data.get("exchange", "hyperliquid").strip()
            api_key = form_data.get("api_key", "").strip()
            api_secret = form_data.get("api_secret", "").strip()
            
            # Handle checkbox - it might be a string "true"/"false" or boolean
            is_master_checkbox = form_data.get("is_master_account", True)
            if isinstance(is_master_checkbox, str):
                is_master_account = is_master_checkbox.lower() == "true"
            else:
                is_master_account = bool(is_master_checkbox)
            
            wallet_address = form_data.get("wallet_address", "").strip()
            subaccount_name = form_data.get("subaccount_name", "").strip()
            private_key = form_data.get("private_key", "").strip()
            notes = form_data.get("notes", "").strip()
            
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.error_message = "Not authenticated"
                yield rx.toast.error("Not authenticated", duration=3000)
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            encrypted_key = encrypt_value(api_key) if api_key else None
            encrypted_secret = encrypt_value(api_secret)
            encrypted_private_key = encrypt_value(private_key) if private_key else None
            
            # Check for duplicate API key for this user (when creating new)
            if not self.is_editing and encrypted_key:
                print(f"[SAVE API KEY] Checking for duplicate API key for user {auth_state.user_id}", flush=True)
                duplicate_check = supabase.table("user_api_keys").select("id,account_name").eq("user_id", auth_state.user_id).eq("api_key", encrypted_key).execute()
                
                if duplicate_check.data:
                    existing_account = duplicate_check.data[0]["account_name"]
                    print(f"[SAVE API KEY] Duplicate found - already exists as '{existing_account}'", flush=True)
                    self.error_message = f"This trading account is already added as '{existing_account}'"
                    yield rx.toast.error(f"This trading account already exists as '{existing_account}'", duration=5000)
                    return
                print(f"[SAVE API KEY] No duplicate found, proceeding with save", flush=True)
            
            # Normalize wallet address for EVM networks (currently all Hyperliquid = EVM)
            normalized_wallet_address = normalize_address_for_storage(wallet_address, "ethereum") if wallet_address else wallet_address
            
            data = {
                "user_id": auth_state.user_id,
                "account_name": account_name,
                "exchange": exchange,
                "api_key": encrypted_key,
                "api_secret": encrypted_secret,
                "is_master_account": is_master_account,
                "wallet_address": normalized_wallet_address,
                "subaccount_name": subaccount_name,
                "private_key": encrypted_private_key,
                "notes": notes,
                "is_active": True
            }
            
            if self.is_editing and self.selected_key_id:
                supabase.table("user_api_keys").update(data).eq("id", self.selected_key_id).execute()
                self.success_message = f"Trading account '{account_name}' updated successfully!"
                yield rx.toast.success(f"'{account_name}' trading account updated successfully!", duration=3000)
            else:
                supabase.table("user_api_keys").insert(data).execute()
                self.success_message = f"Trading account '{account_name}' saved successfully!"
                yield rx.toast.success(f"'{account_name}' trading account saved successfully!", duration=3000)
            
            await self.load_api_keys()
            self.clear_form()
            
        except Exception as e:
            self.error_message = "Failed to save trading account. Please try again."
            yield rx.toast.error("Failed to save trading account. Please try again.", duration=5000)
        finally:
            self.is_loading = False
            self._save_form_data = {}
    
    def delete_api_key(self, key_id: str):
        """Check if key is in use and show confirmation if needed"""
        key_data = next((k for k in self.api_keys if k.id == key_id), None)
        
        if key_data and key_data.is_in_use:
            # Show confirmation dialog for in-use keys
            self.key_to_delete = key_id
            self.key_to_delete_name = key_data.account_name
            self.key_to_delete_position = key_data.used_by_position
            self.show_delete_confirmation = True
            return
        
        # Not in use, proceed with deletion immediately
        self.loading_key_id = key_id
        account_name = key_data.account_name if key_data else "account"
        
        # Return toast and chain to async worker
        return [
            rx.toast.info(f"Deleting '{account_name}' trading account...", duration=5000),
            APIKeyState.delete_api_key_worker
        ]
    
    def cancel_delete(self):
        """User cancelled deletion"""
        self.show_delete_confirmation = False
        self.key_to_delete = ""
        self.key_to_delete_name = ""
        self.key_to_delete_position = ""
    
    async def delete_api_key_worker(self):
        """Async worker for deleting API key"""
        try:
            print(f"[DELETE API KEY] Starting deletion for key_id: {self.loading_key_id}", flush=True)
            
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                print(f"[DELETE API KEY ERROR] Not authenticated", flush=True)
                self.error_message = "Not authenticated"
                yield rx.toast.error("Not authenticated", duration=3000)
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            key_data = next((k for k in self.api_keys if k.id == self.loading_key_id), None)
            account_name = key_data.account_name if key_data else "account"
            
            print(f"[DELETE API KEY] Deleting key for account: {account_name}", flush=True)
            supabase.table("user_api_keys").delete().eq("id", self.loading_key_id).eq("user_id", auth_state.user_id).execute()
            print(f"[DELETE API KEY] Database deletion successful", flush=True)
            
            self.success_message = f"Trading account '{account_name}' deleted successfully!"
            await self.load_api_keys()
            print(f"[DELETE API KEY] Reloaded API keys", flush=True)
            
            if self.selected_key_id == self.loading_key_id:
                self.clear_form()
            
            yield rx.toast.success(f"'{account_name}' trading account deleted successfully!", duration=3000)
            print(f"[DELETE API KEY] Deletion complete", flush=True)
            
        except Exception as e:
            print(f"[DELETE API KEY ERROR] Exception: {e}", flush=True)
            import traceback
            traceback.print_exc()
            self.error_message = "Failed to delete trading account. Please try again."
            yield rx.toast.error("Failed to delete trading account. Please try again.", duration=5000)
        finally:
            self.loading_key_id = ""
    
    async def toggle_active(self, key_id: str):
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            supabase = get_supabase_client(auth_state.access_token)
            
            key_data = next((k for k in self.api_keys if k.id == key_id), None)
            if key_data:
                new_status = not key_data.is_active
                supabase.table("user_api_keys").update({"is_active": new_status}).eq("id", key_id).eq("user_id", auth_state.user_id).execute()
            
            await self.load_api_keys()
        except Exception as e:
            self.error_message = "Failed to update status. Please try again."
