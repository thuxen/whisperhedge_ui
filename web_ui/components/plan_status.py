import reflex as rx
from ..branding import COLORS


class PlanStatusState(rx.State):
    """State for plan status display"""
    tier_name: str = "free"
    display_name: str = "Free"
    price_monthly: float = 0.0
    
    # Current usage - will be synced from LPPositionState
    current_tvl: float = 0.0
    current_positions: int = 0
    
    # Limits (defaults match Free tier)
    tvl_limit: float | None = 2500.0
    position_limit: int | None = 1
    rebalance_frequency: str = "standard"
    
    # Override flags
    has_tvl_override: bool = False
    has_position_override: bool = False
    is_beta_tester: bool = False
    
    async def load_plan_data(self):
        """Load user's plan and usage data from Supabase"""
        try:
            from ..auth import get_supabase_client
            from ..state import AuthState
            
            # Get user ID and access token from auth state
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            access_token = auth_state.access_token
            
            if not user_id:
                from ..dashboard_loading_state import DashboardLoadingState
                dashboard_loading = await self.get_state(DashboardLoadingState)
                dashboard_loading.mark_plan_data_loaded()
                return
            
            # Use get_supabase_client with access token for proper RLS
            supabase = get_supabase_client(access_token)
            
            # Query user_effective_limits view for current plan
            result = supabase.table("user_effective_limits").select("*").eq("user_id", user_id).execute()
            
            if result.data and len(result.data) > 0:
                plan = result.data[0]
                self.tier_name = plan.get("tier_name", "free")
                self.display_name = plan.get("display_name", "Free")
                self.price_monthly = plan.get("price_monthly", 0.0)
                self.tvl_limit = plan.get("effective_tvl_limit")
                self.position_limit = plan.get("effective_position_limit")
                self.rebalance_frequency = plan.get("effective_rebalance_frequency", "standard")
                self.has_tvl_override = plan.get("override_tvl_limit") is not None
                self.has_position_override = plan.get("override_position_limit") is not None
                self.is_beta_tester = plan.get("is_beta_tester", False)
            
            # Sync usage data from OverviewState
            from ..overview_state import OverviewState
            overview_state = await self.get_state(OverviewState)
            self.current_tvl = overview_state.total_value
            self.current_positions = overview_state.total_positions
            
            # Mark as loaded for dashboard loading state
            from ..dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_plan_data_loaded()
        except Exception as e:
            print(f"[PLAN STATUS ERROR] Failed to load plan data: {e}")
            import traceback
            traceback.print_exc()
            # Mark as loaded even on error to prevent infinite loading
            from ..dashboard_loading_state import DashboardLoadingState
            dashboard_loading = await self.get_state(DashboardLoadingState)
            dashboard_loading.mark_plan_data_loaded()
    
    def navigate_to_manage_plan(self):
        """Navigate to manage plan section in dashboard"""
        # Import here to avoid circular dependency
        from .sidebar import DashboardState
        return DashboardState.set_section("manage_plan")
    
    @rx.var
    def tvl_percentage(self) -> float:
        """Calculate TVL usage percentage"""
        if self.tvl_limit is None or self.tvl_limit == 0:
            return 0.0
        return min((self.current_tvl / self.tvl_limit) * 100, 100)
    
    @rx.var
    def position_percentage(self) -> float:
        """Calculate position usage percentage"""
        if self.position_limit is None or self.position_limit == 0:
            return 0.0
        return min((self.current_positions / self.position_limit) * 100, 100)
    
    @rx.var
    def tvl_limit_display(self) -> str:
        """Format TVL limit for display"""
        if self.tvl_limit is None:
            return "Unlimited"
        return f"${self.tvl_limit:,.0f}"
    
    @rx.var
    def position_limit_display(self) -> str:
        """Format position limit for display"""
        if self.position_limit is None:
            return "Unlimited"
        return str(self.position_limit)
    
    @rx.var
    def is_near_tvl_limit(self) -> bool:
        """Check if near TVL limit (>80%)"""
        return self.tvl_percentage >= 80
    
    @rx.var
    def is_near_position_limit(self) -> bool:
        """Check if near position limit (>80%)"""
        return self.position_percentage >= 80


def plan_status_widget() -> rx.Component:
    """Plan status widget for sidebar"""
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading(
                    "Current Plan",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.cond(
                    PlanStatusState.is_beta_tester,
                    rx.badge(
                        "BETA",
                        color_scheme="green",
                        size="1",
                    ),
                ),
                justify="between",
                width="100%",
                margin_bottom="0.5rem",
            ),
            
            # Plan name (no price)
            rx.text(
                PlanStatusState.display_name,
                size="5",
                weight="bold",
                color=COLORS.ACCENT_PRIMARY,
                margin_bottom="1rem",
            ),
            
            # TVL Usage
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Total Value Locked",
                        size="2",
                        weight="medium",
                        color=COLORS.TEXT_SECONDARY,
                    ),
                    rx.cond(
                        PlanStatusState.has_tvl_override,
                        rx.badge(
                            "Override",
                            color_scheme="orange",
                            size="1",
                        ),
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.hstack(
                    rx.text(
                        rx.text.span("$", f"{PlanStatusState.current_tvl:,.0f}"),
                        size="3",
                        weight="bold",
                        color=rx.cond(
                            PlanStatusState.is_near_tvl_limit,
                            "#F59E0B",  # amber
                            COLORS.TEXT_PRIMARY,
                        ),
                    ),
                    rx.text(
                        rx.text.span(" / ", PlanStatusState.tvl_limit_display),
                        size="2",
                        color=COLORS.TEXT_MUTED,
                    ),
                    spacing="1",
                    width="100%",
                ),
                # Progress bar
                rx.box(
                    rx.box(
                        width=f"{PlanStatusState.tvl_percentage}%",
                        height="100%",
                        background=rx.cond(
                            PlanStatusState.is_near_tvl_limit,
                            "#F59E0B",  # amber
                            COLORS.ACCENT_PRIMARY,
                        ),
                        border_radius="4px",
                        transition="width 0.3s ease",
                    ),
                    width="100%",
                    height="6px",
                    background="rgba(59, 130, 246, 0.1)",
                    border_radius="4px",
                    overflow="hidden",
                ),
                align="start",
                spacing="1",
                width="100%",
                margin_bottom="1.5rem",
            ),
            
            # Upgrade button
            rx.cond(
                PlanStatusState.tier_name != "elite",
                rx.button(
                    "Manage Plan",
                    size="3",
                    width="100%",
                    background=COLORS.BUTTON_PRIMARY_BG,
                    color=COLORS.BUTTON_PRIMARY_TEXT,
                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    on_click=PlanStatusState.navigate_to_manage_plan,
                ),
                rx.box(
                    rx.text(
                        "✓ Premium Plan",
                        size="2",
                        weight="medium",
                        color="#10B981",  # green
                        text_align="center",
                    ),
                    width="100%",
                    padding="0.5rem",
                ),
            ),
            
            align="start",
            spacing="2",
            width="100%",
        ),
        padding="1.5rem",
        border_radius="8px",
        border=f"1px solid {COLORS.CARD_BORDER}",
        background=COLORS.CARD_BG,
        width="100%",
    )
