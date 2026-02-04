import reflex as rx
from ..branding import COLORS


def mobile_strategic_philosophy_section() -> rx.Component:
    """Mobile-optimized Strategic Philosophy section - simpler, single column"""
    return rx.vstack(
        rx.heading(
            "The WhisperHedge Philosophy",
            size="7",
            weight="bold",
            text_align="center",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Why we abandoned standard delta-neutral strategies for something smarter.",
            size="3",
            color=COLORS.TEXT_SECONDARY,
            text_align="center",
            margin_bottom="2rem",
        ),
        # Card 1: Stop the "Rebalance Bleed"
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'></path></svg>"),
                    margin_bottom="1rem",
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
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "The Delta-Neutral Trap",
                    size="2",
                    weight="bold",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Chasing a static 0-delta in a dynamic pool is a losing game. Most bots force you to rebalance on every tick, turning \"Impermanent\" loss into \"Permanent\" loss through constant slippage and fees.",
                    size="2",
                    color="#94A3B8",
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Card 2: Defend Your Principal
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><line x1='12' y1='3' x2='12' y2='21'></line><path d='M8 9l4-4 4 4'></path><path d='M16 15l-4 4-4-4'></path></svg>"),
                    margin_bottom="1rem",
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
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Real-Time IL Mitigation",
                    size="2",
                    weight="bold",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Impermanent Loss is the \"invisible tax\" on LPs. WhisperHedge identifies price divergence early and opens targeted offsets on perpetual exchanges.",
                    size="2",
                    color="#94A3B8",
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Card 3: Master the Volatility
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='23 6 13.5 15.5 8.5 10.5 1 18'></polyline><polyline points='17 6 23 6 23 12'></polyline></svg>"),
                    margin_bottom="1rem",
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
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Optimized Drawdowns",
                    size="2",
                    weight="bold",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Market crashes shouldn't wipe out months of fee accumulation. By using asymmetric under-hedging, we provide a mathematical safety net.",
                    size="2",
                    color="#94A3B8",
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        spacing="3",
        align="stretch",
        width="100%",
        padding="1rem",
    )


def mobile_features_section() -> rx.Component:
    """Mobile-optimized Core Features section"""
    return rx.vstack(
        rx.heading(
            "Core Features",
            size="7",
            weight="bold",
            text_align="center",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Engineered for Performance. Built for Security.",
            size="3",
            color=COLORS.TEXT_SECONDARY,
            text_align="center",
            margin_bottom="2rem",
        ),
        # Feature 1: Smart Exposure Management
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M3 3v18h18'></path><path d='M18 17V9'></path><path d='M13 17V5'></path><path d='M8 17v-3'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.heading(
                    "Smart Exposure Management",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "We don't chase \"Perfect Zero\" delta. WhisperHedge monitors your pool's active tick-range and maintains a flexible, asymmetric hedge.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Feature 2: Native Hyperliquid Integration
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polygon points='13 2 3 14 12 14 11 22 21 10 12 10 13 2'></polygon></svg>"),
                    margin_bottom="1rem",
                ),
                rx.hstack(
                    rx.heading(
                        "Native Hyperliquid Integration",
                        size="4",
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
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Experience the power of the world's leading decentralized perp exchange. Institutional-grade execution speed and deep liquidity, all on-chain.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Feature 3: Net-Profit Optimization
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.7)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='8' cy='8' r='6'></circle><path d='M18.09 10.37A6 6 0 1 1 10.34 18'></path><path d='M7 6h1v4'></path><path d='m16.71 13.88.7.71-2.82 2.82'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.heading(
                    "Net-Profit Optimization",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "WhisperHedge is funding-aware; it constantly monitors perp funding rates against your LP fee generation to ensure you stay in the green.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Feature 4: Zero-Touch Architecture
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'></path><path d='m9 12 2 2 4-4'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.heading(
                    "Zero-Touch Architecture",
                    size="4",
                    weight="bold",
                    color="#10B981",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "We never connect to your wallet or touch your principal. WhisperHedge manages your defense via restricted, trade-only API keys.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        spacing="3",
        align="stretch",
        width="100%",
        padding="1rem",
    )


def mobile_how_it_works_section() -> rx.Component:
    """Mobile-optimized How It Works section"""
    return rx.vstack(
        rx.heading(
            "How It Works",
            size="7",
            weight="bold",
            text_align="center",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Three steps to institutional-grade LP protection.",
            size="3",
            color=COLORS.TEXT_SECONDARY,
            text_align="center",
            margin_bottom="2rem",
        ),
        # Step 1: Reference Your Position
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M2 12C2 6.5 6.5 2 12 2a10 10 0 0 1 8 4'></path><path d='M5 19.5C5.5 18 6 15 6 12c0-.7.12-1.37.34-2'></path><path d='M17.29 21.02c.12-.6.43-2.3.5-3.02'></path><path d='M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4'></path><path d='M8.65 22c.21-.66.45-1.32.57-2'></path><path d='M14 13.12c0 2.38 0 6.38-1 8.88'></path><path d='M2 16h.01'></path><path d='M21.8 16c.2-2 .131-5.354 0-6'></path><path d='M9 6.8a6 6 0 0 1 9 5.2c0 .47 0 1.17-.02 2'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.badge("Step 1", color_scheme="blue", size="1", margin_bottom="0.5rem"),
                rx.heading(
                    "Reference Your Position",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Input your specific Liquidity Pool Position ID. WhisperHedge doesn't need to scan your entire wallet—we simply pull the real-time on-chain data for that specific position.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Step 2: Link Your Defense
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><circle cx='7.5' cy='15.5' r='5.5'></circle><path d='m21 2-9.6 9.6'></path><path d='m15.5 7.5 3 3L22 7l-3-3'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.badge("Step 2", color_scheme="blue", size="1", margin_bottom="0.5rem"),
                rx.heading(
                    "Link Your Defense",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Generate a restricted, trade-only API key on Hyperliquid. Your funds stay in your account—WhisperHedge simply uses the API to execute defensive offsets.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Step 3: Activate Automation
        rx.box(
            rx.vstack(
                rx.box(
                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='32' height='32' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 12h-4l-3 9L9 3l-3 9H2'></path></svg>"),
                    margin_bottom="1rem",
                ),
                rx.badge("Step 3", color_scheme="blue", size="1", margin_bottom="0.5rem"),
                rx.heading(
                    "Activate Automation",
                    size="4",
                    weight="bold",
                    color=COLORS.TEXT_PRIMARY,
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Choose Manual or Dynamic mode. Once live, the system monitors price ticks and funding rates 24/7, adjusting your hedge to defend your principal while you collect fees.",
                    size="2",
                    color=COLORS.TEXT_SECONDARY,
                    line_height="1.6",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        spacing="3",
        align="stretch",
        width="100%",
        padding="1rem",
    )


def mobile_pricing_section() -> rx.Component:
    """Mobile-optimized Pricing section"""
    return rx.vstack(
        rx.heading(
            "Simple, Transparent Pricing",
            size="7",
            weight="bold",
            text_align="center",
            margin_bottom="0.5rem",
            color=COLORS.TEXT_PRIMARY,
        ),
        rx.text(
            "Professional protection that scales with your liquidity.",
            size="3",
            color=COLORS.TEXT_SECONDARY,
            text_align="center",
            margin_bottom="2rem",
        ),
        # FREE Tier
        rx.box(
            rx.vstack(
                rx.text(
                    "FREE",
                    size="2",
                    weight="bold",
                    color=COLORS.TEXT_SECONDARY,
                    text_transform="uppercase",
                    letter_spacing="0.1em",
                    margin_bottom="0.5rem",
                ),
                rx.hstack(
                    rx.heading("$0", size="7", weight="bold", color=COLORS.TEXT_PRIMARY),
                    rx.text("/mo", size="2", color=COLORS.TEXT_SECONDARY),
                    align="end",
                    spacing="1",
                    margin_bottom="1rem",
                ),
                rx.divider(margin_y="0.5rem"),
                rx.text("1 Position", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                rx.text("$2,500 TVL Hard Cap", size="2", color=COLORS.TEXT_SECONDARY, margin_bottom="0.5rem"),
                rx.vstack(
                    rx.text("✓ Standard Execution", size="2", color=COLORS.TEXT_SECONDARY),
                    rx.text("✓ Hyperliquid Integration", size="2", color=COLORS.TEXT_SECONDARY),
                    rx.text("✓ All Strategies", size="2", color=COLORS.TEXT_SECONDARY),
                    align="start",
                    spacing="1",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # HOBBY Tier
        rx.box(
            rx.vstack(
                rx.text(
                    "HOBBY",
                    size="2",
                    weight="bold",
                    color=COLORS.TEXT_SECONDARY,
                    text_transform="uppercase",
                    letter_spacing="0.1em",
                    margin_bottom="0.5rem",
                ),
                rx.hstack(
                    rx.heading("$19.99", size="7", weight="bold", color=COLORS.TEXT_PRIMARY),
                    rx.text("/mo", size="2", color=COLORS.TEXT_SECONDARY),
                    align="end",
                    spacing="1",
                    margin_bottom="1rem",
                ),
                rx.divider(margin_y="0.5rem"),
                rx.text("3 Positions", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                rx.text("$10,000 Included TVL", size="2", color=COLORS.TEXT_SECONDARY),
                rx.text("0.1% (10 bps) on excess", size="1", color=COLORS.TEXT_MUTED, font_style="italic", margin_bottom="0.5rem"),
                rx.vstack(
                    rx.text("✓ Standard Execution", size="2", color=COLORS.TEXT_SECONDARY),
                    rx.text("✓ Email Alerts", size="2", color=COLORS.TEXT_SECONDARY),
                    align="start",
                    spacing="1",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #1E293B",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # PRO Tier (Most Popular)
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
                    rx.badge("Most Popular", color_scheme="blue", size="1"),
                    spacing="2",
                    margin_bottom="0.5rem",
                ),
                rx.hstack(
                    rx.heading("$49.99", size="7", weight="bold", color=COLORS.TEXT_PRIMARY),
                    rx.text("/mo", size="2", color=COLORS.TEXT_SECONDARY),
                    align="end",
                    spacing="1",
                    margin_bottom="1rem",
                ),
                rx.divider(margin_y="0.5rem"),
                rx.text("10 Positions", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                rx.text("$50,000 Included TVL", size="2", color=COLORS.TEXT_SECONDARY),
                rx.text("0.05% (5 bps) on excess", size="1", color=COLORS.TEXT_MUTED, font_style="italic", margin_bottom="0.5rem"),
                rx.vstack(
                    rx.text("✓ Priority Execution", size="2", color=COLORS.ACCENT_PRIMARY, weight="bold"),
                    rx.text("✓ Multi-DEX Roadmap Access", size="2", color=COLORS.TEXT_SECONDARY),
                    align="start",
                    spacing="1",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"2px solid {COLORS.ACCENT_PRIMARY}",
            background="rgba(15, 23, 42, 0.4)",
            box_shadow="0 0 15px rgba(59, 130, 246, 0.3)",
            width="100%",
        ),
        # ELITE Tier
        rx.box(
            rx.vstack(
                rx.text(
                    "ELITE",
                    size="2",
                    weight="bold",
                    color="#D4AF37",
                    text_transform="uppercase",
                    letter_spacing="0.1em",
                    margin_bottom="0.5rem",
                ),
                rx.hstack(
                    rx.heading("$149.99", size="7", weight="bold", color=COLORS.TEXT_PRIMARY),
                    rx.text("/mo", size="2", color=COLORS.TEXT_SECONDARY),
                    align="end",
                    spacing="1",
                    margin_bottom="1rem",
                ),
                rx.divider(margin_y="0.5rem"),
                rx.text("Unlimited Positions", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                rx.text("$250,000 Included TVL", size="2", color=COLORS.TEXT_SECONDARY),
                rx.text("0.05% (5 bps) on excess", size="1", color=COLORS.TEXT_MUTED, font_style="italic", margin_bottom="0.5rem"),
                rx.vstack(
                    rx.text("✓ Elite Priority Engine", size="2", color="#D4AF37", weight="bold"),
                    rx.text("   (Top-of-queue rebalancing)", size="1", color="#B8960F", font_style="italic"),
                    rx.text("✓ Direct Dev Support", size="2", color=COLORS.TEXT_SECONDARY),
                    align="start",
                    spacing="1",
                ),
                align="start",
                spacing="2",
            ),
            padding="1.5rem",
            border_radius="8px",
            border=f"1px solid #D4AF37",
            background="rgba(15, 23, 42, 0.4)",
            width="100%",
        ),
        # Disclaimer
        rx.box(
            rx.text(
                "Overage charges are calculated based on your average monthly managed TVL. Priority Calculation ensures your positions are rebalanced first during high-volatility events.",
                size="1",
                color=COLORS.TEXT_MUTED,
                text_align="center",
                line_height="1.5",
            ),
            padding="1rem",
            border_radius="8px",
            background="rgba(15, 23, 42, 0.3)",
            border=f"1px solid #1E293B",
            margin_top="1rem",
            width="100%",
        ),
        spacing="3",
        align="stretch",
        width="100%",
        padding="1rem",
    )
