"""
Settings page - Account preferences and security settings
"""
import reflex as rx
from ..components.sidebar import sidebar
from ..state import AuthState


class SettingsState(rx.State):
    """State for settings page"""
    
    # Profile section
    display_name: str = ""
    email: str = ""
    
    # Security section
    two_factor_enabled: bool = False
    
    # Preferences section
    currency: str = "USD"
    timezone: str = "UTC"
    theme: str = "dark"
    
    # UI state
    success_message: str = ""
    error_message: str = ""
    
    def on_mount(self):
        """Load user settings on page mount"""
        # TODO: Load from database
        pass
    
    def save_profile(self):
        """Save profile settings"""
        # TODO: Implement profile update
        self.success_message = "Profile updated successfully"
        
    def save_preferences(self):
        """Save user preferences"""
        # TODO: Implement preferences update
        self.success_message = "Preferences updated successfully"


def settings_section(title: str, description: str, content: rx.Component) -> rx.Component:
    """Reusable settings section component"""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(title, size="6", weight="bold"),
                width="100%",
            ),
            rx.text(description, color="gray", size="2"),
            rx.divider(margin_y="1rem"),
            content,
            spacing="3",
            width="100%",
        ),
        padding="1.5rem",
        border_radius="8px",
        border="1px solid var(--gray-6)",
        background="var(--gray-2)",
        width="100%",
    )


def profile_section() -> rx.Component:
    """Profile settings section"""
    return settings_section(
        "Profile",
        "Your account information (passwordless authentication)",
        rx.vstack(
            rx.hstack(
                rx.text("Display Name", size="2", weight="medium", width="150px"),
                rx.input(
                    placeholder="Your name",
                    value=SettingsState.display_name,
                    on_change=SettingsState.set_display_name,
                    width="100%",
                    disabled=True,  # Placeholder
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Email", size="2", weight="medium", width="150px"),
                rx.input(
                    placeholder="your@email.com",
                    value=SettingsState.email,
                    on_change=SettingsState.set_email,
                    width="100%",
                    disabled=True,  # Placeholder
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Save Changes",
                    on_click=SettingsState.save_profile,
                    disabled=True,  # Placeholder
                    size="2",
                ),
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
    )


def security_section() -> rx.Component:
    """Security settings section"""
    return settings_section(
        "Security",
        "Additional security features (coming soon)",
        rx.vstack(
            rx.hstack(
                rx.text("Password", size="2", weight="medium", width="150px"),
                rx.text(
                    "Passwordless authentication via magic links",
                    size="2",
                    color="gray",
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Two-Factor Auth", size="2", weight="medium", width="150px"),
                rx.switch(
                    checked=SettingsState.two_factor_enabled,
                    on_change=SettingsState.set_two_factor_enabled,
                    disabled=True,  # Placeholder
                ),
                rx.text("Coming soon - TOTP authenticator support", color="gray", size="2"),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Sessions", size="2", weight="medium", width="150px"),
                rx.text(
                    "Managed automatically by magic link authentication",
                    size="2",
                    color="gray",
                ),
                width="100%",
                align="center",
            ),
            spacing="4",
            width="100%",
        ),
    )


def preferences_section() -> rx.Component:
    """User preferences section"""
    return settings_section(
        "Preferences",
        "Customize your application experience",
        rx.vstack(
            rx.hstack(
                rx.text("Currency", size="2", weight="medium", width="150px"),
                rx.select(
                    ["USD", "EUR", "GBP", "JPY"],
                    value=SettingsState.currency,
                    on_change=SettingsState.set_currency,
                    disabled=True,  # Placeholder
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Timezone", size="2", weight="medium", width="150px"),
                rx.select(
                    ["UTC", "America/New_York", "America/Los_Angeles", "Europe/London"],
                    value=SettingsState.timezone,
                    on_change=SettingsState.set_timezone,
                    disabled=True,  # Placeholder
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Theme", size="2", weight="medium", width="150px"),
                rx.select(
                    ["dark", "light", "system"],
                    value=SettingsState.theme,
                    on_change=SettingsState.set_theme,
                    disabled=True,  # Placeholder
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text("Email Notifications", size="2", weight="medium", width="150px"),
                rx.switch(disabled=True),  # Placeholder
                rx.text("Receive updates about your positions", color="gray", size="2"),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.spacer(),
                rx.button(
                    "Save Preferences",
                    on_click=SettingsState.save_preferences,
                    disabled=True,  # Placeholder
                    size="2",
                ),
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
    )


def danger_zone_section() -> rx.Component:
    """Danger zone section"""
    return settings_section(
        "Danger Zone",
        "Irreversible and destructive actions",
        rx.vstack(
            rx.hstack(
                rx.text("Delete Account", size="2", weight="medium", width="150px"),
                rx.button(
                    "Delete Account",
                    color_scheme="red",
                    variant="outline",
                    size="2",
                    disabled=True,  # Placeholder
                ),
                rx.text("This action cannot be undone", color="red", size="2"),
                width="100%",
                align="center",
            ),
            spacing="4",
            width="100%",
        ),
    )


@rx.page(route="/settings", on_load=SettingsState.on_mount)
def settings() -> rx.Component:
    """Settings page"""
    return rx.box(
        sidebar(),
        rx.box(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.heading("Settings", size="8", weight="bold"),
                    width="100%",
                    padding_bottom="1rem",
                ),
                
                # Success/Error messages
                rx.cond(
                    SettingsState.success_message != "",
                    rx.callout(
                        SettingsState.success_message,
                        icon="check",
                        color_scheme="green",
                        margin_bottom="1rem",
                    ),
                ),
                rx.cond(
                    SettingsState.error_message != "",
                    rx.callout(
                        SettingsState.error_message,
                        icon="alert-triangle",
                        color_scheme="red",
                        margin_bottom="1rem",
                    ),
                ),
                
                # Settings sections
                profile_section(),
                security_section(),
                preferences_section(),
                danger_zone_section(),
                
                spacing="5",
                width="100%",
                max_width="900px",
            ),
            margin_left="250px",
            padding="2rem",
            width="100%",
        ),
        width="100%",
    )
