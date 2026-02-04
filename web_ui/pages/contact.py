import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


class ContactState(rx.State):
    """State for contact form"""
    name: str = ""
    email: str = ""
    subject: str = ""
    message: str = ""
    submitted: bool = False
    
    def set_name(self, value: str):
        """Set name field"""
        self.name = value
    
    def set_email(self, value: str):
        """Set email field"""
        self.email = value
    
    def set_subject(self, value: str):
        """Set subject field"""
        self.subject = value
    
    def set_message(self, value: str):
        """Set message field"""
        self.message = value
    
    def submit_form(self):
        """Handle form submission"""
        # In production, this would send an email or save to database
        self.submitted = True
        
    def reset_form(self):
        """Reset form after submission"""
        self.name = ""
        self.email = ""
        self.subject = ""
        self.message = ""
        self.submitted = False


def contact_page() -> rx.Component:
    """Contact Us page"""
    return rx.vstack(
        navbar(),
        rx.box(
            rx.box(
                rx.vstack(
                # Header
                rx.heading(
                    "Contact Us",
                    size="9",
                    weight="bold",
                    margin_bottom="1rem",
                    color=COLORS.TEXT_PRIMARY,
                ),
                rx.text(
                    "Have questions? We'd love to hear from you.",
                    size="4",
                    color=COLORS.TEXT_SECONDARY,
                    margin_bottom="3rem",
                ),
                
                # Two column layout
                rx.grid(
                    # Left: Contact Info
                    rx.vstack(
                        rx.heading(
                            "Get in Touch",
                            size="6",
                            weight="bold",
                            margin_bottom="1rem",
                            color=COLORS.TEXT_PRIMARY,
                        ),
                        rx.text(
                            "Whether you have a question about features, pricing, need a demo, or anything else, our team is ready to answer all your questions.",
                            size="3",
                            color=COLORS.TEXT_SECONDARY,
                            line_height="1.8",
                            margin_bottom="2rem",
                        ),
                        
                        # Contact methods
                        rx.vstack(
                            # Email
                            rx.hstack(
                                rx.box(
                                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect width='20' height='16' x='2' y='4' rx='2'></rect><path d='m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7'></path></svg>"),
                                ),
                                rx.vstack(
                                    rx.text("Email", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.text("support@whisperhedge.com", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align="start",
                            ),
                            
                            # Discord
                            rx.hstack(
                                rx.box(
                                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'></path></svg>"),
                                ),
                                rx.vstack(
                                    rx.text("Discord", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.text("Join our community", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align="start",
                            ),
                            
                            # Telegram
                            rx.hstack(
                                rx.box(
                                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='m22 2-7 20-4-9-9-4Z'></path><path d='M22 2 11 13'></path></svg>"),
                                ),
                                rx.vstack(
                                    rx.text("Telegram", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.text("@whisperhedge", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align="start",
                            ),
                            
                            align="start",
                            spacing="4",
                        ),
                        
                        # Enterprise contact
                        rx.box(
                            rx.heading(
                                "Enterprise Solutions",
                                size="5",
                                weight="bold",
                                margin_bottom="0.5rem",
                                color=COLORS.TEXT_PRIMARY,
                            ),
                            rx.text(
                                "Managing $5M+ in TVL? Contact our team for custom solutions and dedicated support.",
                                size="2",
                                color=COLORS.TEXT_SECONDARY,
                                line_height="1.6",
                                margin_bottom="1rem",
                            ),
                            rx.text(
                                "enterprise@whisperhedge.com",
                                size="2",
                                color=COLORS.ACCENT_PRIMARY,
                                weight="bold",
                            ),
                            padding="1.5rem",
                            border_radius="8px",
                            border=f"1px solid {COLORS.ACCENT_PRIMARY}",
                            background="rgba(59, 130, 246, 0.05)",
                            margin_top="2rem",
                        ),
                        
                        align="start",
                        spacing="3",
                    ),
                    
                    # Right: Contact Form
                    rx.box(
                        rx.cond(
                            ContactState.submitted,
                            # Success message
                            rx.vstack(
                                rx.box(
                                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 24 24' fill='none' stroke='rgba(16, 185, 129, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M22 11.08V12a10 10 0 1 1-5.93-9.14'></path><polyline points='22 4 12 14.01 9 11.01'></polyline></svg>"),
                                    margin_bottom="1rem",
                                ),
                                rx.heading(
                                    "Message Sent!",
                                    size="6",
                                    weight="bold",
                                    margin_bottom="0.5rem",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "Thank you for contacting us. We'll get back to you within 24 hours.",
                                    size="3",
                                    color=COLORS.TEXT_SECONDARY,
                                    text_align="center",
                                    margin_bottom="2rem",
                                ),
                                rx.button(
                                    "Send Another Message",
                                    on_click=ContactState.reset_form,
                                    variant="outline",
                                    size="3",
                                ),
                                align="center",
                                spacing="3",
                                padding="3rem",
                            ),
                            # Contact form
                            rx.vstack(
                                rx.heading(
                                    "Send us a Message",
                                    size="6",
                                    weight="bold",
                                    margin_bottom="1rem",
                                    color=COLORS.TEXT_PRIMARY,
                                ),
                                
                                # Name field
                                rx.vstack(
                                    rx.text("Name", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.input(
                                        placeholder="Your name",
                                        value=ContactState.name,
                                        on_change=ContactState.set_name,
                                        size="3",
                                        width="100%",
                                    ),
                                    align="start",
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Email field
                                rx.vstack(
                                    rx.text("Email", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.input(
                                        placeholder="your@email.com",
                                        type="email",
                                        value=ContactState.email,
                                        on_change=ContactState.set_email,
                                        size="3",
                                        width="100%",
                                    ),
                                    align="start",
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Subject field
                                rx.vstack(
                                    rx.text("Subject", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.input(
                                        placeholder="How can we help?",
                                        value=ContactState.subject,
                                        on_change=ContactState.set_subject,
                                        size="3",
                                        width="100%",
                                    ),
                                    align="start",
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Message field
                                rx.vstack(
                                    rx.text("Message", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.text_area(
                                        placeholder="Tell us more about your inquiry...",
                                        value=ContactState.message,
                                        on_change=ContactState.set_message,
                                        rows="6",
                                        width="100%",
                                    ),
                                    align="start",
                                    spacing="1",
                                    width="100%",
                                ),
                                
                                # Submit button
                                rx.button(
                                    "Send Message",
                                    on_click=ContactState.submit_form,
                                    size="3",
                                    background=COLORS.BUTTON_PRIMARY_BG,
                                    color=COLORS.BUTTON_PRIMARY_TEXT,
                                    _hover={"background": COLORS.BUTTON_PRIMARY_HOVER},
                                    width="100%",
                                ),
                                
                                align="start",
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        padding="2rem",
                        border_radius="8px",
                        border=f"1px solid #1E293B",
                        background="rgba(15, 23, 42, 0.4)",
                    ),
                    
                    columns="2",
                    spacing="6",
                    width="100%",
                    responsive={
                        "0px": {"columns": "1"},
                        "768px": {"columns": "2"},
                    },
                ),
                
                    spacing="4",
                    align="start",
                    padding_y="4rem",
                ),
                max_width="60rem",
                margin_x="auto",
                padding_x="2rem",
            ),
            background=COLORS.BACKGROUND_PRIMARY,
            min_height="100vh",
            width="100%",
        ),
        footer(),
        spacing="0",
        width="100%",
    )
