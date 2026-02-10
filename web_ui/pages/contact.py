import reflex as rx
from ..branding import COLORS
from .landing_whisperhedge import navbar, footer


class ContactState(rx.State):
    """State for contact form"""
    show_success: bool = False
    
    @rx.var
    def check_url_success(self) -> bool:
        """Check if success parameter is in URL"""
        # Check query parameters for success=true
        return self.router.page.params.get("success", "") == "true"


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
                            # Office Address
                            rx.hstack(
                                rx.box(
                                    rx.html("<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='rgba(59, 130, 246, 0.8)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z'></path><circle cx='12' cy='10' r='3'></circle></svg>"),
                                ),
                                rx.vstack(
                                    rx.text("Office", size="2", weight="bold", color=COLORS.TEXT_PRIMARY),
                                    rx.text("Office A/15F, 65-67 Bonham Strand East", size="2", color=COLORS.TEXT_SECONDARY),
                                    rx.text("Sheung Wan, Hong Kong", size="2", color=COLORS.TEXT_SECONDARY),
                                    align="start",
                                    spacing="1",
                                ),
                                spacing="3",
                                align="start",
                            ),
                            
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
                            ContactState.check_url_success,
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
                                rx.link(
                                    rx.button(
                                        "Send Another Message",
                                        variant="outline",
                                        size="3",
                                    ),
                                    href="/contact",
                                ),
                                align="center",
                                spacing="3",
                                padding="3rem",
                            ),
                            # Contact form with Formspree
                            rx.html(
                                """
                                <form action="https://formspree.io/f/mjgebrez" method="POST" style="width: 100%;">
                                    <div style="margin-bottom: 1.5rem;">
                                        <h3 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; color: #F1F5F9;">Send us a Message</h3>
                                    </div>
                                    
                                    <div style="margin-bottom: 1rem;">
                                        <label style="display: block; font-size: 0.875rem; font-weight: bold; color: #F1F5F9; margin-bottom: 0.5rem;">Name</label>
                                        <input type="text" name="name" placeholder="Your name" required 
                                               style="width: 100%; padding: 0.75rem; border-radius: 6px; border: 1px solid #334155; background: rgba(15, 23, 42, 0.6); color: #F1F5F9; font-size: 1rem;">
                                    </div>
                                    
                                    <div style="margin-bottom: 1rem;">
                                        <label style="display: block; font-size: 0.875rem; font-weight: bold; color: #F1F5F9; margin-bottom: 0.5rem;">Email</label>
                                        <input type="email" name="email" placeholder="your@email.com" required 
                                               style="width: 100%; padding: 0.75rem; border-radius: 6px; border: 1px solid #334155; background: rgba(15, 23, 42, 0.6); color: #F1F5F9; font-size: 1rem;">
                                    </div>
                                    
                                    <div style="margin-bottom: 1rem;">
                                        <label style="display: block; font-size: 0.875rem; font-weight: bold; color: #F1F5F9; margin-bottom: 0.5rem;">Subject</label>
                                        <input type="text" name="subject" placeholder="How can we help?" required 
                                               style="width: 100%; padding: 0.75rem; border-radius: 6px; border: 1px solid #334155; background: rgba(15, 23, 42, 0.6); color: #F1F5F9; font-size: 1rem;">
                                    </div>
                                    
                                    <div style="margin-bottom: 1rem;">
                                        <label style="display: block; font-size: 0.875rem; font-weight: bold; color: #F1F5F9; margin-bottom: 0.5rem;">Message</label>
                                        <textarea name="message" placeholder="Tell us more about your inquiry..." required rows="6"
                                                  style="width: 100%; padding: 0.75rem; border-radius: 6px; border: 1px solid #334155; background: rgba(15, 23, 42, 0.6); color: #F1F5F9; font-size: 1rem; resize: vertical;"></textarea>
                                    </div>
                                    
                                    <input type="hidden" name="_next" value="https://whisperhedge.com/contact?success=true">
                                    
                                    <button type="submit" 
                                            style="width: 100%; padding: 0.75rem 1.5rem; border-radius: 6px; border: none; background: #3B82F6; color: white; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background 0.2s;">
                                        Send Message
                                    </button>
                                </form>
                                """
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
