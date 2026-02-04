import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


def cookies_page() -> rx.Component:
    """Cookie Policy page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                # Header
                rx.heading(
                    "Cookie Policy",
                    size="9",
                    weight="bold",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Last Updated: February 4, 2026",
                    size="2",
                    color=COLORS.TEXT_MUTED,
                    margin_bottom="3rem",
                ),
                
                # What Are Cookies
                rx.box(
                    rx.heading(
                        "1. What Are Cookies",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Cookies are small text files that are placed on your device when you visit our website. They help us provide you with a better experience by remembering your preferences and understanding how you use our platform.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Types of Cookies
                rx.box(
                    rx.heading(
                        "2. Types of Cookies We Use",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Essential Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "These cookies are necessary for the platform to function properly. They enable core functionality such as authentication, security, and session management. You cannot opt-out of these cookies.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Performance Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "These cookies collect information about how you use our platform, such as which pages you visit most often. This data helps us improve our service and user experience.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Functional Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "These cookies remember your preferences and choices (such as language, region, or display settings) to provide a more personalized experience.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Analytics Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "We use analytics services to understand user behavior and improve our platform. These cookies collect anonymized data about your interactions with our service.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Third-Party Cookies
                rx.box(
                    rx.heading(
                        "3. Third-Party Cookies",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We may use third-party services that set cookies on your device, including:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Analytics providers (e.g., Google Analytics)", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Payment processors for subscription management", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Customer support and communication tools", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "These third parties have their own privacy policies and cookie policies, which we encourage you to review.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Managing Cookies
                rx.box(
                    rx.heading(
                        "4. Managing Cookies",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "You can control and manage cookies in several ways:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Browser Settings:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "Most browsers allow you to refuse or accept cookies, delete existing cookies, and set preferences for certain websites. Check your browser's help section for instructions.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Cookie Preferences:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "You can manage your cookie preferences through our platform settings. Note that disabling certain cookies may affect the functionality of our service.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Cookie Duration
                rx.box(
                    rx.heading(
                        "5. Cookie Duration",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Session Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "These temporary cookies are deleted when you close your browser.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Persistent Cookies:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "These cookies remain on your device for a set period or until you delete them. They help us remember your preferences across sessions.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Updates
                rx.box(
                    rx.heading(
                        "6. Updates to This Policy",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We may update this Cookie Policy from time to time to reflect changes in our practices or for legal reasons. We will notify you of any material changes by posting the updated policy on our website.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Contact
                rx.box(
                    rx.heading(
                        "7. Contact Us",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "If you have questions about our use of cookies, please contact us at:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "privacy@whisperhedge.com",
                        size="3",
                        color=COLORS.ACCENT_PRIMARY,
                        weight="bold",
                    ),
                ),
                
                    spacing="4",
                    align="start",
                    padding_y="4rem",
                ),
                max_width="60rem",
                margin_x="auto",
                padding_x="2rem",
            ),
            background=COLORS.BACKGROUND_PRIMARY,
            min_height="100vh",
            width="100%",
        ),
        footer(),
        spacing="0",
        width="100%",
    )
