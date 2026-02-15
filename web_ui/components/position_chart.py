"""
Chart component for displaying LP position value over time
"""
import reflex as rx
from ..lp_position_state import LPPositionState


def position_value_chart() -> rx.Component:
    """Display chart of LP value, hedge account value, and total value over time"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.dialog.title("Position Value History"),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="1",
                            on_click=LPPositionState.close_chart,
                        )
                    ),
                    width="100%",
                    align="center",
                ),
                
                rx.cond(
                    LPPositionState.chart_loading,
                    rx.center(
                        rx.spinner(size="3"),
                        padding="4rem",
                    ),
                    rx.cond(
                        LPPositionState.chart_data.length() > 0,
                        rx.vstack(
                            # Time range selector
                            rx.hstack(
                                rx.text("Time Range:", size="2", weight="medium"),
                                rx.button(
                                    "1h",
                                    size="1",
                                    variant="soft",
                                    color_scheme=rx.cond(LPPositionState.chart_hours == 1, "blue", "gray"),
                                    on_click=lambda: LPPositionState.load_chart_data(LPPositionState.selected_chart_position_id, 1),
                                ),
                                rx.button(
                                    "6h",
                                    size="1",
                                    variant="soft",
                                    color_scheme=rx.cond(LPPositionState.chart_hours == 6, "blue", "gray"),
                                    on_click=lambda: LPPositionState.load_chart_data(LPPositionState.selected_chart_position_id, 6),
                                ),
                                rx.button(
                                    "24h",
                                    size="1",
                                    variant="soft",
                                    color_scheme=rx.cond(LPPositionState.chart_hours == 24, "blue", "gray"),
                                    on_click=lambda: LPPositionState.load_chart_data(LPPositionState.selected_chart_position_id, 24),
                                ),
                                rx.button(
                                    "7d",
                                    size="1",
                                    variant="soft",
                                    color_scheme=rx.cond(LPPositionState.chart_hours == 168, "blue", "gray"),
                                    on_click=lambda: LPPositionState.load_chart_data(LPPositionState.selected_chart_position_id, 168),
                                ),
                                spacing="2",
                            ),
                            
                            # Chart
                            rx.recharts.area_chart(
                                rx.recharts.area(
                                    data_key="lp_value_usd",
                                    stroke="#8884d8",
                                    fill="#8884d8",
                                    fill_opacity=0.6,
                                    name="LP Value",
                                    stack_id="1",
                                ),
                                rx.recharts.area(
                                    data_key="hl_account_value",
                                    stroke="#82ca9d",
                                    fill="#82ca9d",
                                    fill_opacity=0.6,
                                    name="Hedge Account",
                                    stack_id="1",
                                ),
                                # Add a third invisible area for total to ensure it appears in tooltip
                                rx.recharts.area(
                                    data_key="total_value",
                                    stroke="transparent",
                                    fill="transparent",
                                    fill_opacity=0,
                                    name="Total Value",
                                    stack_id="1",
                                    legend_type="none",
                                ),
                                rx.recharts.x_axis(
                                    data_key="timestamp",
                                    angle=-45,
                                    text_anchor="end",
                                    height=80,
                                    tick={"fontSize": 12},
                                ),
                                rx.recharts.y_axis(),
                                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                                rx.recharts.legend(),
                                rx.recharts.tooltip(
                                    formatter=lambda value, name: (
                                        f"${float(value):.2f}" if isinstance(value, (int, float, str)) and value is not None else "$0.00",
                                        {
                                            "lp_value_usd": "LP Value",
                                            "hl_account_value": "Hedge Account",
                                            "total_value": "Total Value"
                                        }.get(name, name)
                                    ),
                                    label_formatter=lambda label: f"Time: {label}" if label else "Time: N/A",
                                ),
                                data=LPPositionState.chart_data,
                                width="100%",
                                height=400,
                            ),
                            
                            # Summary stats
                            rx.text(
                                f"Showing {LPPositionState.chart_data.length()} data points",
                                size="2",
                                color="gray",
                                margin_top="1rem",
                            ),
                            
                            spacing="4",
                            width="100%",
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("bar-chart-3", size=48, color="gray"),
                                rx.text("No chart data available", size="3", color="gray"),
                                rx.text("This position may not have hedge data logged yet", size="2", color="gray"),
                                spacing="2",
                            ),
                            padding="4rem",
                        ),
                    ),
                ),
                
                spacing="4",
                width="100%",
            ),
            max_width="900px",
            padding="1.5rem",
        ),
        open=LPPositionState.show_chart,
        on_open_change=LPPositionState.set_show_chart,
    )
