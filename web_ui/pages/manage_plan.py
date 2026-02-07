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
    
    # UI state
    active_tab: str = "overview"
    is_loading: bool = False
    error_message: str = ""
    
    def set_active_tab(self, tab: str):
        """Switch between tabs"""
        self.active_tab = tab
    
    def set_error_message(self, message: str):
        """Explicitly set error message"""
        self.error_message = message
    
    def load_current_plan(self):
        """Load user's current plan from Supabase"""
        try:
            import os
            from supabase import create_client
            
            print("[PLAN] Loading current plan from Supabase")
            
            # Get user ID from auth state
            auth_state = self.get_state(AuthState)
            user_id = auth_state.user_id
            
            if not user_id:
                print("[PLAN] No user_id found, skipping plan load")
                return
            
            print(f"[PLAN]   - User ID: {user_id}")
            
            # Initialize Supabase client
            supabase = create_client(
                os.getenv("SUPABASE_URL"),
                os.getenv("SUPABASE_ANON_KEY")
            )
            
            # Query user subscription
            result = supabase.table("user_subscriptions").select("*").eq("user_id", user_id).execute()
            
            if result.data and len(result.data) > 0:
                plan = result.data[0]
                print(f"[PLAN] ✓ Plan loaded from database")
                print(f"[PLAN]   - Tier: {plan.get('tier_name', 'free')}")
                print(f"[PLAN]   - Status: {plan.get('status', 'N/A')}")
                print(f"[PLAN]   - Stripe Customer: {plan.get('stripe_customer_id', 'N/A')}")
                print(f"[PLAN]   - Stripe Subscription: {plan.get('stripe_subscription_id', 'N/A')}")
                
                # Update state with plan data
                self.current_tier_name = plan.get("tier_name", "free")
                self.stripe_customer_id = plan.get("stripe_customer_id", "")
                self.stripe_subscription_id = plan.get("stripe_subscription_id", "")
            else:
                print("[PLAN] No subscription found in database, using free tier")
                self.current_tier_name = "free"
                
        except Exception as e:
            print(f"[PLAN ERROR] Failed to load plan: {e}")
            import traceback
            traceback.print_exc()
    
    async def create_checkout_session(self, tier_name: str):
        """Create Stripe checkout session for plan upgrade"""
        try:
            import os
            from ..services.stripe_service import create_checkout_session
            
            print(f"[CHECKOUT] Initiating checkout for tier: {tier_name}")
            
            # Get user info from auth state - need to get the parent state instance
            auth_state = await self.get_state(AuthState)
            user_id = auth_state.user_id
            user_email = auth_state.user_email
            
            print(f"[CHECKOUT]   - User ID: {user_id}")
            print(f"[CHECKOUT]   - User Email: {user_email}")
            
            # Get base URL for redirects - use env var or default to localhost
            base_url = os.getenv("APP_URL", "http://localhost:3000")
            print(f"[CHECKOUT]   - Base URL: {base_url}")
            
            # Create Stripe checkout session
            checkout_url = create_checkout_session(
                user_id=user_id,
                user_email=user_email,
                tier_name=tier_name,
                success_url=f"{base_url}/dashboard?upgrade_success=true",
                cancel_url=f"{base_url}/dashboard?upgrade_cancelled=true",
            )
            
            if checkout_url:
                print(f"[CHECKOUT] ✓ Redirecting to Stripe: {checkout_url}")
                # Redirect to Stripe checkout
                return rx.redirect(checkout_url)
            else:
                print(f"[CHECKOUT ERROR] No checkout URL returned")
                self.error_message = "Failed to create checkout session. Check console for details."
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"[CHECKOUT ERROR] Stripe checkout failed: {e}")
            import traceback
            traceback.print_exc()
    
    def manage_subscription(self):
        """Redirect to Stripe customer portal for subscription management"""
        try:
            import os
            from ..services.stripe_service import create_customer_portal_session
            
            print(f"[PORTAL] Opening customer portal for customer: {self.stripe_customer_id}")
            
            # Get base URL for return redirect - use env var or default to localhost
            base_url = os.getenv("APP_URL", "http://localhost:3000")
            print(f"[PORTAL]   - Return URL: {base_url}/dashboard")
            
            # Create customer portal session
            portal_url = create_customer_portal_session(
                customer_id=self.stripe_customer_id,
                return_url=f"{base_url}/dashboard",
            )
            
            if portal_url:
                print(f"[PORTAL] ✓ Redirecting to portal: {portal_url}")
                # Redirect to Stripe customer portal
                return rx.redirect(portal_url)
            else:
                print(f"[PORTAL ERROR] No portal URL returned")
                self.error_message = "Failed to open customer portal. Please contact support."
                
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            print(f"[PORTAL ERROR] Customer portal failed: {e}")
            import traceback
            traceback.print_exc()
    
    def on_load(self):
        """Called when the manage plan page loads"""
        print("[PAGE] Manage Plan page loading")
        print(f"[PAGE]   - Current URL: {self.router.page.path}")
        print(f"[PAGE]   - Query params: {self.router.page.params}")
        
        # Check for success/cancel query params from Stripe redirect
        upgrade_success = self.router.page.params.get("upgrade_success")
        upgrade_cancelled = self.router.page.params.get("upgrade_cancelled")
        
        if upgrade_success:
            print("[PAGE] ✓ Stripe checkout completed successfully")
            print("[PAGE]   - Loading updated plan from database...")
            self.load_current_plan()
        elif upgrade_cancelled:
            print("[PAGE] ⚠ Stripe checkout was cancelled")
        else:
            print("[PAGE]   - Normal page load, loading current plan...")
            self.load_current_plan()
        
        print("[PAGE] Page load complete")


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


def tab_button(label: str, tab_id: str) -> rx.Component:
    """Tab button component"""
    is_active = ManagePlanState.active_tab == tab_id
    
    return rx.box(
        rx.text(
            label,
            size="3",
            weight="medium",
        ),
        padding="0.75rem 1.5rem",
        border_bottom=rx.cond(
            is_active,
            f"2px solid {COLORS.ACCENT_PRIMARY}",
            "2px solid transparent",
        ),
        color=rx.cond(
            is_active,
            COLORS.TEXT_PRIMARY,
            COLORS.TEXT_SECONDARY,
        ),
        cursor="pointer",
        on_click=lambda: ManagePlanState.set_active_tab(tab_id),
        _hover={
            "color": COLORS.TEXT_PRIMARY,
        },
    )


def overview_tab() -> rx.Component:
    """Overview tab - shows current plan and usage"""
    return rx.vstack(
        # Current Plan Summary
        rx.box(
            rx.vstack(
                rx.heading(
                    "Current Plan",
                    size="5",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="1rem",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            ManagePlanState.current_display_name,
                            size="7",
                            weight="bold",
                            color=COLORS.ACCENT_PRIMARY,
                        ),
                        rx.text(
                            rx.cond(
                                ManagePlanState.current_price > 0,
                                f"${ManagePlanState.current_price:.2f}/month",
                                "Free Forever",
                            ),
                            size="3",
                            color=COLORS.TEXT_SECONDARY,
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.button(
                        "Change Plan",
                        size="3",
                        variant="outline",
                        on_click=lambda: ManagePlanState.set_active_tab("change_plan"),
                    ),
                    width="100%",
                    align="center",
                ),
                align="start",
                spacing="3",
                width="100%",
            ),
            padding="2rem",
            border_radius="8px",
            border=f"1px solid {COLORS.CARD_BORDER}",
            background=COLORS.CARD_BG,
            margin_bottom="2rem",
        ),
        
        # Usage Stats
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
                            rx.progress(
                                value=((ManagePlanState.current_tvl / ManagePlanState.current_tvl_limit) * 100).to(int),
                                max=100,
                                width="100%",
                                margin_top="0.5rem",
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
                            rx.progress(
                                value=((ManagePlanState.current_positions / ManagePlanState.current_position_limit) * 100).to(int),
                                max=100,
                                width="100%",
                                margin_top="0.5rem",
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
                
                # TVL footnote
                rx.text(
                    "* TVL (Total Value Locked) = LP Position Value + Hyperliquid Hedge Account Value",
                    size="1",
                    color=COLORS.TEXT_MUTED,
                    font_style="italic",
                    margin_top="0.5rem",
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
        
        align="start",
        spacing="4",
        width="100%",
    )


def change_plan_tab() -> rx.Component:
    """Change Plan tab - shows all plan options for upgrade/downgrade"""
    return rx.vstack(
        rx.heading(
            "Choose Your Plan",
            size="5",
            weight="bold",
            color=COLORS.TEXT_PRIMARY,
            margin_bottom="1rem",
        ),
        rx.text(
            "Upgrade or downgrade your subscription at any time.",
            size="3",
            color=COLORS.TEXT_SECONDARY,
            margin_bottom="2rem",
        ),
        
        # Plan options grid
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
        
        align="start",
        spacing="4",
        width="100%",
    )


def billing_tab() -> rx.Component:
    """Billing tab - manage payment method, view invoices, cancel subscription"""
    return rx.vstack(
        rx.heading(
            "Billing Management",
            size="5",
            weight="bold",
            color=COLORS.TEXT_PRIMARY,
            margin_bottom="1rem",
        ),
        
        # For paid users
        rx.cond(
            ManagePlanState.stripe_subscription_id != "",
            rx.vstack(
                # Stripe Portal Card
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("credit-card", size=24, color=COLORS.ACCENT_PRIMARY),
                            rx.vstack(
                                rx.text(
                                    "Payment Method & Invoices",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "Manage your payment method, view invoices, and download receipts.",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="start",
                                spacing="1",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("external-link", size=16),
                                rx.text("Open Stripe Billing Portal"),
                                spacing="2",
                            ),
                            size="3",
                            on_click=ManagePlanState.manage_subscription,
                            width="fit-content",
                        ),
                        align="start",
                        spacing="3",
                        width="100%",
                    ),
                    padding="2rem",
                    border_radius="8px",
                    border=f"1px solid {COLORS.CARD_BORDER}",
                    background=COLORS.CARD_BG,
                    margin_bottom="1.5rem",
                ),
                
                # Cancel Subscription Card
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.icon("alert-triangle", size=24, color="#EF4444"),
                            rx.vstack(
                                rx.text(
                                    "Cancel Subscription",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "You can cancel your subscription at any time. You'll retain access until the end of your billing period.",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="start",
                                spacing="1",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        rx.button(
                            "Cancel Subscription",
                            size="3",
                            color_scheme="red",
                            variant="outline",
                            on_click=ManagePlanState.manage_subscription,
                            width="fit-content",
                        ),
                        align="start",
                        spacing="3",
                        width="100%",
                    ),
                    padding="2rem",
                    border_radius="8px",
                    border="1px solid rgba(239, 68, 68, 0.3)",
                    background="rgba(239, 68, 68, 0.05)",
                ),
                
                align="start",
                spacing="4",
                width="100%",
            ),
            # Free tier message
            rx.box(
                rx.vstack(
                    rx.icon("info", size=24, color=COLORS.TEXT_SECONDARY),
                    rx.text(
                        "You're on the Free plan",
                        size="4",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Upgrade to a paid plan to access billing management features.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                    ),
                    rx.button(
                        "View Plans",
                        size="3",
                        on_click=lambda: ManagePlanState.set_active_tab("change_plan"),
                        margin_top="1rem",
                    ),
                    align="center",
                    spacing="3",
                ),
                padding="3rem",
                border_radius="8px",
                border=f"1px solid {COLORS.CARD_BORDER}",
                background=COLORS.CARD_BG,
                text_align="center",
            ),
        ),
        
        align="start",
        spacing="4",
        width="100%",
    )


def manage_plan_content() -> rx.Component:
    """Manage Plan content - for use within dashboard"""
    return rx.vstack(
        # Header
        rx.heading(
            "Billing & Subscription",
            size="8",
            weight="bold",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Manage your plan, view usage, and update billing details.",
            size="4",
            color=COLORS.TEXT_SECONDARY,
            margin_bottom="2rem",
        ),
        
        # Error message
        rx.cond(
            ManagePlanState.error_message != "",
            rx.box(
                rx.hstack(
                    rx.icon("alert-triangle", size=18, color="#EF4444"),
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
                background="rgba(239, 68, 68, 0.1)",
                border="1px solid rgba(239, 68, 68, 0.3)",
                margin_bottom="2rem",
                max_width="1400px",
                margin_x="auto",
                width="100%",
            ),
        ),
        
        # Tab Navigation
        rx.box(
            rx.hstack(
                tab_button("Overview", "overview"),
                tab_button("Change Plan", "change_plan"),
                tab_button("Billing", "billing"),
                spacing="0",
                border_bottom=f"1px solid {COLORS.BORDER_DEFAULT}",
            ),
            margin_bottom="2rem",
            max_width="1400px",
            margin_x="auto",
            width="100%",
        ),
        
        # Tab Content
        rx.box(
            rx.cond(
                ManagePlanState.active_tab == "overview",
                overview_tab(),
                rx.cond(
                    ManagePlanState.active_tab == "change_plan",
                    change_plan_tab(),
                    billing_tab(),
                ),
            ),
            max_width="1400px",
            margin_x="auto",
            width="100%",
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
