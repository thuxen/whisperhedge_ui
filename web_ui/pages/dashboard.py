import reflex as rx
from ..state import AuthState
from ..api_key_state import APIKeyState
from ..lp_position_state import LPPositionState
from ..components import (
    sidebar,
    DashboardState,
    overview_section,
    api_keys_section,
    lp_positions_section,
    bot_status_section,
    settings_section,
)


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
                                    ("settings", settings_section()),
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
                    ),
                    
                    spacing="0",
                    width="100%",
                    align="stretch",
                ),
                width="100%",
                height="100vh",
            ),
            on_mount=[APIKeyState.load_api_keys, LPPositionState.load_positions, LPPositionState.load_wallets],
        ),
        rx.center(
            rx.vstack(
                rx.heading("Access Denied", size="8"),
                rx.text("Please log in to access the dashboard.", size="4", color="gray"),
                rx.link(
                    rx.button("Go to Login", size="3"),
                    href="/login",
                ),
                spacing="4",
                align="center",
            ),
            height="100vh",
        ),
    )
