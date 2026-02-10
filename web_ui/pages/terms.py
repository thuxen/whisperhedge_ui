import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


def terms_page() -> rx.Component:
    """Terms of Service page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                # Header
                rx.heading(
                    "Terms of Service",
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
                
                # Acceptance
                rx.box(
                    rx.heading(
                        "1. Acceptance of Terms",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "By accessing or using WhisperHedge's platform, you agree to be bound by these Terms of Service. If you do not agree to these terms, you may not use our services.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Service Description
                rx.box(
                    rx.heading(
                        "2. Service Description",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "WhisperHedge provides automated hedging services for liquidity pool positions on decentralized exchanges. Our platform:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Monitors your LP positions via on-chain data", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Executes hedging trades on perpetual exchanges using your API keys", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Provides risk management and IL mitigation strategies", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Does NOT have custody of your funds or private keys", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="2rem",
                    ),
                ),
                
                # User Responsibilities
                rx.box(
                    rx.heading(
                        "3. User Responsibilities",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "You are responsible for:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Maintaining sufficient collateral in your Hyperliquid account", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Securing your API keys and account credentials", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Providing accurate position information", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Understanding the risks of leveraged trading and hedging strategies", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Complying with all applicable laws and regulations", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Paying all applicable fees and overage charges", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Risk Disclosure
                rx.box(
                    rx.heading(
                        "4. Risk Disclosure",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "IMPORTANT: Trading cryptocurrencies and using hedging strategies involves substantial risk of loss. You acknowledge and accept that:",
                        size="3",
                        color=COLORS.ACCENT_WARNING,
                        line_height="1.8",
                        font_weight="bold",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Past performance does not guarantee future results", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Hedging strategies may not fully protect against losses", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Market volatility can result in liquidations", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Funding rates and fees can erode returns", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Smart contract risks and exchange risks exist", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• You may lose your entire investment", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Nature of Software and Financial Risk Disclosure
                rx.box(
                    rx.heading(
                        "4.5. Nature of Software and Financial Risk Disclosure",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Software Provider Status:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "WhisperCapital (the \"Company\") is a provider of technical software tools for market participants. The Company is NOT a registered investment advisor, broker-dealer, or financial institution. The software provided is a technical \"bridge\" that allows users to automate their own logic.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Non-Custodial Nature:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "At no point does the Company have access to, custody of, or control over User funds. All transactions are executed through the User's third-party exchange accounts via API keys provided by the User. Users are solely responsible for the security of their own API keys and exchange accounts.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Execution Risk:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "Automated \"hedging\" and trading bots carry inherent risks, including but not limited to API latency, market volatility, and software logic errors. The Company shall not be liable for any financial losses, \"slippage,\" or liquidated positions resulting from the use of the software.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "No Guarantee of Results:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "Any \"hedge\" strategies or templates provided within the software are for informational and illustrative purposes only. The Company does not guarantee the success of any strategy and does not provide financial advice.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "User Responsibility:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "The User acknowledges that they are using the software in a \"Self-Directed\" capacity. The User is responsible for verifying the settings of their \"bot\" and ensuring it aligns with their own risk tolerance.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Fees and Payment
                rx.box(
                    rx.heading(
                        "5. Fees and Payment",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Subscription Fees:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "You agree to pay the subscription fees for your selected tier (FREE, HOBBY, PRO, or ELITE) as described on our pricing page.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Overage Charges:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "If your total value locked (TVL) exceeds your tier's included amount, overage charges will apply based on your average monthly managed TVL. Overage rates: HOBBY (0.1%), PRO (0.05%), ELITE (0.05%).",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Cancellation:",
                        size="3",
                        weight="bold",
                        color=COLORS.TEXT_PRIMARY,
                        margin_bottom="0.5rem",
                    ),
                    rx.text(
                        "You may cancel your subscription at any time. Cancellations take effect at the end of the current billing cycle. No refunds for partial months.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Limitation of Liability
                rx.box(
                    rx.heading(
                        "6. Limitation of Liability",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "TO THE MAXIMUM EXTENT PERMITTED BY LAW, WHISPERHEDGE SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING LOSS OF PROFITS, DATA, OR OTHER INTANGIBLE LOSSES, RESULTING FROM YOUR USE OF OUR SERVICES.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Our total liability shall not exceed the amount you paid to WhisperHedge in the 12 months preceding the claim.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Service Availability
                rx.box(
                    rx.heading(
                        "7. Service Availability",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We strive to maintain 24/7 service availability but do not guarantee uninterrupted access. We may suspend or terminate services for maintenance, security, or legal compliance without liability.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Termination
                rx.box(
                    rx.heading(
                        "8. Termination",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We reserve the right to suspend or terminate your account if you violate these terms, engage in fraudulent activity, or for any reason at our discretion. Upon termination, all hedging activities will cease immediately.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Changes to Terms
                rx.box(
                    rx.heading(
                        "9. Changes to Terms",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We may modify these terms at any time. Continued use of our services after changes constitutes acceptance of the modified terms. We will notify you of material changes via email or platform notification.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                ),
                
                # Contact
                rx.box(
                    rx.heading(
                        "10. Contact",
                        size="6",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "For questions about these Terms of Service, contact us at:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "legal@whisperhedge.com",
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
