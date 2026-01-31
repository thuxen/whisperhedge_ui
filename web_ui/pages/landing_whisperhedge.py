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
        background=COLORS.NAVBAR_BG,
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
        ),
        background=COLORS.BACKGROUND_PRIMARY,
    )


def problem_section() -> rx.Component:
    """The Hidden Cost of Liquidity: Impermanent Loss"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "The Hidden Cost of Liquidity: Impermanent Loss.",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The Problem",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_WARNING,
                            ),
                            rx.text(
                                "Being a Liquidity Provider is a race against price divergence. When the market moves, your pool's asset ratio shifts—forcing you to sell the winners and buy the losers. This 'Impermanent Loss' often exceeds the fees you collect, leaving you with less value than if you had simply held your tokens.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The WhisperHedge Fix",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_SUCCESS,
                            ),
                            rx.text(
                                "We don't just 'watch' your position; we defend its value. By opening automated, strategic offsets, we neutralize the downside of price divergence, ensuring your fee earnings stay in your pocket rather than covering your losses.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="50rem",
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
                padding_bottom="2rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
    )


def risk_protection_section() -> rx.Component:
    """Risk Protection - Smaller Drawdowns with Upside Exposure"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.box(
                    width="100%",
                    height="1px",
                    background=COLORS.BORDER_SUBTLE,
                    margin_y="2rem",
                ),
                rx.heading(
                    "Smaller Drawdowns. Steady Fees. Upside Intact.",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The Safety Buffer",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_PRIMARY,
                            ),
                            rx.text(
                                "Crypto markets are volatile. WhisperHedge creates a safety buffer by reducing your exposure to wild price swings while you continue collecting LP fees. You're protected from the worst drawdowns without sacrificing your position entirely.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Keep Your Upside",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_SUCCESS,
                            ),
                            rx.text(
                                "Unlike full delta-neutral strategies that cap your gains, our strategic under-hedging lets you participate in market upside. You maintain exposure to positive price action while having a defensive layer against crashes—earning fees with confidence.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="50rem",
                ),
                spacing="5",
                align="center",
                padding_y="4rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
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
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
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
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
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
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
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
                        background=COLORS.CARD_BG,
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
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
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
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
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
                    border=f"1px solid {COLORS.CARD_BORDER}",
                    background=COLORS.CARD_BG,
                    width="100%",
                ),
                spacing="5",
                padding_y="6rem",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
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
                    border=f"1px solid {COLORS.CARD_BORDER}",
                    background=COLORS.CARD_BG,
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


def strategic_underhedging_section() -> rx.Component:
    """Why Delta-Neutral is a Mathematical Trap"""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.box(
                    width="100%",
                    height="1px",
                    background=COLORS.BORDER_SUBTLE,
                    margin_y="2rem",
                ),
                rx.heading(
                    "Why \"Delta-Neutral\" is a Mathematical Trap.",
                    size="8",
                    weight="bold",
                    text_align="center",
                    margin_bottom="3rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The Problem with 100% Hedging",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_WARNING,
                            ),
                            rx.text(
                                "Most bots chase 'Perfect Zero' delta, but LP positions are dynamic. Maintaining 100% neutrality forces constant rebalancing—locking in IL and bleeding fees with every tick. You end up hedging away your entire profit.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid {COLORS.CARD_BORDER}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "The WhisperHedge Approach",
                                size="5",
                                weight="bold",
                                margin_bottom="1rem",
                                color=COLORS.ACCENT_SUCCESS,
                            ),
                            rx.text(
                                "We utilize Strategic Under-Hedging. Our algorithms understand that a pool is a moving target. We provide enough protection to survive the crashes without the hyper-active rebalancing that bleeds your account dry. We optimize for Net Profit, not theoretical neutrality.",
                                size="4",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.7",
                            ),
                            align="start",
                        ),
                        padding="2.5rem",
                        border_radius="8px",
                        border=f"2px solid {COLORS.ACCENT_PRIMARY}",
                        background=COLORS.CARD_BG,
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                    max_width="50rem",
                ),
                spacing="5",
                align="center",
                padding_top="4rem",
                padding_bottom="0",
            ),
            size="4",
        ),
        background=COLORS.BACKGROUND_SURFACE,
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
        background=COLORS.BACKGROUND_SURFACE,
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
        problem_section(),
        strategic_underhedging_section(),
        risk_protection_section(),
        features_section(),
        how_it_works_section(),
        pricing_section(),
        comparison_table_section(),
        footer(),
        width="100%",
    )
