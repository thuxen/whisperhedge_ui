import os
from dotenv import load_dotenv

load_dotenv()

def get_current_host():
    """Get current host from environment variables"""
    # Check REFLEX_DOMAIN first (used on VPS), then fallback to HOST or VERCEL_URL
    return os.getenv('REFLEX_DOMAIN', os.getenv('HOST', os.getenv('VERCEL_URL', '')))

def is_whisperhedge_domain():
    """Check if current domain is whisperhedge.com"""
    host = get_current_host()
    return 'whisperhedge.com' in host

class BrandConfig:
    """
    Centralized branding configuration.
    Domain-based branding with fallback to whitelabel.
    """
    
    # Company Information - dynamically set based on domain
    APP_NAME = "WhisperHedge" if is_whisperhedge_domain() else "White Label"
    COMPANY_NAME = "WhisperHedge" if is_whisperhedge_domain() else "White Label"
    DOMAIN = "whisperhedge.com" if is_whisperhedge_domain() else ""
    TAGLINE = "Liquidity Pool Hedging Simplified" if is_whisperhedge_domain() else "Automated Hedging Platform"
    
    # Logo Paths (optional - will fallback to text if files don't exist)
    LOGO_LIGHT = os.getenv("BRAND_LOGO_LIGHT", "/whisperhedge_logo_transparentbg.png")
    LOGO_DARK = os.getenv("BRAND_LOGO_DARK", "/whisperhedge_logo_transparentbg.png")
    LOGO_LIGHT_SVG = os.getenv("BRAND_LOGO_LIGHT_SVG", "/whisperhedge_logo_transparentbg.svg")
    LOGO_DARK_SVG = os.getenv("BRAND_LOGO_DARK_SVG", "/whisperhedge_logo_transparentbg.svg")
    FAVICON = os.getenv("BRAND_FAVICON", "/favicon.ico")
    
    # Logo Display Settings
    LOGO_HEIGHT_NAVBAR = os.getenv("BRAND_LOGO_HEIGHT_NAVBAR", "32px")
    LOGO_HEIGHT_LANDING = os.getenv("BRAND_LOGO_HEIGHT_LANDING", "48px")
    LOGO_HEIGHT_SIDEBAR = os.getenv("BRAND_LOGO_HEIGHT_SIDEBAR", "28px")
    
    # Contact & Support - dynamically set based on domain
    SUPPORT_EMAIL = "support@whisperhedge.com" if is_whisperhedge_domain() else "support@example.com"
    DOCS_URL = "https://docs.whisperhedge.com" if is_whisperhedge_domain() else ""
    
    # Theme Colors (optional overrides)
    PRIMARY_COLOR = os.getenv("BRAND_PRIMARY_COLOR", "")
    SECONDARY_COLOR = os.getenv("BRAND_SECONDARY_COLOR", "")
    
    @classmethod
    def get_logo_path(cls, prefer_svg: bool = True, dark_mode: bool = False) -> str:
        """
        Get the appropriate logo path based on preferences.
        Returns empty string if no logo should be used (fallback to text).
        """
        if dark_mode:
            if prefer_svg:
                return cls.LOGO_DARK_SVG
            return cls.LOGO_DARK
        else:
            if prefer_svg:
                return cls.LOGO_LIGHT_SVG
            return cls.LOGO_LIGHT
