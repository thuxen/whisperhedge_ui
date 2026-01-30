# Domain-Based Branding Deployment Guide

## Overview

The application now supports automatic domain-based branding:
- **whisperhedge.com** → Shows "WhisperHedge" branding
- **Any other domain** → Shows "White Label" branding

## How It Works

The branding system checks the `REFLEX_DOMAIN` environment variable to determine which branding to display:

```python
# If REFLEX_DOMAIN contains "whisperhedge.com"
APP_NAME = "WhisperHedge"
TAGLINE = "Liquidity Pool Hedging Simplified"

# Otherwise (whitelabel)
APP_NAME = "White Label"
TAGLINE = "Automated Hedging Platform"
```

## Testing Locally

### Test WhisperHedge Version (Production)
```bash
# Set REFLEX_DOMAIN environment variable
export REFLEX_DOMAIN=whisperhedge.com
reflex run
```

### Test Whitelabel Version (Default)
```bash
# Don't set REFLEX_DOMAIN (or set to any other domain)
reflex run

# Or explicitly test with a partner domain
export REFLEX_DOMAIN=metrix.finance
reflex run
```

### Quick Test Script
```bash
python test_branding.py
```

This will show you how the branding changes based on the HOST variable.

## Deployment

### On Your VPS (whisperhedge.com)

**Good news**: You already have `REFLEX_DOMAIN=whisperhedge.com` set on your VPS!

No changes needed - the branding will automatically detect this and show WhisperHedge branding.

**Result**: Users visiting whisperhedge.com will see "WhisperHedge" branding.

### For Whitelabel Partners

Partners deploy the same codebase but **don't set REFLEX_DOMAIN** or set it to their domain:

```bash
# Partner's .env file
REFLEX_DOMAIN=metrix.finance
# Or leave REFLEX_DOMAIN unset for automatic whitelabel
```

**Result**: Users will see "White Label" branding.

## What Changes Based on Domain

| Element | WhisperHedge | White Label |
|---------|-------------|-------------|
| App Name | WhisperHedge | White Label |
| Company Name | WhisperHedge | White Label |
| Tagline | Liquidity Pool Hedging Simplified | Automated Hedging Platform |
| Support Email | support@whisperhedge.com | support@example.com |
| Docs URL | https://docs.whisperhedge.com | (empty) |

## Backend Sharing

All deployments share the **same backend code**:
- Authentication system
- Position management
- Hedging logic
- API integrations

Only the **frontend branding** changes based on domain.

## Future Customization

Partners can further customize by setting environment variables:
```bash
BRAND_APP_NAME="Custom Name"
BRAND_TAGLINE="Custom Tagline"
BRAND_SUPPORT_EMAIL="custom@email.com"
```

These will override the domain-based defaults.
