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
                    "How it works",
                    href="#how-it-works",
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
    """The WhisperHedge Strategic Philosophy"""
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
                        "0px": {"columns": "1"},
                        "768px": {"columns": "3"},
                    },
                ),
                spacing="5",
                align="center",
                padding_y="6rem",
            ),
            size="4",
        ),
        background="transparent",
    )


def features_section() -> rx.Component:
    """Features section - What the bot does"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "What WhisperHedge Does",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    id="features",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.vstack(
                    # Feature 1
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "🤖 Automated Position Monitoring",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Our bot continuously tracks your LP positions across Uniswap V3, Aerodrome, and PancakeSwap. It calculates your real-time exposure and delta as prices move, ensuring you're always protected.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.BORDER_SUBTLE}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        width="100%",
                    ),
                    # Feature 2
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "⚡ Fully Decentralized Hedging",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "WhisperHedge automatically opens and adjusts offsetting positions on Hyperliquid, a decentralized perpetual exchange. Your LP positions on DEXs like Uniswap V3 and your hedges are completely decentralized—no KYC, no centralized custody. We use strategic under-hedging to protect against crashes while minimizing funding costs.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.BORDER_SUBTLE}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        width="100%",
                    ),
                    # Feature 3
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "📊 Funding-Aware Optimization",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "The bot monitors perpetual funding rates in real-time. It won't open a hedge that costs more than your LP is earning, ensuring your net profit stays positive. Smart rebalancing only when necessary.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.BORDER_SUBTLE}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        width="100%",
                    ),
                    # Feature 4
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "🔐 Non-Custodial & Secure",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_SUCCESS,
                            ),
                            rx.text(
                                "We never touch your funds. WhisperHedge executes trades via restricted API keys on your preferred perpetual exchange with withdrawal permissions disabled. Your principal stays in your control at all times.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"2px solid {COLORS.ACCENT_SUCCESS}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="50rem",
                ),
                rx.link(
                    rx.button(
                        "Start Protecting My Yield",
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
        background=COLORS.BACKGROUND_PRIMARY,
    )


def how_it_works_section() -> rx.Component:
    """How It Works - Simplified 2-step workflow"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "How It Works",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    id="how-it-works",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.hstack(
                    # Step 1
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.text("1", size="8", weight="bold", color=COLORS.ACCENT_PRIMARY),
                                width="4rem",
                                height="4rem",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                border_radius="50%",
                                background=COLORS.BACKGROUND_ELEVATED,
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Strategic Calibration",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Our system calculates your real-time exposure and the 'cost-to-protect.'",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                text_align="center",
                                line_height="1.6",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="2.5rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.BORDER_SUBTLE}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        flex="1",
                    ),
                    # Step 2
                    rx.box(
                        rx.vstack(
                            rx.box(
                                rx.text("2", size="8", weight="bold", color=COLORS.ACCENT_PRIMARY),
                                width="4rem",
                                height="4rem",
                                display="flex",
                                align_items="center",
                                justify_content="center",
                                border_radius="50%",
                                background=COLORS.BACKGROUND_ELEVATED,
                                margin_bottom="1.5rem",
                            ),
                            rx.heading(
                                "Automated Defense",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "The bot manages a flexible hedge on a perpetual exchange that adapts as your pool moves, focusing on capital preservation over rigid symmetry.",
                                size="3",
                                color=COLORS.TEXT_SECONDARY,
                                text_align="center",
                                line_height="1.6",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="2.5rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.BORDER_SUBTLE}",
                        background="rgba(15, 23, 42, 0.5)",
                        backdrop_filter="blur(12px)",
                        flex="1",
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
    """Pricing tiers comparison table"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Pricing",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    id="pricing",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Feature", color=COLORS.TEXT_PRIMARY),
                                rx.table.column_header_cell("Starter", color=COLORS.TEXT_PRIMARY),
                                rx.table.column_header_cell("Pro", color=COLORS.TEXT_PRIMARY),
                                rx.table.column_header_cell("Elite", color=COLORS.TEXT_PRIMARY),
                            ),
                        ),
                        rx.table.body(
                            rx.table.row(
                                rx.table.cell("Monthly Fee", color=COLORS.TEXT_SECONDARY, weight="bold"),
                                rx.table.cell("$0 (Free)", color=COLORS.ACCENT_SUCCESS),
                                rx.table.cell("$49", color=COLORS.TEXT_PRIMARY),
                                rx.table.cell("$199", color=COLORS.TEXT_PRIMARY),
                            ),
                            rx.table.row(
                                rx.table.cell("Managed TVL", color=COLORS.TEXT_SECONDARY, weight="bold"),
                                rx.table.cell("Up to $2,500", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("Up to $50,000", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("Unlimited", color=COLORS.ACCENT_SUCCESS),
                            ),
                            rx.table.row(
                                rx.table.cell("Hedge Logic", color=COLORS.TEXT_SECONDARY, weight="bold"),
                                rx.table.cell("Standard Delta", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("Strategic Under-Hedge", color=COLORS.ACCENT_PRIMARY),
                                rx.table.cell("Strategic Under-Hedge", color=COLORS.ACCENT_PRIMARY),
                            ),
                            rx.table.row(
                                rx.table.cell("Update Frequency", color=COLORS.TEXT_SECONDARY, weight="bold"),
                                rx.table.cell("5 Minutes", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("30 Seconds", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("Real-time (Sub-sec)", color=COLORS.ACCENT_SUCCESS),
                            ),
                            rx.table.row(
                                rx.table.cell("Overage Charge", color=COLORS.TEXT_SECONDARY, weight="bold"),
                                rx.table.cell("N/A (Hard Cap)", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("0.05% on vol > $50k", color=COLORS.TEXT_SECONDARY),
                                rx.table.cell("Included", color=COLORS.ACCENT_SUCCESS),
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
                rx.text(
                    "Pro tier overage: 0.05% fee applies only to managed volume exceeding $50,000.",
                    size="2",
                    color=COLORS.TEXT_MUTED,
                    text_align="center",
                    margin_top="1rem",
                ),
                rx.link(
                    rx.button(
                        "Start Protecting My Yield",
                        size="4",
                        background=COLORS.BUTTON_PRIMARY_BG,
                        color=COLORS.BUTTON_PRIMARY_TEXT,
                        _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                    ),
                    href="/signup",
                ),
                spacing="5",
                padding_y="6rem",
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
                        rx.link("Documentation", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
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
                        rx.link("About Us", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        rx.link("Blog", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        rx.link("Careers", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        rx.link("Contact", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
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
                        rx.link("Privacy Policy", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        rx.link("Terms of Service", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        rx.link("Cookie Policy", href="#", size="2", color=COLORS.TEXT_SECONDARY, _hover={"color": COLORS.TEXT_PRIMARY}),
                        align="start",
                        spacing="2",
                    ),
                    justify="between",
                    width="100%",
                    spacing="8",
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
                            "GitHub",
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
        comparison_table_section(),
        footer(),
        width="100%",
        background=COLORS.BACKGROUND_PRIMARY,
    )
