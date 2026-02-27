import reflex as rx


def mobile_warning_banner() -> rx.Component:
    """
    Warning banner that displays only on mobile devices.
    Informs users that the platform is optimized for desktop.
    """
    return rx.box(
        rx.hstack(
            rx.text("📱", size="5"),
            rx.vstack(
                rx.text("Mobile Notice", weight="bold", size="3"),
                rx.text(
                    "WhisperHedge is currently optimized for desktop browsers. Mobile monitoring features coming soon!",
                    size="2"
                ),
                rx.text(
                    "For the best experience, please use a desktop or laptop.",
                    size="2",
                    color="gray"
                ),
                spacing="1",
                align_items="start",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        padding="1rem",
        background="var(--blue-3)",
        border="1px solid var(--blue-6)",
        border_radius="8px",
        margin_bottom="1rem",
        width="100%",
        display=["block", "block", "none"],  # Show on mobile/tablet, hide on desktop
    )
