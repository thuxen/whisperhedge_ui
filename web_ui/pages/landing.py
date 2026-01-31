import reflex as rx
from ..branding.config import is_whisperhedge_domain


def landing_page() -> rx.Component:
    """
    Dynamic landing page that renders based on domain.
    - whisperhedge.com: Custom WhisperHedge landing
    - Other domains: Simple whitelabel landing
    
    Note: We import the landing functions inside this function to avoid
    circular import issues and ensure proper component rendering.
    """
    from .landing_whisperhedge import whisperhedge_landing
    from .landing_whitelabel import whitelabel_landing
    
    # Check domain at compile time and return the appropriate component
    if is_whisperhedge_domain():
        return whisperhedge_landing()
    else:
        return whitelabel_landing()
