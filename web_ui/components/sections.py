import reflex as rx
from .api_keys import api_keys_component


def overview_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Overview", size="7", margin_bottom="1rem"),
        rx.card(
            rx.vstack(
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text(
                    "This section is under development.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
                align_items="center",
                padding="4rem",
            ),
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def lp_positions_section() -> rx.Component:
    from .lp_positions import lp_positions_component
    return lp_positions_component()


def bot_status_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Bot Status", size="7", margin_bottom="1rem"),
        rx.card(
            rx.vstack(
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text(
                    "This section is under development.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
                align_items="center",
                padding="4rem",
            ),
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def settings_section() -> rx.Component:
    return rx.vstack(
        rx.heading("Settings", size="7", margin_bottom="1rem"),
        rx.card(
            rx.vstack(
                rx.heading("Coming Soon", size="6", color="gray"),
                rx.text(
                    "This section is under development.",
                    size="3",
                    color="gray",
                ),
                spacing="3",
                align_items="center",
                padding="4rem",
            ),
            width="100%",
        ),
        spacing="4",
        width="100%",
    )


def api_keys_section() -> rx.Component:
    return rx.vstack(
        rx.heading("API Keys", size="7", margin_bottom="1rem"),
        api_keys_component(),
        spacing="4",
        width="100%",
    )
