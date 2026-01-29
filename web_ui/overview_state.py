import reflex as rx


class OverviewState(rx.State):
    """State for overview page statistics"""
    
    # LP Position stats
    total_positions: int = 0
    hedged_positions: int = 0
    total_value: float = 0.0
    
    # API Key stats
    total_api_keys: int = 0
    in_use_api_keys: int = 0
    
    @rx.var
    def lp_positions_display(self) -> str:
        """Display format: hedged/total"""
        return f"{self.hedged_positions}/{self.total_positions}"
    
    @rx.var
    def lp_positions_text(self) -> str:
        """Descriptive text for LP positions"""
        return f"{self.hedged_positions} Actively Hedged Position{'s' if self.hedged_positions != 1 else ''}"
    
    @rx.var
    def api_keys_display(self) -> str:
        """Display format: in_use/total"""
        return f"{self.in_use_api_keys}/{self.total_api_keys}"
    
    @rx.var
    def api_keys_text(self) -> str:
        """Descriptive text for API keys"""
        return f"{self.in_use_api_keys} In Use"
    
    @rx.var
    def total_value_formatted(self) -> str:
        """Formatted total value"""
        return f"${self.total_value:,.2f}"
    
    def update_stats(self, lp_positions: list, api_keys: list):
        """Update overview statistics from LP positions and API keys"""
        # LP Position stats
        self.total_positions = len(lp_positions)
        self.hedged_positions = sum(1 for pos in lp_positions if pos.get('hedge_enabled', False))
        self.total_value = sum(pos.get('total_value_usd', 0.0) for pos in lp_positions)
        
        # API Key stats
        self.total_api_keys = len(api_keys)
        self.in_use_api_keys = sum(1 for key in api_keys if key.get('is_in_use', False))
