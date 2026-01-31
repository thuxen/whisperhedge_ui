"""
Centralized color scheme configuration for WhisperHedge.

Deep Liquidity Theme - High-end trading terminal aesthetic.
Change colors here to update the entire application.
"""


class ColorScheme:
    """
    Deep Liquidity color scheme - Trust & Precision
    Inspired by high-end trading terminals (Bloomberg, BlackRock)
    """
    
    # Backgrounds
    BACKGROUND_PRIMARY = "#020617"      # Deepest Navy/Black - Main background
    BACKGROUND_SURFACE = "#0F172A"      # Rich Navy - Cards, navbar, surfaces
    BACKGROUND_ELEVATED = "#1E293B"     # Lighter navy - Hover states, borders
    
    # Accent Colors
    ACCENT_PRIMARY = "#3B82F6"          # Electric Blue - Primary actions, CTAs
    ACCENT_PRIMARY_HOVER = "#60A5FA"    # Lighter blue - Hover state
    ACCENT_SUCCESS = "#10B981"          # Emerald - Profit, hedge success
    ACCENT_WARNING = "#F43F5E"          # Rose - Risk, impermanent loss
    
    # Text Colors
    TEXT_PRIMARY = "#F8FAFC"            # Off-white - Headings, important text
    TEXT_SECONDARY = "#94A3B8"          # Slate Blue - Body text, muted content
    TEXT_MUTED = "#64748B"              # Darker slate - Disabled, placeholder
    
    # Border Colors
    BORDER_DEFAULT = "#1E293B"          # Default borders
    BORDER_SUBTLE = "#334155"           # Subtle borders, dividers
    
    # Component-specific colors
    NAVBAR_BG = BACKGROUND_SURFACE
    NAVBAR_BORDER = BORDER_DEFAULT
    NAVBAR_LINK = TEXT_SECONDARY
    NAVBAR_LINK_HOVER = TEXT_PRIMARY
    
    CARD_BG = BACKGROUND_SURFACE
    CARD_BORDER = BORDER_DEFAULT
    
    BUTTON_PRIMARY_BG = ACCENT_PRIMARY
    BUTTON_PRIMARY_HOVER = ACCENT_PRIMARY_HOVER
    BUTTON_PRIMARY_TEXT = TEXT_PRIMARY
    
    INPUT_BG = BACKGROUND_SURFACE
    INPUT_BORDER = BORDER_DEFAULT
    INPUT_TEXT = TEXT_PRIMARY
    INPUT_PLACEHOLDER = TEXT_MUTED


# Convenience exports
COLORS = ColorScheme()
