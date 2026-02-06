import reflex as rx
from ..branding import COLORS
from ..state import AuthState


class ManagePlanState(rx.State):
    """State for plan management"""
    # Current plan info
    current_tier_name: str = "free"
    current_display_name: str = "Free"
    current_price: float = 0.0
    current_tvl_limit: float = 2500.0
    current_position_limit: int = 1
    
    # Usage stats
    current_tvl: float = 0.0
    current_positions: int = 0
    
    # Override flags
    has_tvl_override: bool = False
    has_position_override: bool = False
    is_beta_tester: bool = False
    
    # Stripe
    stripe_customer_id: str = ""
    stripe_subscription_id: str = ""
    
    # Loading states
    is_loading: bool = False
    error_message: str = ""
    
    def set_error_message(self, message: str):
        """Explicitly set error message"""
        self.error_message = message
    
    def load_current_plan(self):
        """Load user's current plan from Supabase"""
        # TODO: Implement Supabase query to get user's plan
        pass
    
    async def create_checkout_session(self, tier_name: str):
        """Create Stripe checkout session for plan upgrade"""
        try:
            import os
            from ..services.stripe_service import create_checkout_session
            
            # Get user info from auth state - need to get the parent state instance
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            user_email = auth_state.user_email
            
            print(f"[DEBUG] Creating checkout session:")
            print(f"  - user_id: {user_id}")
            print(f"  - user_email: {user_email}")
            print(f"  - tier_name: {tier_name}")
            
            # Get base URL for redirects - use env var or default to localhost
            base_url = os.getenv("APP_URL", "http://localhost:3000")
            print(f"  - base_url: {base_url}")
            
            # Create Stripe checkout session
            checkout_url = create_checkout_session(
                user_id=user_id,
                user_email=user_email,
                tier_name=tier_name,
                success_url=f"{base_url}/dashboard?upgrade_success=true",
                cancel_url=f"{base_url}/dashboard?upgrade_cancelled=true",
            )
            
            print(f"[DEBUG] Checkout URL: {checkout_url}")
            
            if checkout_url:
                # Redirect to Stripe checkout
                return rx.redirect(checkout_url)
            else:
                self.error_message = "Failed to create checkout session. Check console for details."
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"[ERROR] Stripe checkout failed: {e}")
            import traceback
            traceback.print_exc()
    
    def manage_subscription(self):
        """Redirect to Stripe customer portal for subscription management"""
        try:
            import os
            from ..services.stripe_service import create_customer_portal_session
            
            # Get base URL for return redirect - use env var or default to localhost
            base_url = os.getenv("APP_URL", "http://localhost:3000")
            
            # Create customer portal session
            portal_url = create_customer_portal_session(
                customer_id=self.stripe_customer_id,
                return_url=f"{base_url}/dashboard",
            )
            
            if portal_url:
                # Redirect to Stripe customer portal
                return rx.redirect(portal_url)
            else:
                self.error_message = "Failed to open customer portal. Please contact support."
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"[ERROR] Customer portal failed: {e}")


def plan_card(
    tier_name: str,
    display_name: str,
    price: float,
    positions: str,
    tvl: str,
    features: list[str],
    is_current: bool = False,
    is_popular: bool = False,
    badge_color: str = COLORS.TEXT_SECONDARY,
) -> rx.Component:
    """Plan card component for manage plan page"""
    
    return rx.box(
        rx.vstack(
            # Header with badge
            rx.hstack(
                rx.text(
                    display_name.upper(),
                    size="2",
                    weight="bold",
                    color=badge_color,
                    text_transform="uppercase",
                    letter_spacing="0.1em",
                ),
                rx.cond(
                    is_popular,
                    rx.badge(
                        "Most Popular",
                        color_scheme="blue",
                        size="1",
                    ),
                ),
                rx.cond(
                    is_current,
                    rx.badge(
                        "Current Plan",
                        color_scheme="green",
                        size="1",
                    ),
                ),
                spacing="2",
                margin_bottom="1rem",
            ),
            
            # Price
            rx.hstack(
                rx.heading(
                    f"${price:.2f}" if price > 0 else "$0",
                    size="8",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "/mo",
                    size="3",
                    color=COLORS.TEXT_SECONDARY,
                ),
                align="end",
                spacing="1",
                margin_bottom="1rem",
            ),
            
            rx.divider(margin_y="1rem"),
            
            # Limits
            rx.vstack(
                rx.text(
                    positions,
                    size="3",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    tvl,
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="1rem",
                ),
                
                # Features
                rx.vstack(
                    *[
                        rx.text(
                            f"✓ {feature}",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                        )
                        for feature in features
                    ],
                    align="start",
                    spacing="2",
                ),
                align="start",
                spacing="2",
            ),
            
            # Action button
            rx.cond(
                is_current,
                rx.button(
                    "Current Plan",
                    size="3",
                    variant="outline",
                    width="100%",
                    margin_top="1rem",
                    disabled=True,
                ),
                rx.button(
                    "Select Plan",
                    size="3",
                    background=COLORS.BUTTON_PRIMARY_BG,
                    color=COLORS.BUTTON_PRIMARY_TEXT,
                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    width="100%",
                    margin_top="1rem",
                    on_click=lambda: ManagePlanState.create_checkout_session(tier_name),
                ),
            ),
            
            align="start",
            spacing="3",
        ),
        padding="2rem",
        border_radius="8px",
        border=rx.cond(
            is_popular,
            f"2px solid {COLORS.ACCENT_PRIMARY}",
            f"1px solid #1E293B",
        ),
        background="rgba(15, 23, 42, 0.4)",
        box_shadow=rx.cond(
            is_popular,
            "0 0 20px rgba(59, 130, 246, 0.3)",
            "none",
        ),
    )


def manage_plan_content() -> rx.Component:
    """Manage Plan content - for use within dashboard"""
    return rx.vstack(
        # Header
        rx.heading(
            "Manage Your Plan",
            size="8",
            weight="bold",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Upgrade, downgrade, or manage your subscription.",
            size="4",
            color=COLORS.TEXT_SECONDARY,
            margin_bottom="1rem",
        ),
        
        # Info/Error message
        rx.cond(
            ManagePlanState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("info", size=18, color="#3B82F6"),
                    rx.text(
                        ManagePlanState.error_message,
                        size="3",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=ManagePlanState.set_error_message(""),
                        variant="ghost",
                        size="1",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                padding="1rem",
                border_radius="8px",
                background="rgba(59, 130, 246, 0.1)",
                border="1px solid rgba(59, 130, 246, 0.3)",
                margin_bottom="2rem",
                max_width="1400px",
                margin_x="auto",
                width="100%",
            ),
        ),
                    
                    # Current usage stats
                    rx.box(
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    "Current Usage",
                                    size="5",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                    margin_bottom="1rem",
                                ),
                                rx.grid(
                                    # TVL Usage
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                "Total Value Locked",
                                                size="2",
                                                color=COLORS.TEXT_SECONDARY,
                                                margin_bottom="0.5rem",
                                            ),
                                            rx.hstack(
                                                rx.text(
                                                    f"${ManagePlanState.current_tvl:,.0f}",
                                                    size="6",
                                                    weight="bold",
                                                    color=COLORS.TEXT_PRIMARY,
                                                ),
                                                rx.text(
                                                    f" / ${ManagePlanState.current_tvl_limit:,.0f}",
                                                    size="3",
                                                    color=COLORS.TEXT_MUTED,
                                                ),
                                                spacing="1",
                                            ),
                                            align="start",
                                            spacing="1",
                                        ),
                                        padding="1.5rem",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS.CARD_BORDER}",
                                        background=COLORS.CARD_BG,
                                    ),
                                    
                                    # Position Usage
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                "Active Positions",
                                                size="2",
                                                color=COLORS.TEXT_SECONDARY,
                                                margin_bottom="0.5rem",
                                            ),
                                            rx.hstack(
                                                rx.text(
                                                    ManagePlanState.current_positions,
                                                    size="6",
                                                    weight="bold",
                                                    color=COLORS.TEXT_PRIMARY,
                                                ),
                                                rx.text(
                                                    f" / {ManagePlanState.current_position_limit}",
                                                    size="3",
                                                    color=COLORS.TEXT_MUTED,
                                                ),
                                                spacing="1",
                                            ),
                                            align="start",
                                            spacing="1",
                                        ),
                                        padding="1.5rem",
                                        border_radius="8px",
                                        border=f"1px solid {COLORS.CARD_BORDER}",
                                        background=COLORS.CARD_BG,
                                    ),
                                    
                                    columns="2",
                                    spacing="4",
                                    width="100%",
                                ),
                                
                                # Beta tester badge
                                rx.cond(
                                    ManagePlanState.is_beta_tester,
                                    rx.box(
                                        rx.hstack(
                                            rx.icon("info", size=16, color="#10B981"),
                                            rx.text(
                                                "You're a beta tester with custom limits. Contact support to modify your plan.",
                                                size="2",
                                                color=COLORS.TEXT_SECONDARY,
                                            ),
                                            spacing="2",
                                        ),
                                        padding="1rem",
                                        border_radius="8px",
                                        background="rgba(16, 185, 129, 0.1)",
                                        border="1px solid rgba(16, 185, 129, 0.3)",
                                        margin_top="1rem",
                                    ),
                                ),
                                
                                align="start",
                                spacing="3",
                                width="100%",
                            ),
                            padding="2rem",
                            border_radius="8px",
                            border=f"1px solid {COLORS.CARD_BORDER}",
                            background=COLORS.CARD_BG,
                        ),
                        max_width="1400px",
                        margin_x="auto",
                        margin_bottom="3rem",
                        width="100%",
                    ),
                    
                    # Plan options grid
                    rx.box(
                        rx.grid(
                            # FREE
                            plan_card(
                                tier_name="free",
                                display_name="Free",
                                price=0.0,
                                positions="1 LP Position",
                                tvl="$2,500 TVL Hard Cap",
                                features=[
                                    "Standard Execution",
                                    "Hyperliquid Integration",
                                    "All Strategies",
                                ],
                                is_current=ManagePlanState.current_tier_name == "free",
                            ),
                            
                            # HOBBY
                            plan_card(
                                tier_name="hobby",
                                display_name="Hobby",
                                price=19.99,
                                positions="3 LP Positions",
                                tvl="$10,000 Included TVL",
                                features=[
                                    "Standard Execution",
                                    "Email Alerts",
                                    "0.1% (10 bps) on excess TVL",
                                ],
                                is_current=ManagePlanState.current_tier_name == "hobby",
                            ),
                            
                            # PRO
                            plan_card(
                                tier_name="pro",
                                display_name="Pro",
                                price=49.99,
                                positions="10 LP Positions",
                                tvl="$50,000 Included TVL",
                                features=[
                                    "Priority Execution",
                                    "Multi-DEX Roadmap Access",
                                    "0.05% (5 bps) on excess TVL",
                                ],
                                is_current=ManagePlanState.current_tier_name == "pro",
                                is_popular=True,
                                badge_color=COLORS.ACCENT_PRIMARY,
                            ),
                            
                            # ELITE
                            plan_card(
                                tier_name="elite",
                                display_name="Elite",
                                price=149.99,
                                positions="Unlimited LP Positions",
                                tvl="$250,000 Included TVL",
                                features=[
                                    "Elite Priority Calculation Engine",
                                    "Top-of-queue Rebalancing",
                                    "Direct Dev Support",
                                    "0.05% (5 bps) on excess TVL",
                                ],
                                is_current=ManagePlanState.current_tier_name == "elite",
                                badge_color="#D4AF37",
                            ),
                            
                            columns="4",
                            spacing="4",
                            width="100%",
                        ),
                        max_width="1400px",
                        margin_x="auto",
                        width="100%",
                    ),
                    
                    # Manage subscription button (for existing paid subscribers)
                    rx.cond(
                        ManagePlanState.stripe_subscription_id != "",
                        rx.box(
                            rx.vstack(
                                rx.divider(margin_y="2rem"),
                                rx.text(
                                    "Need to update payment method or cancel?",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    text_align="center",
                                ),
                                rx.button(
                                    "Manage Subscription in Stripe",
                                    size="3",
                                    variant="outline",
                                    on_click=ManagePlanState.manage_subscription,
                                ),
                                align="center",
                                spacing="3",
                            ),
                            width="100%",
                        ),
                    ),
                    
        align="start",
        spacing="4",
        width="100%",
    )


def manage_plan_page() -> rx.Component:
    """Manage Plan page - requires authentication"""
    from ..components import sidebar
    
    return rx.cond(
        AuthState.is_authenticated,
        rx.box(
            rx.hstack(
                sidebar(),
                
                rx.box(
                    rx.vstack(
                        manage_plan_content(),
                        spacing="0",
                        width="100%",
                        padding="2rem",
                        min_height="100vh",
                    ),
                    flex="1",
                    overflow_y="auto",
                    height="100vh",
                    background=COLORS.BACKGROUND_PRIMARY,
                ),
                
                spacing="0",
                width="100%",
                height="100vh",
            ),
            width="100%",
            height="100vh",
            overflow="hidden",
        ),
        rx.fragment(
            rx.script("window.location.href = '/login'")
        ),
    )
