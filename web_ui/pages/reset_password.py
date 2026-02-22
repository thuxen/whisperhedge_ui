import reflex as rx


def reset_password_page() -> rx.Component:
    """Step 1: Minimal page to confirm it loads from email link"""
    return rx.box(
        rx.text(
            "✅ Password Reset Page Loaded Successfully",
            size="8",
            weight="bold",
            color="green",
        ),
        padding="2rem",
        display="flex",
        justify_content="center",
        align_items="center",
        min_height="100vh",
    )
