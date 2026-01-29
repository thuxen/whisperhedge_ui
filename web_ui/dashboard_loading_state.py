import reflex as rx


class DashboardLoadingState(rx.State):
    """State to track dashboard data loading on mount."""
    
    is_loading_dashboard: bool = True
    api_keys_loaded: bool = False
    positions_loaded: bool = False
    wallets_loaded: bool = False
    
    def mark_api_keys_loaded(self):
        """Mark API keys as loaded."""
        self.api_keys_loaded = True
        self._check_all_loaded()
    
    def mark_positions_loaded(self):
        """Mark positions as loaded."""
        self.positions_loaded = True
        self._check_all_loaded()
    
    def mark_wallets_loaded(self):
        """Mark wallets as loaded."""
        self.wallets_loaded = True
        self._check_all_loaded()
    
    def _check_all_loaded(self):
        """Check if all data is loaded and update loading state."""
        if self.api_keys_loaded and self.positions_loaded and self.wallets_loaded:
            self.is_loading_dashboard = False
    
    def reset_loading(self):
        """Reset loading state (called on dashboard mount)."""
        self.is_loading_dashboard = True
        self.api_keys_loaded = False
        self.positions_loaded = False
        self.wallets_loaded = False
