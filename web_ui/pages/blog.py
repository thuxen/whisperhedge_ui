import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


def blog_page() -> rx.Component:
    """Blog listing page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                # Header
                rx.heading(
                    "WhisperHedge Blog",
                    size="9",
                    weight="bold",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Insights on DeFi, liquidity provision, and risk management",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="3rem",
                ),
                
                # Featured post
                rx.link(
                    rx.box(
                        rx.vstack(
                            rx.badge("Featured", color_scheme="blue", size="2", margin_bottom="1rem"),
                            rx.heading(
                                "The Hidden Cost of Liquidity: Why Most LPs Are Losing Money",
                                size="7",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Impermanent loss isn't just a theoretical concept—it's actively draining billions from liquidity providers. In this deep dive, we explore why traditional LP strategies fail and how asymmetric hedging can protect your principal while maintaining fee generation.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.8",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("February 5, 2026", size="2", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="2", color=COLORS.TEXT_MUTED),
                                rx.text("8 min read", size="2", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"2px solid {COLORS.ACCENT_PRIMARY}",
                        background="rgba(59, 130, 246, 0.05)",
                        margin_bottom="3rem",
                        cursor="pointer",
                        _hover={"border": f"2px solid {COLORS.BUTTON_PRIMARY_HOVER}"},
                    ),
                    href="/blog/hidden-cost-of-liquidity",
                ),
                
                # Blog posts grid
                rx.grid(
                    # Post 1
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Understanding Delta-Neutral Strategies",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "A comprehensive guide to delta-neutral hedging, its limitations, and why under-hedging can be more profitable.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 28, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("6 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    # Post 2
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Hyperliquid Integration: Why We Chose a Decentralized Perp DEX",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Exploring the benefits of using Hyperliquid for hedging: deep liquidity, low fees, and true decentralization.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 25, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("5 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    # Post 3
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Funding Rates Explained: The Hidden Cost of Perpetual Hedging",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "How funding rates work, why they matter for your hedging strategy, and how WhisperHedge optimizes for net profitability.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 22, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("7 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    # Post 4
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Case Study: Protecting a $100K Uniswap V3 Position",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Real-world example of how WhisperHedge protected an ETH/USDC position through a 30% market drawdown.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 18, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("10 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    # Post 5
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The Math Behind Asymmetric Under-Hedging",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "A technical deep-dive into the quantitative models that power WhisperHedge's hedging strategies.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 15, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("12 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    # Post 6
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Security Best Practices: API Keys and Non-Custodial Architecture",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "How WhisperHedge maintains security without ever touching your private keys or holding custody of funds.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.text("January 10, 2026", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("•", size="1", color=COLORS.TEXT_MUTED),
                                rx.text("5 min read", size="1", color=COLORS.TEXT_MUTED),
                                spacing="2",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="1.5rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        cursor="pointer",
                        _hover={"border": f"1px solid {COLORS.ACCENT_PRIMARY}"},
                    ),
                    
                    columns="2",
                    spacing="4",
                    width="100%",
                    responsive={
                        "0px": {"columns": "1"},
                        "768px": {"columns": "2"},
                    },
                ),
                
                # Coming soon message
                rx.box(
                    rx.text(
                        "More articles coming soon. Subscribe to our newsletter to stay updated.",
                        size="2",
                        color=COLORS.TEXT_MUTED,
                        text_align="center",
                    ),
                    margin_top="3rem",
                    width="100%",
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
