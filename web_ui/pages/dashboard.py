import reflex as rx
from ..state import AuthState
from ..api_key_state import APIKeyState
from ..lp_position_state import LPPositionState
from ..dashboard_loading_state import DashboardLoadingState
from ..branding import COLORS
from ..components import (
    sidebar,
    DashboardState,
    overview_section,
    api_keys_section,
    lp_positions_section,
    bot_status_section,
    faq_section,
    settings_section,
    manage_plan_section,
)
from ..components.plan_status import PlanStatusState
from ..pages.manage_plan import ManagePlanState


def dashboard_page() -> rx.Component:
    return rx.cond(
        AuthState.is_authenticated,
        rx.fragment(
            rx.box(
                rx.hstack(
                    sidebar(),
                    
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.match(
                                    DashboardState.active_section,
                                    ("overview", overview_section()),
                                    ("api_keys", api_keys_section()),
                                    ("lp_positions", lp_positions_section()),
                                    ("bot_status", bot_status_section()),
                                    ("faq", faq_section()),
                                    ("settings", settings_section()),
                                    ("manage_plan", manage_plan_section()),
                                    api_keys_section(),
                                ),
                                width="100%",
                            ),
                            
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
                    align="stretch",
                ),
                width="100%",
                height="100vh",
            ),
            
            # Loading overlay
            rx.cond(
                DashboardLoadingState.is_loading_dashboard,
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.spinner(size="3", color=COLORS.ACCENT_PRIMARY),
                            rx.heading("Loading Dashboard...", size="6", margin_top="1rem", color=COLORS.TEXT_PRIMARY),
                            rx.text("Fetching your positions and API keys", size="3", color=COLORS.TEXT_SECONDARY),
                            spacing="4",
                            align="center",
                        ),
                        height="100vh",
                    ),
                    position="fixed",
                    top="0",
                    left="0",
                    width="100vw",
                    height="100vh",
                    background="rgba(2, 6, 23, 0.95)",
                    backdrop_filter="blur(8px)",
                    z_index="9999",
                ),
            ),
        ),
        rx.box(
            rx.center(
                rx.vstack(
                    rx.heading("Access Denied", size="8", color=COLORS.TEXT_PRIMARY),
                    rx.text("Please log in to access the dashboard.", size="4", color=COLORS.TEXT_SECONDARY),
                    rx.link(
                        rx.button(
                            "Go to Login",
                            size="3",
                            background=COLORS.BUTTON_PRIMARY_BG,
                            color=COLORS.BUTTON_PRIMARY_TEXT,
                            _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                        ),
                        href="/login",
                    ),
                    spacing="4",
                    align="center",
                ),
                height="100vh",
            ),
            background=COLORS.BACKGROUND_PRIMARY,
            min_height="100vh",
        ),
    )
