import reflex as rx
from pydantic import BaseModel
from .auth import get_supabase_client
from .crypto_utils import encrypt_value, decrypt_value
from .hl_utils import get_hl_account_balance


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
    error_message: str = ""
    success_message: str = ""
    show_api_secret: bool = False
    show_private_key: bool = False
    is_editing: bool = False
    
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
    
    def edit_api_key(self, key_id: str):
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
    
    async def load_api_keys(self):
        self.is_loading = True
        self.clear_messages()
        
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                self.is_loading = False
                return
            
            supabase = get_supabase_client()
            response = supabase.table("user_api_keys").select("*").eq("user_id", auth_state.user_id).order("created_at", desc=True).execute()
            
            if response.data:
                self.api_keys = []
                for key_data in response.data:
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
                    )
                    self.api_keys.append(decrypted_key)
            else:
                self.api_keys = []
                
        except Exception as e:
            self.error_message = f"Error loading API keys: {str(e)}"
        finally:
            self.is_loading = False
    
    async def fetch_balance(self, key_id: str):
        """Fetch Hyperliquid balance for a specific API key"""
        try:
            # Find the key
            key_data = next((k for k in self.api_keys if k.id == key_id), None)
            if not key_data:
                return
            
            # Update loading state
            key_data.balance_loading = True
            key_data.balance_error = ""
            
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
                else:
                    key_data.balance_error = "Failed to fetch balance"
            else:
                key_data.balance_error = "Only Hyperliquid supported"
            
            key_data.balance_loading = False
            
        except Exception as e:
            key_data = next((k for k in self.api_keys if k.id == key_id), None)
            if key_data:
                key_data.balance_loading = False
                key_data.balance_error = f"Error: {str(e)}"
    
    async def save_api_keys(self, form_data: dict):
        self.is_loading = True
        self.clear_messages()
        
        print(f"DEBUG: Form data received: {form_data}")
        
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
        
        print(f"DEBUG: is_master_account = {is_master_account}, type = {type(is_master_account)}")
        
        if not account_name:
            self.error_message = "Account name is required"
            self.is_loading = False
            return
        
        if not api_secret:
            self.error_message = "API Secret is required"
            self.is_loading = False
            return
        
        if exchange == "hyperliquid":
            if not wallet_address:
                self.error_message = "Wallet address is required for Hyperliquid (needed for balance/position queries)"
                self.is_loading = False
                return
        else:
            if not api_key:
                self.error_message = f"API Key is required for {exchange}"
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
            encrypted_key = encrypt_value(api_key) if api_key else None
            encrypted_secret = encrypt_value(api_secret)
            encrypted_private_key = encrypt_value(private_key) if private_key else None
            
            data = {
                "user_id": auth_state.user_id,
                "account_name": account_name,
                "exchange": exchange,
                "api_key": encrypted_key,
                "api_secret": encrypted_secret,
                "is_master_account": is_master_account,
                "wallet_address": wallet_address,
                "subaccount_name": subaccount_name,
                "private_key": encrypted_private_key,
                "notes": notes,
                "is_active": True
            }
            
            if self.is_editing and self.selected_key_id:
                supabase.table("user_api_keys").update(data).eq("id", self.selected_key_id).execute()
                self.success_message = f"API keys for '{account_name}' updated successfully!"
            else:
                supabase.table("user_api_keys").insert(data).execute()
                self.success_message = f"API keys for '{account_name}' saved successfully!"
            
            await self.load_api_keys()
            self.clear_form()
            
        except Exception as e:
            self.error_message = f"Error saving API keys: {str(e)}"
        finally:
            self.is_loading = False
    
    async def delete_api_key(self, key_id: str):
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
            key_data = next((k for k in self.api_keys if k.id == key_id), None)
            account_name = key_data.account_name if key_data else "account"
            
            supabase.table("user_api_keys").delete().eq("id", key_id).eq("user_id", auth_state.user_id).execute()
            
            self.success_message = f"API keys for '{account_name}' deleted successfully!"
            await self.load_api_keys()
            
            if self.selected_key_id == key_id:
                self.clear_form()
            
        except Exception as e:
            self.error_message = f"Error deleting API keys: {str(e)}"
        finally:
            self.is_loading = False
    
    async def toggle_active(self, key_id: str):
        try:
            from web_ui.state import AuthState
            auth_state = await self.get_state(AuthState)
            
            if not auth_state.is_authenticated or not auth_state.user_id:
                return
            
            supabase = get_supabase_client()
            
            key_data = next((k for k in self.api_keys if k.id == key_id), None)
            if key_data:
                new_status = not key_data.is_active
                supabase.table("user_api_keys").update({"is_active": new_status}).eq("id", key_id).eq("user_id", auth_state.user_id).execute()
                await self.load_api_keys()
        except Exception as e:
            self.error_message = f"Error toggling status: {str(e)}"
