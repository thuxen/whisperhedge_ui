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
                                    content="""function(props) {
                                        if (!props.payload || props.payload.length === 0) {
                                            return null;
                                        }
                                        const data = props.payload[0].payload;
                                        const lpValue = parseFloat(data.lp_value_usd) || 0;
                                        const hedgeValue = parseFloat(data.hl_account_value) || 0;
                                        const totalValue = parseFloat(data.total_value) || (lpValue + hedgeValue);
                                        
                                        // Format with dollar signs
                                        const formatUSD = (val) => '$' + val.toFixed(2);
                                        
                                        // Create tooltip content
                                        const containerStyle = {
                                            backgroundColor: '#ffffff',
                                            border: '1px solid #ccc',
                                            borderRadius: '4px',
                                            padding: '10px',
                                            fontSize: '12px',
                                            fontFamily: 'sans-serif',
                                            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                                            minWidth: '180px'
                                        };
                                        
                                        const timeStyle = {
                                            margin: '0 0 8px 0',
                                            fontWeight: 'bold',
                                            color: '#333'
                                        };
                                        
                                        const itemStyle = {
                                            margin: '2px 0',
                                            display: 'flex',
                                            justifyContent: 'space-between'
                                        };
                                        
                                        const totalStyle = {
                                            margin: '8px 0 0 0',
                                            paddingTop: '8px',
                                            borderTop: '1px solid #ddd',
                                            fontWeight: 'bold',
                                            display: 'flex',
                                            justifyContent: 'space-between'
                                        };
                                        
                                        return React.createElement('div', {style: containerStyle}, [
                                            React.createElement('div', {key: 'time', style: timeStyle}, data.timestamp || ''),
                                            React.createElement('div', {key: 'lp', style: itemStyle}, [
                                                React.createElement('span', {style: {color: '#8884d8'}}, 'LP Value'),
                                                React.createElement('span', {style: {fontWeight: 'bold'}}, formatUSD(lpValue))
                                            ]),
                                            React.createElement('div', {key: 'hedge', style: itemStyle}, [
                                                React.createElement('span', {style: {color: '#82ca9d'}}, 'Hedge Account'),
                                                React.createElement('span', {style: {fontWeight: 'bold'}}, formatUSD(hedgeValue))
                                            ]),
                                            React.createElement('div', {key: 'total', style: totalStyle}, [
                                                React.createElement('span', {style: {color: '#ff7300'}}, 'Total'),
                                                React.createElement('span', {style: {fontWeight: 'bold', color: '#ff7300'}}, formatUSD(totalValue))
                                            ])
                                        ]);
                                    }""",
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
