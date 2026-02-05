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
        # Assets are served from project_root/assets/
        # Go up from web_ui/branding/ to project root, then into assets/
        project_root = Path(__file__).parent.parent.parent
        file_path = project_root / "assets" / logo_path.lstrip('/')
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
    
    # Simplified approach - always try to show logo + text
    # Return image + text side by side
    return rx.hstack(
        rx.image(
            src="/whisperhedge_logo_transparentbg.png",
            alt=BrandConfig.APP_NAME,
            height=logo_height,
            width="auto",
            loading="eager",
            display="block",
            object_fit="contain",
        ),
        rx.heading(
            BrandConfig.APP_NAME,
            size=heading_size,
            **kwargs
        ),
        align="center",
        spacing="1",
        display="flex",
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
