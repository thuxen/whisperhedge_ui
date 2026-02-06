import reflex as rx
from ..branding import brand_logo, BrandConfig, COLORS
from .landing_whisperhedge_mobile import (
    mobile_strategic_philosophy_section,
    mobile_features_section,
    mobile_how_it_works_section,
    mobile_pricing_section,
)


class MobileMenuState(rx.State):
    """State for mobile menu"""
    is_open: bool = False
    
    def toggle_menu(self):
        """Toggle mobile menu open/closed"""
        self.is_open = not self.is_open


def navbar() -> rx.Component:
    """Navigation bar for WhisperHedge landing page"""
    return rx.box(
        rx.hstack(
            # Left: Logo/Name (clickable to home, no link styling)
            rx.box(
                brand_logo(size="navbar"),
                on_click=rx.redirect("/"),
                cursor="pointer",
            ),
            
            # Center: Nav links (hidden on mobile)
            rx.hstack(
                rx.link(
                    "Features",
                    href="/#features",
                    size="3",
                    color=COLORS.NAVBAR_LINK,
                    _hover={"color": COLORS.NAVBAR_LINK_HOVER},
                ),
                rx.link(
                    "How it works",
                    href="/#how-it-works",
                    size="3",
                    color=COLORS.NAVBAR_LINK,
                    _hover={"color": COLORS.NAVBAR_LINK_HOVER},
                ),
                rx.link(
                    "Pricing",
                    href="/#pricing",
                    size="3",
                    color=COLORS.NAVBAR_LINK,
                    _hover={"color": COLORS.NAVBAR_LINK_HOVER},
                ),
                spacing="6",
                align="center",
                display=["none", "none", "flex"],
            ),
            
            # Right: Login and Free Trial buttons (hidden on mobile)
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
                display=["none", "none", "flex"],
            ),
            
            # Mobile: Hamburger menu button (shown only on mobile)
            rx.box(
                rx.button(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='3' y1='12' x2='21' y2='12'></line><line x1='3' y1='6' x2='21' y2='6'></line><line x1='3' y1='18' x2='21' y2='18'></line></svg>"),
                    variant="ghost",
                    size="3",
                    on_click=MobileMenuState.toggle_menu,
                ),
                display=["block", "block", "none"],
            ),
            
            justify="between",
            align="center",
            width="100%",
            padding="1rem 2rem",
        ),
        # Mobile menu dropdown
        rx.cond(
            MobileMenuState.is_open,
            rx.box(
                rx.vstack(
                    rx.link(
                        "Features",
                        href="/#features",
                        size="3",
                        color=COLORS.TEXT_PRIMARY,
                        width="100%",
                        padding="0.75rem 1rem",
                        _hover={"background": "rgba(59, 130, 246, 0.1)"},
                        on_click=MobileMenuState.toggle_menu,
                    ),
                    rx.link(
                        "How it works",
                        href="/#how-it-works",
                        size="3",
                        color=COLORS.TEXT_PRIMARY,
                        width="100%",
                        padding="0.75rem 1rem",
                        _hover={"background": "rgba(59, 130, 246, 0.1)"},
                        on_click=MobileMenuState.toggle_menu,
                    ),
                    rx.link(
                        "Pricing",
                        href="/#pricing",
                        size="3",
                        color=COLORS.TEXT_PRIMARY,
                        width="100%",
                        padding="0.75rem 1rem",
                        _hover={"background": "rgba(59, 130, 246, 0.1)"},
                        on_click=MobileMenuState.toggle_menu,
                    ),
                    rx.divider(margin_y="0.5rem"),
                    rx.link(
                        rx.button(
                            "Login",
                            variant="ghost",
                            size="3",
                            width="100%",
                        ),
                        href="/login",
                        width="100%",
                        on_click=MobileMenuState.toggle_menu,
                    ),
                    rx.link(
                        rx.button(
                            "Start Free Trial",
                            size="3",
                            background=COLORS.BUTTON_PRIMARY_BG,
                            color=COLORS.BUTTON_PRIMARY_TEXT,
                            _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                            width="100%",
                        ),
                        href="/signup",
                        width="100%",
                        on_click=MobileMenuState.toggle_menu,
                    ),
                    spacing="0",
                    width="100%",
                    align="start",
                ),
                background="rgba(15, 23, 42, 0.95)",
                backdrop_filter="blur(12px)",
                border_bottom=f"1px solid {COLORS.NAVBAR_BORDER}",
                padding="1rem",
                width="100%",
                display=["block", "block", "none"],
            ),
        ),
        position="sticky",
        top="0",
        z_index="50",
        background="rgba(15, 23, 42, 0.5)",
        backdrop_filter="blur(12px)",
        border_bottom=f"1px solid {COLORS.NAVBAR_BORDER}",
        width="100%",
    )


def hero_section() -> rx.Component:
    """Hero section with main headline and CTA"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.badge(
                    "AUTOMATED HEDGING BOT FOR LIQUIDITY PROVIDERS",
                    size="2",
                    color_scheme="blue",
                    margin_bottom="1rem",
                ),
                rx.heading(
                    "Automate Your LP Defense. Maximize Fee Retention.",
                    size="9",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1.5rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "WhisperHedge is an automated bot that protects your liquidity pool positions from Impermanent Loss. We execute strategic hedges on Hyperliquid while you continue earning fees—no manual intervention required.",
                    size="5",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    max_width="50rem",
                    margin_bottom="2rem",
                ),
                rx.link(
                    rx.button(
                        "Secure My LP Position",
                        size="4",
                        background=COLORS.BUTTON_PRIMARY_BG,
                        color=COLORS.BUTTON_PRIMARY_TEXT,
                        _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    ),
                    href="/signup",
                ),
                spacing="5",
                align="center",
                padding_top="4rem",
                padding_bottom="6rem",
            ),
            size="4",
            position="relative",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
        background_image=f"""
            radial-gradient(circle at center, rgba(59, 130, 246, 0.08) 0%, transparent 70%),
            linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)
        """,
        background_size="100% 100%, 40px 40px, 40px 40px",
    )


def risk_automation_section() -> rx.Component:
    """Risk automation focus section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.text(
                    "We focus on risk automation so you can focus on liquidity, yield, and opportunity. As a WhisperHedge user, you can finally close those complex tracking spreadsheets and stop second-guessing your hedge ratios. Our platform provides the real-time precision you need to defend your principal while ensuring your fee earnings aren't being devoured by rebalancing costs. It's time to move beyond manual management and start protecting your capital with institutional-grade logic.",
                    size="5",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    max_width="60rem",
                    line_height="1.8",
                ),
                # Dashboard image
                rx.image(
                    src="/whisperhedge_dashboard.png",
                    alt="WhisperHedge Dashboard Interface",
                    width="100%",
                    max_width="60rem",
                    border_radius="12px",
                    margin_top="3rem",
                    box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                ),
                align="center",
                padding_y="4rem",
            ),
            size="4",
        ),
        background="transparent",
    )


def strategic_philosophy_section() -> rx.Component:
    """The WhisperHedge Strategic Philosophy - Responsive version"""
    return rx.box(
        # Desktop version (hidden on mobile)
        rx.box(
            desktop_strategic_philosophy_content(),
            display=["none", "none", "block"],
        ),
        # Mobile version (hidden on desktop)
        rx.box(
            mobile_strategic_philosophy_section(),
            display=["block", "block", "none"],
        ),
        background="transparent",
    )


def desktop_strategic_philosophy_content() -> rx.Component:
    """Desktop version of Strategic Philosophy section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "The WhisperHedge Philosophy",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                    style={"scroll-margin-top": "100px"},
                ),
                rx.text(
                    "Why we abandoned standard delta-neutral strategies for something smarter.",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    margin_bottom="4rem",
                ),
                rx.grid(
                    # Card 1: Stop the "Rebalance Bleed"
                    rx.box(
                        rx.vstack(
                            # Icon placeholder - Shield
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.text(
                                "STRATEGY 01",
                                size="1",
                                weight="bold",
                                color=COLORS.ACCENT_PRIMARY,
                                letter_spacing="0.1em",
                                text_transform="uppercase",
                                margin_bottom="0.5rem",
                            ),
                            rx.heading(
                                "Stop the \"Rebalance Bleed\"",
                                size="5",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "The Delta-Neutral Trap",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_SECONDARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Chasing a static 0-delta in a dynamic pool is a losing game. Most bots force you to rebalance on every tick, turning \"Impermanent\" loss into \"Permanent\" loss through constant slippage and fees. We allow for strategic variance, protecting your upside while defending the core.",
                                size="2",
                                color="#94A3B8",
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        _hover={"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        transition="border 0.3s ease",
                    ),
                    # Card 2: Defend Your Principal
                    rx.box(
                        rx.vstack(
                            # Icon placeholder - Scale
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='3' x2='12' y2='21'></line><path d='M8 9l4-4 4 4'></path><path d='M16 15l-4 4-4-4'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.text(
                                "STRATEGY 02",
                                size="1",
                                weight="bold",
                                color=COLORS.ACCENT_PRIMARY,
                                letter_spacing="0.1em",
                                text_transform="uppercase",
                                margin_bottom="0.5rem",
                            ),
                            rx.heading(
                                "Defend Your Principal",
                                size="5",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Real-Time IL Mitigation",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_SECONDARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Impermanent Loss is the \"invisible tax\" on LPs. WhisperHedge identifies price divergence early and opens targeted offsets on perpetual exchanges. We don't just watch your position go out of range; we defend the value of the tokens you started with.",
                                size="2",
                                color="#94A3B8",
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        _hover={"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        transition="border 0.3s ease",
                    ),
                    # Card 3: Master the Volatility
                    rx.box(
                        rx.vstack(
                            # Icon placeholder - Trend Down
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='23 6 13.5 15.5 8.5 10.5 1 18'></polyline><polyline points='17 6 23 6 23 12'></polyline></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.text(
                                "STRATEGY 03",
                                size="1",
                                weight="bold",
                                color=COLORS.ACCENT_PRIMARY,
                                letter_spacing="0.1em",
                                text_transform="uppercase",
                                margin_bottom="0.5rem",
                            ),
                            rx.heading(
                                "Master the Volatility",
                                size="5",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Optimized Drawdowns",
                                size="3",
                                weight="bold",
                                color=COLORS.TEXT_SECONDARY,
                                margin_bottom="0.5rem",
                            ),
                            rx.text(
                                "Market crashes shouldn't wipe out months of fee accumulation. By using asymmetric under-hedging, we provide a mathematical safety net that softens the impact of \"black swan\" events without the high overhead costs of a traditional 1:1 hedge.",
                                size="2",
                                color="#94A3B8",
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        _hover={"border": "1px solid rgba(59, 130, 246, 0.5)"},
                        transition="border 0.3s ease",
                    ),
                    columns="3",
                    spacing="4",
                    width="100%",
                    responsive={
                        "0px": {"columns": "1", "spacing": "3"},
                        "768px": {"columns": "3", "spacing": "4"},
                    },
                ),
                spacing="5",
                align="center",
                padding_y="4rem",
                padding_x="1rem",
            ),
            size="4",
        ),
        background="transparent",
    )


def features_section() -> rx.Component:
    """Core Features section - Responsive version"""
    return rx.box(
        # Desktop version (hidden on mobile)
        rx.box(
            desktop_features_content(),
            display=["none", "none", "block"],
        ),
        # Mobile version (hidden on desktop)
        rx.box(
            mobile_features_section(),
            display=["block", "block", "none"],
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def desktop_features_content() -> rx.Component:
    """Desktop version of Core Features section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Core Features",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1rem",
                    id="features",
                    color=COLORS.TEXT_PRIMARY,
                    style={"scroll-margin-top": "100px"},
                ),
                rx.text(
                    "Engineered for Performance. Built for Security.",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    margin_bottom="4rem",
                ),
                rx.grid(
                    # Feature 1: Smart Exposure Management
                    rx.box(
                        rx.vstack(
                            # BarChart3 Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'></path><path d='M18 17V9'></path><path d='M13 17V5'></path><path d='M8 17v-3'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Smart Exposure Management",
                                size="5",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "We don't chase \"Perfect Zero\" delta. WhisperHedge monitors your pool's active tick-range and maintains a flexible, asymmetric hedge. You get robust protection against catastrophic price divergence without the constant rebalancing fees that eat your yield.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    # Feature 2: Native Hyperliquid Integration
                    rx.box(
                        rx.vstack(
                            # Zap Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'></polygon></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.hstack(
                                rx.heading(
                                    "Native Hyperliquid Integration",
                                    size="5",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.badge(
                                    "Decentralized",
                                    size="1",
                                    color_scheme="blue",
                                ),
                                spacing="2",
                                align="center",
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Experience the power of the world's leading decentralized perp exchange. By anchoring our engine to Hyperliquid, we provide institutional-grade execution speed and deep liquidity, all while keeping your hedging strategy entirely on-chain and transparent.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    # Feature 3: Net-Profit Optimization
                    rx.box(
                        rx.vstack(
                            # Coins Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='8' cy='8' r='6'></circle><path d='M18.09 10.37A6 6 0 1 1 10.34 18'></path><path d='M7 6h1v4'></path><path d='m16.71 13.88.7.71-2.82 2.82'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Net-Profit Optimization",
                                size="5",
                                weight="bold",
                                color=COLORS.TEXT_PRIMARY,
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "Most bots hedge blindly. WhisperHedge is funding-aware; it constantly monitors perp funding rates against your LP fee generation. If a hedge becomes too expensive to maintain, the algorithm optimizes your position to ensure you stay in the green.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    # Feature 4: Zero-Touch Architecture
                    rx.box(
                        rx.vstack(
                            # ShieldCheck Icon (emerald color)
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'></path><path d='m9 12 2 2 4-4'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Zero-Touch Architecture",
                                size="5",
                                weight="bold",
                                color="#10B981",
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "We never connect to your wallet or touch your principal. By simply referencing your public LP position, WhisperHedge manages your defense via restricted, trade-only API keys. Your funds stay exactly where they belong—under your total control.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                    responsive={
                        "0px": {"columns": "1", "spacing": "3"},
                        "768px": {"columns": "2", "spacing": "4"},
                    },
                ),
                # DEX Coverage Section
                rx.vstack(
                    rx.heading(
                        "Broad DEX Coverage",
                        size="7",
                        weight="bold",
                        text_align="center",
                        margin_bottom="0.5rem",
                        color=COLORS.TEXT_PRIMARY,
                    ),
                    rx.text(
                        "Protecting liquidity across the most active venues in DeFi.",
                        size="3",
                        color=COLORS.TEXT_SECONDARY,
                        text_align="center",
                        margin_bottom="2rem",
                    ),
                    rx.hstack(
                        # Uniswap V3 - Live
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Uniswap V3",
                                        size="4",
                                        weight="bold",
                                        color=COLORS.TEXT_PRIMARY,
                                    ),
                                    rx.badge(
                                        rx.hstack(
                                            rx.html("<span style='display:inline-block;width:6px;height:6px;background:#10B981;border-radius:50%;animation:pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;'></span><style>@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }</style>"),
                                            rx.text("LIVE", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        color_scheme="green",
                                        size="1",
                                    ),
                                    spacing="2",
                                    align="center",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "All Chains",
                                    size="1",
                                    color=COLORS.TEXT_MUTED,
                                ),
                                align="center",
                                spacing="1",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid #10B981",
                            background="rgba(15, 23, 42, 0.6)",
                        ),
                        # Uniswap V4 - Coming Soon
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Uniswap V4",
                                        size="4",
                                        weight="bold",
                                        color="#64748B",
                                    ),
                                    rx.badge(
                                        "SOON",
                                        color_scheme="gray",
                                        size="1",
                                    ),
                                    spacing="2",
                                    align="center",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "Ethereum",
                                    size="1",
                                    color="#475569",
                                ),
                                align="center",
                                spacing="1",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid #334155",
                            background="rgba(15, 23, 42, 0.6)",
                            opacity="0.7",
                        ),
                        # Aerodrome - Coming Soon
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Aerodrome",
                                        size="4",
                                        weight="bold",
                                        color="#64748B",
                                    ),
                                    rx.badge(
                                        "SOON",
                                        color_scheme="gray",
                                        size="1",
                                    ),
                                    spacing="2",
                                    align="center",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "Base",
                                    size="1",
                                    color="#475569",
                                ),
                                align="center",
                                spacing="1",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid #334155",
                            background="rgba(15, 23, 42, 0.6)",
                            opacity="0.7",
                        ),
                        # Raydium - Coming Soon
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Raydium",
                                        size="4",
                                        weight="bold",
                                        color="#64748B",
                                    ),
                                    rx.badge(
                                        "SOON",
                                        color_scheme="gray",
                                        size="1",
                                    ),
                                    spacing="2",
                                    align="center",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "Solana",
                                    size="1",
                                    color="#475569",
                                ),
                                align="center",
                                spacing="1",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid #334155",
                            background="rgba(15, 23, 42, 0.6)",
                            opacity="0.7",
                        ),
                        # Orca - Coming Soon
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.heading(
                                        "Orca",
                                        size="4",
                                        weight="bold",
                                        color="#64748B",
                                    ),
                                    rx.badge(
                                        "SOON",
                                        color_scheme="gray",
                                        size="1",
                                    ),
                                    spacing="2",
                                    align="center",
                                    margin_bottom="0.5rem",
                                ),
                                rx.text(
                                    "Solana",
                                    size="1",
                                    color="#475569",
                                ),
                                align="center",
                                spacing="1",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid #334155",
                            background="rgba(15, 23, 42, 0.6)",
                            opacity="0.7",
                        ),
                        spacing="3",
                        wrap="wrap",
                        justify="center",
                        responsive={
                            "0px": {"spacing": "2"},
                            "768px": {"spacing": "3"},
                        },
                    ),
                    align="center",
                    spacing="3",
                    margin_top="4rem",
                ),
                spacing="5",
                align="center",
                padding_y="4rem",
                padding_x="1rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def how_it_works_section() -> rx.Component:
    """How It Works - Responsive version"""
    return rx.box(
        # Desktop version (hidden on mobile)
        rx.box(
            desktop_how_it_works_content(),
            display=["none", "none", "block"],
        ),
        # Mobile version (hidden on desktop)
        rx.box(
            mobile_how_it_works_section(),
            display=["block", "block", "none"],
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def desktop_how_it_works_content() -> rx.Component:
    """Desktop version of How It Works section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "How It Works",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1rem",
                    id="how-it-works",
                    color=COLORS.TEXT_PRIMARY,
                    style={"scroll-margin-top": "100px"},
                ),
                rx.text(
                    "Three steps to institutional-grade LP protection.",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    margin_bottom="4rem",
                ),
                rx.hstack(
                    # Step 1: Reference Your Position
                    rx.box(
                        rx.vstack(
                            # Fingerprint Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M2 12C2 6.5 6.5 2 12 2a10 10 0 0 1 8 4'></path><path d='M5 19.5C5.5 18 6 15 6 12c0-.7.12-1.37.34-2'></path><path d='M17.29 21.02c.12-.6.43-2.3.5-3.02'></path><path d='M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4'></path><path d='M8.65 22c.21-.66.45-1.32.57-2'></path><path d='M14 13.12c0 2.38 0 6.38-1 8.88'></path><path d='M2 16h.01'></path><path d='M21.8 16c.2-2 .131-5.354 0-6'></path><path d='M9 6.8a6 6 0 0 1 9 5.2c0 .47 0 1.17-.02 2'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Reference Your Position",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                                text_align="center",
                            ),
                            rx.text(
                                "Input your specific Liquidity Pool Position ID. WhisperHedge doesn't need to scan your entire wallet or request a connection. We simply pull the real-time on-chain data for that specific position to calculate your exposure.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                text_align="center",
                                line_height="1.6",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        flex="1",
                    ),
                    # Arrow connector
                    rx.box(
                        rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.5)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='5' y1='12' x2='19' y2='12'></line><polyline points='12 5 19 12 12 19'></polyline></svg>"),
                        display="flex",
                        align_items="center",
                        responsive={
                            "0px": {"display": "none"},
                            "768px": {"display": "flex"},
                        },
                    ),
                    # Step 2: Link Your Defense
                    rx.box(
                        rx.vstack(
                            # Key Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='7.5' cy='15.5' r='5.5'></circle><path d='m21 2-9.6 9.6'></path><path d='m15.5 7.5 3 3L22 7l-3-3'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Link Your Defense",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                                text_align="center",
                            ),
                            rx.text(
                                "Generate a restricted, trade-only API key on Hyperliquid and ensure your account has sufficient collateral. Your funds stay in your Hyperliquid account—WhisperHedge simply uses the API to execute the necessary defensive offsets.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                text_align="center",
                                line_height="1.6",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        flex="1",
                    ),
                    # Arrow connector
                    rx.box(
                        rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.5)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='5' y1='12' x2='19' y2='12'></line><polyline points='12 5 19 12 12 19'></polyline></svg>"),
                        display="flex",
                        align_items="center",
                        responsive={
                            "0px": {"display": "none"},
                            "768px": {"display": "flex"},
                        },
                    ),
                    # Step 3: Activate Automation
                    rx.box(
                        rx.vstack(
                            # Activity/Play Icon
                            rx.box(
                                rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 12h-4l-3 9L9 3l-3 9H2'></path></svg>"),
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Activate Automation",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                                text_align="center",
                            ),
                            rx.text(
                                "Choose between Manual tactical hedging or our Dynamic automated engine. Once live, the system monitors price ticks and funding rates 24/7, adjusting your hedge to defend your principal while you collect fees.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                text_align="center",
                                line_height="1.6",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                        flex="1",
                    ),
                    spacing="3",
                    width="100%",
                    align="center",
                    responsive={
                        "0px": {"flex_direction": "column", "spacing": "4"},
                        "768px": {"flex_direction": "row", "spacing": "3"},
                    },
                ),
                spacing="5",
                align="center",
                padding_y="4rem",
                padding_x="1rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def comparison_table_section() -> rx.Component:
    """Comparison table - What are we actually doing?"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "What are we actually doing?",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Scenario", color=COLORS.TEXT_PRIMARY),
                                rx.table.column_header_cell("Without WhisperHedge", color=COLORS.TEXT_PRIMARY),
                                rx.table.column_header_cell("With WhisperHedge", color=COLORS.TEXT_PRIMARY),
                            ),
                        ),
                        rx.table.body(
                            rx.table.row(
                                rx.table.cell("Market drops 20%", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("You lose 20% of LP value", color=COLORS.ACCENT_WARNING),
                                rx.table.cell("Hedge offsets most of the loss", color=COLORS.ACCENT_SUCCESS),
                            ),
                            rx.table.row(
                                rx.table.cell("Market stays flat", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("You earn LP fees", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("You earn LP fees minus small hedge cost", color=COLORS.TEXT_SECONDARY),
                            ),
                            rx.table.row(
                                rx.table.cell("Market pumps 30%", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("You gain on LP value", color=COLORS.ACCENT_SUCCESS),
                                rx.table.cell("Reduced gain, but protected from crashes", color=COLORS.TEXT_SECONDARY),
                            ),
                        ),
                        variant="surface",
                        size="3",
                    ),
                    padding="2rem",
                    border_radius="8px",
                    border=f"1px solid {COLORS.BORDER_SUBTLE}",
                    background="rgba(15, 23, 42, 0.5)",
                    backdrop_filter="blur(12px)",
                    width="100%",
                ),
                spacing="5",
                padding_y="6rem",
            ),
            size="4",
        ),
        background="transparent",
    )


def pricing_section() -> rx.Component:
    """Simple, Transparent Pricing - Responsive version"""
    return rx.box(
        # Desktop version (hidden on mobile)
        rx.box(
            desktop_pricing_content(),
            display=["none", "none", "block"],
        ),
        # Mobile version (hidden on desktop)
        rx.box(
            mobile_pricing_section(),
            display=["block", "block", "none"],
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def desktop_pricing_content() -> rx.Component:
    """Desktop version of Pricing section"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Simple, Transparent Pricing",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="1rem",
                    id="pricing",
                    color=COLORS.TEXT_PRIMARY,
                    style={"scroll-margin-top": "100px"},
                ),
                rx.text(
                    "Professional protection that scales with your liquidity.",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    text_align="center",
                    margin_bottom="4rem",
                ),
                rx.grid(
                    # Tier 1: FREE
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "FREE",
                                size="2",
                                weight="bold",
                                color=COLORS.TEXT_SECONDARY,
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.heading(
                                    "$0",
                                    size="8",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "/mo",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="end",
                                spacing="1",
                                margin_bottom="1rem",
                            ),
                            rx.divider(margin_y="1rem"),
                            rx.vstack(
                                rx.text(
                                    "1 LP Position",
                                    size="3",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "$2,500 TVL Hard Cap",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                    margin_bottom="1rem",
                                ),
                                rx.vstack(
                                    rx.text("✓ Standard Execution", size="2", color=COLORS.TEXT_SECONDARY),
                                    rx.text("✓ Hyperliquid Integration", size="2", color=COLORS.TEXT_SECONDARY),
                                    rx.text("✓ All Strategies", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="2",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.link(
                                rx.button(
                                    "Get Started",
                                    size="3",
                                    variant="outline",
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                href="/signup",
                                width="100%",
                            ),
                            align="start",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    # Tier 2: HOBBY
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "HOBBY",
                                size="2",
                                weight="bold",
                                color=COLORS.TEXT_SECONDARY,
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.heading(
                                    "$19.99",
                                    size="8",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "/mo",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="end",
                                spacing="1",
                                margin_bottom="1rem",
                            ),
                            rx.divider(margin_y="1rem"),
                            rx.vstack(
                                rx.text(
                                    "3 LP Positions",
                                    size="3",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "$10,000 Included TVL",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                rx.text(
                                    "0.1% (10 bps) on excess TVL",
                                    size="2",
                                    color=COLORS.TEXT_MUTED,
                                    font_style="italic",
                                    margin_bottom="1rem",
                                ),
                                rx.vstack(
                                    rx.text("✓ Standard Execution", size="2", color=COLORS.TEXT_SECONDARY),
                                    rx.text("✓ Email Alerts", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="2",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.link(
                                rx.button(
                                    "Get Started",
                                    size="3",
                                    variant="outline",
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                href="/signup",
                                width="100%",
                            ),
                            align="start",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    # Tier 3: PRO (Most Popular)
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.text(
                                    "PRO",
                                    size="2",
                                    weight="bold",
                                    color=COLORS.ACCENT_PRIMARY,
                                    text_transform="uppercase",
                                    letter_spacing="0.1em",
                                ),
                                rx.badge(
                                    "Most Popular",
                                    color_scheme="blue",
                                    size="1",
                                ),
                                spacing="2",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.heading(
                                    "$49.99",
                                    size="8",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "/mo",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="end",
                                spacing="1",
                                margin_bottom="1rem",
                            ),
                            rx.divider(margin_y="1rem"),
                            rx.vstack(
                                rx.text(
                                    "10 LP Positions",
                                    size="3",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "$50,000 Included TVL",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                rx.text(
                                    "0.05% (5 bps) on excess TVL",
                                    size="2",
                                    color=COLORS.TEXT_MUTED,
                                    font_style="italic",
                                    margin_bottom="1rem",
                                ),
                                rx.vstack(
                                    rx.text("✓ Priority Execution", size="2", color=COLORS.ACCENT_PRIMARY, weight="bold"),
                                    rx.text("✓ Multi-DEX Roadmap Access", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="2",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.link(
                                rx.button(
                                    "Get Started",
                                    size="3",
                                    background=COLORS.BUTTON_PRIMARY_BG,
                                    color=COLORS.BUTTON_PRIMARY_TEXT,
                                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                href="/signup",
                                width="100%",
                            ),
                            align="start",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"2px solid {COLORS.ACCENT_PRIMARY}",
                        background="rgba(15, 23, 42, 0.4)",
                        box_shadow="0 0 20px rgba(59, 130, 246, 0.3)",
                    ),
                    # Tier 4: ELITE
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "ELITE",
                                size="2",
                                weight="bold",
                                color="#D4AF37",
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                margin_bottom="1rem",
                            ),
                            rx.hstack(
                                rx.heading(
                                    "$149.99",
                                    size="8",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "/mo",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                align="end",
                                spacing="1",
                                margin_bottom="1rem",
                            ),
                            rx.divider(margin_y="1rem"),
                            rx.vstack(
                                rx.text(
                                    "Unlimited LP Positions",
                                    size="3",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "$250,000 Included TVL",
                                    size="2",
                                    color=COLORS.TEXT_SECONDARY,
                                ),
                                rx.text(
                                    "0.05% (5 bps) on excess TVL",
                                    size="2",
                                    color=COLORS.TEXT_MUTED,
                                    font_style="italic",
                                    margin_bottom="1rem",
                                ),
                                rx.vstack(
                                    rx.text("✓ Elite Priority Calculation Engine", size="2", color="#D4AF37", weight="bold"),
                                    rx.text("   (Top-of-queue rebalancing)", size="1", color="#B8960F", font_style="italic"),
                                    rx.text("✓ Direct Dev Support", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="2",
                                ),
                                align="start",
                                spacing="2",
                            ),
                            rx.link(
                                rx.button(
                                    "Get Started",
                                    size="3",
                                    background=COLORS.BUTTON_PRIMARY_BG,
                                    color=COLORS.BUTTON_PRIMARY_TEXT,
                                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                                    width="100%",
                                    margin_top="1rem",
                                ),
                                href="/signup",
                                width="100%",
                            ),
                            align="start",
                            spacing="3",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #D4AF37",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    columns="4",
                    spacing="4",
                    width="100%",
                    responsive={
                        "0px": {"columns": "1", "spacing": "3"},
                        "768px": {"columns": "2", "spacing": "4"},
                        "1024px": {"columns": "4", "spacing": "4"},
                    },
                ),
                # Disclaimer footer - moved directly under pricing boxes
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Overage charges are calculated based on your average monthly managed TVL and billed at the end of each cycle. Priority Calculation ensures your positions are analyzed and rebalanced first during high-volatility events.",
                            size="2",
                            color=COLORS.TEXT_MUTED,
                            text_align="center",
                            line_height="1.6",
                        ),
                        rx.text(
                            "TVL (Total Value Locked) = LP Position Value + Hyperliquid Hedge Account Value",
                            size="2",
                            color=COLORS.TEXT_MUTED,
                            text_align="center",
                            line_height="1.6",
                        ),
                        spacing="2",
                    ),
                    padding="2rem",
                    border_radius="8px",
                    background="rgba(15, 23, 42, 0.3)",
                    border=f"1px solid #1E293B",
                    margin_top="2rem",
                ),
                # Whale custom solution link
                rx.box(
                    rx.text(
                        "Need a custom solution for $5M+ TVL? ",
                        rx.link(
                            "Talk to our team.",
                            href="/contact",
                            color=COLORS.ACCENT_PRIMARY,
                            text_decoration="underline",
                            _hover={"color": COLORS.BUTTON_PRIMARY_HOVER},
                        ),
                        size="2",
                        color=COLORS.TEXT_SECONDARY,
                        text_align="center",
                    ),
                    margin_top="2rem",
                    width="100%",
                ),
                # Trust/Safety Footer
                rx.hstack(
                    rx.hstack(
                        rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m9 12 2 2 4-4'></path><circle cx='12' cy='12' r='10'></circle></svg>"),
                        rx.text(
                            "No Credit Card Required for Free Tier",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8'></path><path d='M3 3v5h5'></path></svg>"),
                        rx.text(
                            "Cancel or Upgrade Anytime",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'></path><path d='m9 12 2 2 4-4'></path></svg>"),
                        rx.text(
                            "Non-Custodial: We never touch your private keys",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    spacing="6",
                    justify="center",
                    wrap="wrap",
                    margin_top="3rem",
                    width="100%",
                ),
                spacing="5",
                align="center",
                padding_y="4rem",
                padding_x="1rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def faq_section() -> rx.Component:
    """FAQ section with accordion-style questions"""
    return rx.box(
        rx.container(
            rx.vstack(
                # Section header
                rx.heading(
                    "Frequently Asked Questions",
                    size="8",
                    weight="bold",
                    margin_bottom="3rem",
                    text_align="center",
                    color=COLORS.TEXT_PRIMARY,
                    id="faq",
                    scroll_margin_top="100px",
                ),
                
                # FAQ Accordion
                rx.vstack(
                    # Q1: Do I need to connect my wallet?
                    rx.accordion.root(
                        rx.accordion.item(
                            header=rx.accordion.header(
                                rx.text(
                                    "Do I need to connect my wallet?",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                            ),
                            content=rx.accordion.content(
                                rx.text(
                                    "No. WhisperHedge is non-custodial. We only require your public LP Position ID to monitor your data and a restricted API key from Hyperliquid to execute the hedge. We never have access to your private keys or your principal.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    line_height="1.8",
                                ),
                            ),
                            value="q1",
                        ),
                        # Q2: How often does the bot rebalance my hedge?
                        rx.accordion.item(
                            header=rx.accordion.header(
                                rx.text(
                                    "How often does the bot rebalance my hedge?",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                            ),
                            content=rx.accordion.content(
                                rx.text(
                                    "The bot monitors the market 24/7. Rebalancing checks are made every minute and rebalance trades are executed when the delta has shifted according to your position settings. In Dynamic mode, the engine triggers an adjustment whenever your delta or price-range exposure deviates beyond your set threshold.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    line_height="1.8",
                                ),
                            ),
                            value="q2",
                        ),
                        # Q3: What happens if Hyperliquid goes down?
                        rx.accordion.item(
                            header=rx.accordion.header(
                                rx.text(
                                    "What happens if Hyperliquid goes down?",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                            ),
                            content=rx.accordion.content(
                                rx.text(
                                    "WhisperHedge is built with fail-safes. If our connection to Hyperliquid is interrupted, the system will alert you immediately via your dashboard and email. However, since your LP position is on-chain (e.g., Uniswap), your principal remains unaffected.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    line_height="1.8",
                                ),
                            ),
                            value="q3",
                        ),
                        # Q4: How are overage charges billed?
                        rx.accordion.item(
                            header=rx.accordion.header(
                                rx.text(
                                    "How are overage charges billed?",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                            ),
                            content=rx.accordion.content(
                                rx.text(
                                    "We calculate your \"Average Managed TVL\" across the month. If you exceed your plan's included limit, the overage (0.05% or 0.1% depending on the plan) is added to your next billing cycle.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    line_height="1.8",
                                ),
                            ),
                            value="q4",
                        ),
                        # Q5: How do you handle liquidation risk on the Hyperliquid side?
                        rx.accordion.item(
                            header=rx.accordion.header(
                                rx.text(
                                    "How do you handle liquidation risk on the Hyperliquid side?",
                                    size="4",
                                    weight="bold",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                            ),
                            content=rx.accordion.content(
                                rx.text(
                                    "Safety is our priority. WhisperHedge includes built-in Collateral Monitoring. If your Hyperliquid margin ratio drops below a safe level due to aggressive price moves, the system will alert you immediately or—depending on your settings—automatically trim the hedge to prevent liquidation of your collateral.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    line_height="1.8",
                                ),
                            ),
                            value="q5",
                        ),
                        collapsible=True,
                        variant="ghost",
                        width="100%",
                    ),
                    spacing="0",
                    width="100%",
                    max_width="800px",
                    margin_x="auto",
                ),
                
                # Final CTA
                rx.box(
                    rx.link(
                        rx.button(
                            "Ready to protect your liquidity? Start Free Now",
                            size="4",
                            background=COLORS.BUTTON_PRIMARY_BG,
                            color=COLORS.BUTTON_PRIMARY_TEXT,
                            _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                            padding_x="3rem",
                            padding_y="1.5rem",
                            font_size="1.1rem",
                            font_weight="bold",
                        ),
                        href="/signup",
                    ),
                    margin_top="4rem",
                    text_align="center",
                    width="100%",
                ),
                
                spacing="4",
                align="center",
                padding_y="4rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def footer() -> rx.Component:
    """Footer section with links and copyright"""
    return rx.box(
        rx.container(
            rx.vstack(
                # Top section with links
                rx.box(
                    # Desktop: Horizontal layout
                    rx.hstack(
                        # Company column
                        rx.vstack(
                            rx.heading(
                                "WhisperHedge",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Intelligent protection for liquidity pool positions.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                max_width="15rem",
                            ),
                            align="start",
                            spacing="2",
                        ),
                        # Product column
                        rx.vstack(
                            rx.heading(
                                "Product",
                                size="4",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("Features", href="#features", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("How it works", href="#how-it-works", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Pricing", href="#pricing", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                        ),
                        # Company column
                        rx.vstack(
                            rx.heading(
                                "Company",
                                size="4",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("About Us", href="/about", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Blog", href="/blog", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Contact", href="/contact", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                        ),
                        # Legal column
                        rx.vstack(
                            rx.heading(
                                "Legal",
                                size="4",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("Privacy Policy", href="/privacy", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Terms of Service", href="/terms", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Cookie Policy", href="/cookies", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                        ),
                        justify="between",
                        width="100%",
                        spacing="8",
                        display=["none", "none", "flex"],
                    ),
                    # Mobile: Vertical layout
                    rx.vstack(
                        # Company column
                        rx.vstack(
                            rx.heading(
                                "WhisperHedge",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Intelligent protection for liquidity pool positions.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                            ),
                            align="start",
                            spacing="2",
                            margin_bottom="2rem",
                        ),
                        # Product column
                        rx.vstack(
                            rx.heading(
                                "Product",
                                size="4",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("Features", href="#features", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("How it works", href="#how-it-works", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Pricing", href="#pricing", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                            margin_bottom="2rem",
                        ),
                        # Company column
                        rx.vstack(
                            rx.heading(
                                "Company",
                                size="4",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("About Us", href="/about", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Blog", href="/blog", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Contact", href="/contact", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                            margin_bottom="2rem",
                        ),
                        # Legal column
                        rx.vstack(
                            rx.heading(
                                "Legal",
                                size="4",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.link("Privacy Policy", href="/privacy", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Terms of Service", href="/terms", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            rx.link("Cookie Policy", href="/cookies", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                            align="start",
                            spacing="2",
                        ),
                        align="start",
                        width="100%",
                        spacing="3",
                        display=["flex", "flex", "none"],
                    ),
                ),
                # Divider
                rx.box(
                    width="100%",
                    height="1px",
                    background=COLORS.BORDER_SUBTLE,
                    margin_y="2rem",
                ),
                # Bottom section with copyright and social
                rx.hstack(
                    rx.text(
                        f"© {2026} WhisperHedge. All rights reserved.",
                        size="2",
                        color=COLORS.TEXT_MUTED,
                    ),
                    rx.hstack(
                        rx.link(
                            "Twitter",
                            href="#",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                            _hover={"color": COLORS.TEXT_PRIMARY},
                        ),
                        rx.link(
                            "Discord",
                            href="#",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                            _hover={"color": COLORS.TEXT_PRIMARY},
                        ),
                        rx.link(
                            "Telegram",
                            href="#",
                            size="2",
                            color=COLORS.TEXT_SECONDARY,
                            _hover={"color": COLORS.TEXT_PRIMARY},
                        ),
                        spacing="6",
                    ),
                    justify="between",
                    width="100%",
                    align="center",
                ),
                spacing="6",
                padding_y="4rem",
            ),
            size="4",
        ),
        background="rgba(15, 23, 42, 0.3)",
        border_top=f"1px solid {COLORS.BORDER_DEFAULT}",
        width="100%",
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
        risk_automation_section(),
        strategic_philosophy_section(),
        features_section(),
        how_it_works_section(),
        pricing_section(),
        faq_section(),
        footer(),
        width="100%",
        background=COLORS.BACKGROUND_PRIMARY,
    )
