import reflex as rx
from pathlib import Path
from .config import BrandConfig

def _logo_exists(logo_path: str) -> bool:
    """
    Check if logo file exists at runtime.
    Safe fallback - returns False on any error.
    """
    try:
        if not logo_path:
            return False
        
        # Convert web path to filesystem path
        # Remove leading slash and prepend assets directory
        file_path = Path(__file__).parent / logo_path.lstrip('/')
        return file_path.exists()
    except Exception:
        # On any error, return False to use text fallback
        return False


def brand_logo(
    size: str = "navbar",
    prefer_svg: bool = True,
    **kwargs
) -> rx.Component:
    """
    Renders brand logo with automatic fallback to text.
    
    Args:
        size: One of "navbar", "landing", "sidebar" - determines logo height
        prefer_svg: If True, tries SVG first, then PNG
        **kwargs: Additional props passed to the container
    
    Returns:
        Logo image if available, otherwise text heading
    """
    # Determine logo height based on size
    height_map = {
        "navbar": BrandConfig.LOGO_HEIGHT_NAVBAR,
        "landing": BrandConfig.LOGO_HEIGHT_LANDING,
        "sidebar": BrandConfig.LOGO_HEIGHT_SIDEBAR,
    }
    logo_height = height_map.get(size, BrandConfig.LOGO_HEIGHT_NAVBAR)
    
    # Determine heading size based on context
    heading_size_map = {
        "navbar": "6",
        "landing": "9",
        "sidebar": "5",
    }
    heading_size = heading_size_map.get(size, "6")
    
    # Try to get logo path (will check both light/dark based on theme)
    # For now, we'll use a simple approach - check light logo
    logo_light = BrandConfig.get_logo_path(prefer_svg=prefer_svg, dark_mode=False)
    logo_dark = BrandConfig.get_logo_path(prefer_svg=prefer_svg, dark_mode=True)
    
    # Check if at least one logo exists
    has_logo = _logo_exists(logo_light) or _logo_exists(logo_dark)
    
    if has_logo:
        # Return image with theme-aware src
        return rx.box(
            rx.image(
                src=rx.cond(
                    rx.color_mode_cond(light="light", dark="dark") == "dark",
                    logo_dark if _logo_exists(logo_dark) else logo_light,
                    logo_light,
                ),
                alt=BrandConfig.APP_NAME,
                height=logo_height,
                width="auto",
                loading="eager",
                **kwargs
            )
        )
    else:
        # Fallback to text
        return rx.heading(
            BrandConfig.APP_NAME,
            size=heading_size,
            **kwargs
        )


def brand_name(as_component: bool = False) -> rx.Component | str:
    """
    Returns the brand name.
    
    Args:
        as_component: If True, returns as rx.text component, else as string
    
    Returns:
        Brand name as component or string
    """
    if as_component:
        return rx.text(BrandConfig.APP_NAME)
    return BrandConfig.APP_NAME


def brand_favicon() -> str:
    """
    Returns the favicon path.
    Safe fallback to empty string if not available.
    """
    favicon_path = BrandConfig.FAVICON
    if _logo_exists(favicon_path):
        return favicon_path
    return ""
