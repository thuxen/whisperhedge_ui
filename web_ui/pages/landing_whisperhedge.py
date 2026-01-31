import reflex as rx
from ..branding import brand_logo, BrandConfig, COLORS


def navbar() -> rx.Component:
    """Navigation bar for WhisperHedge landing page"""
    return rx.box(
        rx.hstack(
            # Left: Logo/Name
            brand_logo(size="navbar"),
            
            # Center: Nav links
            rx.hstack(
                rx.link(
                    "Features",
                    href="#features",
                    size="3",
                    color=COLORS.NAVBAR_LINK,
                    _hover={"color": COLORS.NAVBAR_LINK_HOVER},
                ),
                rx.link(
                    "Pricing",
                    href="#pricing",
                    size="3",
                    color=COLORS.NAVBAR_LINK,
                    _hover={"color": COLORS.NAVBAR_LINK_HOVER},
                ),
                spacing="6",
                align="center",
            ),
            
            # Right: Login and Free Trial buttons
            rx.hstack(
                rx.link(
                    rx.button(
                        "Login",
                        variant="ghost",
                        size="3",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    href="/login",
                ),
                rx.link(
                    rx.button(
                        "Free Trial",
                        size="3",
                        background=COLORS.BUTTON_PRIMARY_BG,
                        color=COLORS.BUTTON_PRIMARY_TEXT,
                        _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    ),
                    href="/signup",
                ),
                spacing="4",
                align="center",
            ),
            
            justify="between",
            align="center",
            width="100%",
            padding="1rem 2rem",
        ),
        position="sticky",
        top="0",
        z_index="50",
        background=COLORS.NAVBAR_BG,
        border_bottom=f"1px solid {COLORS.NAVBAR_BORDER}",
        width="100%",
    )


def hero_section() -> rx.Component:
    """Hero section with main headline and CTA"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Stop Losing Your LP Gains to Market Swings.",
                    size="9",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1.5rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "WhisperHedge provides intelligent, asymmetric protection for concentrated liquidity. We don't just \"cover the position\"—we optimize your exposure so you keep your fees without getting liquidated by volatility.",
                    size="5",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    max_width="50rem",
                    margin_bottom="2rem",
                ),
                rx.link(
                    rx.button(
                        "Secure Your Position",
                        size="4",
                        background=COLORS.BUTTON_PRIMARY_BG,
                        color=COLORS.BUTTON_PRIMARY_TEXT,
                        _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    ),
                    href="/signup",
                ),
                spacing="5",
                align="center",
                padding_y="6rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
    )


def problem_section() -> rx.Component:
    """Section explaining why perfect hedging loses money"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Why \"Perfect Hedging\" is a Losing Game.",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="2rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Most bots try to maintain a 0-delta position. Between funding fees and rebalancing costs, you're usually paying away your entire yield just to stay \"neutral.\"",
                    size="5",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    max_width="50rem",
                    margin_bottom="1.5rem",
                ),
                rx.text(
                    "The WhisperHedge Difference:",
                    size="5",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "We specialize in Precision Hedging. Our algorithms focus on mitigating the \"tail risk\"—the big moves that actually hurt—while leaving you room to capture the upside of the yield.",
                    size="5",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    max_width="50rem",
                ),
                spacing="4",
                align="center",
                padding_y="6rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
    )


def features_section() -> rx.Component:
    """Key features section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Key Features",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    id="features",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.vstack(
                    # Feature 1: Asymmetric Protection
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Asymmetric Protection",
                                size="6",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Instead of a rigid 1:1 hedge, WhisperHedge uses calculated under-hedging to reduce your \"bleed\" during flat markets.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                    ),
                    # Feature 2: Dynamic Range Tracking
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Dynamic Range Tracking",
                                size="6",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Automatically adjusts your protection levels as your LP position moves through its price ticks.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                    ),
                    # Feature 3: Funding-Aware Execution
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Funding-Aware Execution",
                                size="6",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "The bot monitors perp funding rates; it won't open a hedge that costs more than the LP is earning.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                    ),
                    # Feature 4: Capital Efficiency
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Capital Efficiency",
                                size="6",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Keep your collateral working. We calculate the minimum necessary margin to protect your range, freeing up your capital for other plays.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                    ),
                    spacing="4",
                    width="100%",
                ),
                spacing="5",
                padding_y="6rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def whisperhedge_landing() -> rx.Component:
    """
    Custom landing page for whisperhedge.com
    
    This is your full-featured WhisperHedge landing page.
    You can customize this with hero sections, features, pricing, etc.
    """
    return rx.box(
        navbar(),
        hero_section(),
        problem_section(),
        features_section(),
        width="100%",
    )
