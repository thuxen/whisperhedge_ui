import reflex as rx


class MobileWarningState(rx.State):
    """State for mobile warning dialog"""
    show_mobile_warning: bool = True
    
    def dismiss_mobile_warning(self):
        """User dismissed the mobile warning"""
        self.show_mobile_warning = False


def mobile_warning_dialog() -> rx.Component:
    """
    Full-page modal dialog that displays only on mobile devices.
    Informs users that the platform is optimized for desktop.
    """
    return rx.cond(
        MobileWarningState.show_mobile_warning,
        rx.box(
            rx.dialog.root(
                rx.dialog.content(
                    rx.vstack(
                        rx.center(
                            rx.text("📱", size="9"),
                        ),
                        rx.heading("Mobile Notice", size="6", text_align="center"),
                        rx.divider(),
                        rx.vstack(
                            rx.text(
                                "WhisperHedge is currently optimized for desktop browsers.",
                                size="3",
                                text_align="center",
                            ),
                            rx.text(
                                "Mobile monitoring features coming soon!",
                                size="3",
                                text_align="center",
                                weight="bold",
                                color="blue",
                            ),
                            rx.text(
                                "For the best experience, please use a desktop or laptop.",
                                size="2",
                                text_align="center",
                                color="gray",
                            ),
                            spacing="2",
                        ),
                        rx.divider(),
                        rx.dialog.close(
                            rx.button(
                                "I Understand",
                                size="3",
                                width="100%",
                                color_scheme="blue",
                                on_click=MobileWarningState.dismiss_mobile_warning,
                            ),
                        ),
                        spacing="4",
                        align_items="center",
                    ),
                    max_width="400px",
                ),
                open=True,
            ),
            display=["block", "block", "none"],  # Show on mobile/tablet, hide on desktop
        ),
    )
