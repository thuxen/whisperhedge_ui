# Landing Page Customization Guide

## Overview

The landing page now automatically switches based on domain:
- **whisperhedge.com** → `landing_whisperhedge.py`
- **Other domains** → `landing_whitelabel.py`

## File Structure

```
web_ui/
├── pages/
│   ├── landing.py                  ← Router (don't edit)
│   ├── landing_whisperhedge.py     ← Edit WhisperHedge landing here
│   ├── landing_whitelabel.py       ← Edit whitelabel landing here
│   ├── login.py
│   ├── signup.py
│   └── dashboard.py
└── web_ui.py                       ← Main app (no need to edit)
```

## How to Edit Landing Pages

### Edit WhisperHedge Landing (whisperhedge.com only)

**File:** `web_ui/pages/landing_whisperhedge.py`

This is your dedicated file for the WhisperHedge landing page. You can make it as complex as you want with multiple sections, tabs, animations, etc.

```python
def whisperhedge_landing() -> rx.Component:
    """Custom landing page for whisperhedge.com"""
    return rx.container(
        rx.vstack(
            # Add your custom WhisperHedge content here
            brand_logo(size="landing", margin_bottom="2rem"),
            
            # Hero section
            rx.heading("Welcome to WhisperHedge", size="8"),
            rx.text("Advanced LP Position Hedging", size="5"),
            
            # Features section
            rx.grid(
                rx.card("Feature 1"),
                rx.card("Feature 2"),
                rx.card("Feature 3"),
                columns="3",
            ),
            
            # CTA buttons
            rx.hstack(
                rx.link(rx.button("Sign In", size="3"), href="/login"),
                rx.link(rx.button("Create Account", size="3"), href="/signup"),
                spacing="4",
            ),
        ),
    )
```

### Edit Whitelabel Landing (all other domains)

**File:** `web_ui/pages/landing_whitelabel.py`

This is the simple version for whitelabel partners. Keep it minimal and generic.

```python
def whitelabel_landing() -> rx.Component:
    """Simple landing page for whitelabel partners"""
    return rx.container(
        rx.vstack(
            # Simple whitelabel content
            brand_logo(size="landing", margin_bottom="2rem"),
            rx.text(BrandConfig.TAGLINE, size="5"),
            
            # Basic CTA
            rx.hstack(
                rx.link(rx.button("Sign In", size="3"), href="/login"),
                rx.link(rx.button("Create Account", size="3"), href="/signup"),
                spacing="4",
            ),
        ),
    )
```

## Testing Your Changes

### Test WhisperHedge Version
```bash
export REFLEX_DOMAIN=whisperhedge.com
reflex run
# Visit http://localhost:3000
```

### Test Whitelabel Version
```bash
unset REFLEX_DOMAIN
reflex run
# Visit http://localhost:3000
```

## Example: Adding a Hero Section to WhisperHedge

```python
def whisperhedge_landing() -> rx.Component:
    return rx.container(
        # Hero Section
        rx.section(
            rx.vstack(
                brand_logo(size="landing", margin_bottom="2rem"),
                rx.heading(
                    "Protect Your Liquidity Positions",
                    size="9",
                    weight="bold",
                    text_align="center",
                ),
                rx.text(
                    "Advanced automated hedging for Uniswap V3 and beyond",
                    size="5",
                    color="gray",
                    text_align="center",
                    max_width="600px",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Get Started Free", size="4"),
                        href="/signup",
                    ),
                    rx.link(
                        rx.button("Watch Demo", size="4", variant="soft"),
                        href="#demo",
                    ),
                    spacing="4",
                ),
                spacing="6",
                align="center",
                padding="4rem 1rem",
            ),
        ),
        
        # Features Section
        rx.section(
            rx.vstack(
                rx.heading("Features", size="7", text_align="center"),
                rx.grid(
                    rx.card(
                        rx.vstack(
                            rx.icon("shield", size=32),
                            rx.heading("Automated Protection", size="5"),
                            rx.text("Set it and forget it hedging"),
                        ),
                    ),
                    rx.card(
                        rx.vstack(
                            rx.icon("activity", size=32),
                            rx.heading("Real-time Monitoring", size="5"),
                            rx.text("Track your positions 24/7"),
                        ),
                    ),
                    rx.card(
                        rx.vstack(
                            rx.icon("trending-up", size=32),
                            rx.heading("Dynamic Strategies", size="5"),
                            rx.text("Adaptive hedging algorithms"),
                        ),
                    ),
                    columns="3",
                    spacing="4",
                ),
                spacing="6",
                padding="4rem 1rem",
            ),
        ),
        
        # CTA Section
        rx.section(
            rx.vstack(
                rx.heading("Ready to Get Started?", size="7"),
                rx.hstack(
                    rx.link(rx.button("Sign In", size="3"), href="/login"),
                    rx.link(rx.button("Create Account", size="3", variant="soft"), href="/signup"),
                    spacing="4",
                ),
                spacing="4",
                align="center",
                padding="4rem 1rem",
            ),
        ),
    )
```

## Key Points

✅ **Separate Functions**: Each domain has its own function  
✅ **Easy to Customize**: Edit only the landing page you want to change  
✅ **Automatic Switching**: Domain detection happens automatically  
✅ **Shared Backend**: Both versions use the same authentication and features  
✅ **Independent Styling**: Style each landing page differently  

## What's Shared vs. What's Different

### Shared (Same for All)
- Login page (`/login`)
- Signup page (`/signup`)
- Dashboard (`/dashboard`)
- All backend logic
- Authentication system
- Position management

### Different (Domain-Specific)
- Landing page content (home `/`)
- Branding (APP_NAME, TAGLINE, etc.)
- Logo/assets (if customized)

## Next Steps

1. Edit `whisperhedge_landing()` to create your custom WhisperHedge landing page
2. Keep `whitelabel_landing()` simple for partners
3. Test both versions locally
4. Deploy - the VPS will automatically show the WhisperHedge version!
