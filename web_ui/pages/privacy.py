import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


def privacy_page() -> rx.Component:
    """Privacy Policy page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                    # Header
                    rx.heading(
                        "Privacy Policy",
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
                
                # Introduction
                rx.box(
                    rx.heading(
                        "1. Introduction",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "WhisperHedge (\"we,\" \"our,\" or \"us\") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our liquidity pool protection platform.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Information We Collect
                rx.box(
                    rx.heading(
                        "2. Information We Collect",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Personal Information:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "We may collect personal information that you provide directly to us, including but not limited to: email address, name, payment information, and API keys (trade-only, restricted access).",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Blockchain Data:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "We collect on-chain data related to your liquidity pool positions, including position IDs, token balances, and transaction history. This data is publicly available on the blockchain and is used solely to provide our hedging services.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Usage Data:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "We automatically collect certain information when you access our platform, including IP address, browser type, device information, and usage patterns.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # How We Use Your Information
                rx.box(
                    rx.heading(
                        "3. How We Use Your Information",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We use the information we collect to:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Provide and maintain our hedging services", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Execute trades on your behalf via restricted API keys", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Monitor and analyze your LP positions for risk management", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Process payments and manage subscriptions", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Send service notifications and alerts", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Improve our platform and develop new features", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Comply with legal obligations", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Data Security
                rx.box(
                    rx.heading(
                        "4. Data Security",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We implement industry-standard security measures to protect your information, including:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Encryption of data in transit and at rest", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Secure storage of API keys with restricted permissions", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Regular security audits and penetration testing", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Access controls and authentication mechanisms", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Important: We never have access to your private keys or custody of your funds. All trades are executed via trade-only API keys that you control.",
                        size="3",
                        color=COLORS.ACCENT_PRIMARY,
                        line_height="1.8",
                        font_weight="bold",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Data Sharing
                rx.box(
                    rx.heading(
                        "5. Data Sharing and Disclosure",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We do not sell your personal information. We may share your information only in the following circumstances:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• With service providers who assist in operating our platform", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• With exchanges (Hyperliquid) to execute trades on your behalf", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• To comply with legal obligations or respond to lawful requests", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• To protect our rights, privacy, safety, or property", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Your Rights
                rx.box(
                    rx.heading(
                        "6. Your Rights",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "You have the right to:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Access and review your personal information", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Request correction of inaccurate data", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Request deletion of your account and data", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Opt-out of marketing communications", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Revoke API key permissions at any time", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
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
                        "If you have questions about this Privacy Policy or our data practices, please contact us at:",
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
