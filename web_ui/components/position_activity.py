"""
Activity dialog component for displaying LP position logs/trades
"""
import reflex as rx
from ..lp_position_state import LPPositionState


def position_activity_dialog() -> rx.Component:
    """Display activity/logs for a specific LP position"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.dialog.title("Position Activity"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="1",
                            on_click=LPPositionState.close_activity_dialog,
                        )
                    ),
                    width="100%",
                    align="center",
                ),
                
                # Placeholder content
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Position Activity & Logs",
                            size="4",
                            weight="bold",
                            margin_bottom="1rem",
                        ),
                        rx.text(
                            "This section will display:",
                            size="2",
                            margin_bottom="0.5rem",
                        ),
                        rx.text("• Hedge execution history", size="2"),
                        rx.text("• Trade logs and details", size="2"),
                        rx.text("• Position rebalancing events", size="2"),
                        rx.text("• Error logs and warnings", size="2"),
                        spacing="2",
                    ),
                    padding="2rem",
                    background="var(--gray-2)",
                    border_radius="8px",
                    width="100%",
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="800px",
            padding="2rem",
        ),
        open=LPPositionState.show_activity_dialog,
    )
