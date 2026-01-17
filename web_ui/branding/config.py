import os
from dotenv import load_dotenv

load_dotenv()

class BrandConfig:
    """
    Centralized branding configuration.
    All values can be overridden via environment variables.
    Safe defaults ensure the app always works.
    """
    
    # Company Information
    APP_NAME = os.getenv("BRAND_APP_NAME", "WhisperHedge")
    COMPANY_NAME = os.getenv("BRAND_COMPANY_NAME", "WhisperHedge")
    DOMAIN = os.getenv("BRAND_DOMAIN", "whisperhedge.com")
    TAGLINE = os.getenv("BRAND_TAGLINE", "Liquidity Pool Hedging Simplified")
    
    # Logo Paths (optional - will fallback to text if files don't exist)
    LOGO_LIGHT = os.getenv("BRAND_LOGO_LIGHT", "/branding/assets/logo.png")
    LOGO_DARK = os.getenv("BRAND_LOGO_DARK", "/branding/assets/logo-dark.png")
    LOGO_LIGHT_SVG = os.getenv("BRAND_LOGO_LIGHT_SVG", "/branding/assets/logo.svg")
    LOGO_DARK_SVG = os.getenv("BRAND_LOGO_DARK_SVG", "/branding/assets/logo-dark.svg")
    FAVICON = os.getenv("BRAND_FAVICON", "/branding/assets/favicon.ico")
    
    # Logo Display Settings
    LOGO_HEIGHT_NAVBAR = os.getenv("BRAND_LOGO_HEIGHT_NAVBAR", "32px")
    LOGO_HEIGHT_LANDING = os.getenv("BRAND_LOGO_HEIGHT_LANDING", "48px")
    LOGO_HEIGHT_SIDEBAR = os.getenv("BRAND_LOGO_HEIGHT_SIDEBAR", "28px")
    
    # Contact & Support
    SUPPORT_EMAIL = os.getenv("BRAND_SUPPORT_EMAIL", "support@whisperhedge.com")
    DOCS_URL = os.getenv("BRAND_DOCS_URL", "https://docs.whisperhedge.com")
    
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
