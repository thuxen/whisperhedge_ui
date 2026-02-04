import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


def about_page() -> rx.Component:
    """About Us page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                # Header
                rx.heading(
                    "About WhisperHedge",
                    size="9",
                    weight="bold",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Institutional-grade protection for liquidity providers",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="3rem",
                ),
                
                # Mission
                rx.box(
                    rx.heading(
                        "Our Mission",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "WhisperHedge was founded to solve a critical problem in decentralized finance: liquidity providers losing money to impermanent loss while market makers and sophisticated traders profit. We believe that providing liquidity should be a sustainable, profitable activity—not a gamble.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Our mission is to democratize access to institutional-grade hedging strategies, making advanced risk management tools available to every liquidity provider, regardless of their portfolio size.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="3rem",
                    ),
                ),
                
                # The Problem
                rx.box(
                    rx.heading(
                        "The Problem We Solve",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Traditional liquidity provision exposes LPs to several risks:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "Impermanent Loss:",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Price divergence between pooled assets can erode principal value, often exceeding fee earnings.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.8",
                            ),
                        ),
                        rx.box(
                            rx.text(
                                "Rebalance Bleed:",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Traditional delta-neutral strategies force constant rebalancing, turning temporary losses into permanent ones through slippage and fees.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.8",
                            ),
                        ),
                        rx.box(
                            rx.text(
                                "Volatility Risk:",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Market crashes can wipe out months of accumulated fees in a single event.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.8",
                            ),
                        ),
                        align="start",
                        spacing="3",
                        margin_bottom="3rem",
                    ),
                ),
                
                # Our Approach
                rx.box(
                    rx.heading(
                        "Our Approach",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "WhisperHedge uses asymmetric under-hedging strategies that:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Defend your principal without chasing perfect zero-delta", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Allow strategic variance to preserve upside potential", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Monitor funding rates to ensure net profitability", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Provide mathematical safety nets against black swan events", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Execute trades via non-custodial, trade-only API keys", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="3rem",
                    ),
                ),
                
                # Technology
                rx.box(
                    rx.heading(
                        "Technology & Security",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Built on cutting-edge infrastructure:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Real-time on-chain position monitoring", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Native integration with Hyperliquid's decentralized perp exchange", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Advanced risk calculation engine with priority execution tiers", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Zero-touch architecture—we never access your private keys", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Encrypted API key storage with restricted permissions", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="3rem",
                    ),
                ),
                
                # Team
                rx.box(
                    rx.heading(
                        "Our Team",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "WhisperHedge is built by a team of DeFi veterans, quantitative traders, and blockchain engineers who have experienced the pain of impermanent loss firsthand. We combine deep expertise in:",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("• Quantitative finance and risk management", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Decentralized exchange mechanics and liquidity provision", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• Smart contract development and security", size="3", color=COLORS.TEXT_SECONDARY),
                        rx.text("• High-frequency trading and execution systems", size="3", color=COLORS.TEXT_SECONDARY),
                        align="start",
                        spacing="2",
                        margin_bottom="3rem",
                    ),
                ),
                
                # Vision
                rx.box(
                    rx.heading(
                        "Our Vision",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "We envision a future where liquidity provision is a reliable, profitable activity for everyone—not just institutional players. By providing sophisticated risk management tools at an accessible price point, we're leveling the playing field and helping build a more sustainable DeFi ecosystem.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="1rem",
                    ),
                    rx.text(
                        "Our roadmap includes expanding to multiple DEXs, adding more advanced hedging strategies, and building a community of protected liquidity providers who can share insights and strategies.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="3rem",
                    ),
                ),
                
                # CTA
                rx.box(
                    rx.heading(
                        "Join Us",
                        size="7",
                        weight="bold",
                        margin_bottom="1rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Ready to protect your liquidity positions? Start with our free tier and experience institutional-grade hedging for yourself.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        line_height="1.8",
                        margin_bottom="2rem",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "Get Started Free",
                                size="3",
                                background=COLORS.BUTTON_PRIMARY_BG,
                                color=COLORS.BUTTON_PRIMARY_TEXT,
                                _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                            ),
                            href="/signup",
                        ),
                        rx.link(
                            rx.button(
                                "Contact Us",
                                size="3",
                                variant="outline",
                            ),
                            href="/contact",
                        ),
                        spacing="3",
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
