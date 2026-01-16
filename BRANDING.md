# Branding Guide

This guide explains how to customize the branding of your WhisperHedge UI instance.

## Overview

The WhisperHedge UI supports complete white-labeling through a simple configuration system. You can customize:

- Company name and branding text
- Logos (with automatic fallback to text)
- Colors and themes
- Contact information
- Domain and URLs

## Quick Start

### Option 1: Text-Only Branding (Simplest)

1. Copy `web_ui/.env.example` to `web_ui/.env`
2. Set your brand name:
   ```env
   BRAND_APP_NAME=YourCompanyName
   BRAND_COMPANY_NAME=YourCompanyName
   BRAND_DOMAIN=yourcompany.com
   ```
3. Restart the app

That's it! Your brand name will appear throughout the interface.

### Option 2: Add Custom Logos

1. Follow Option 1 above
2. Add your logo files to `web_ui/branding/assets/`:
   - `logo.svg` (recommended) or `logo.png`
   - `logo-dark.svg` or `logo-dark.png` (optional, for dark mode)
   - `favicon.ico` (optional)
3. Restart the app

Your logos will automatically appear throughout the interface!

## Configuration Reference

### Environment Variables

All branding can be customized via `.env` file:

```env
# Company Information
BRAND_APP_NAME=WhisperHedge
BRAND_COMPANY_NAME=WhisperHedge
BRAND_DOMAIN=whisperhedge.com
BRAND_TAGLINE=Advanced Crypto Hedging Platform

# Logo Paths (optional - defaults work if files exist)
BRAND_LOGO_LIGHT_SVG=/branding/assets/logo.svg
BRAND_LOGO_DARK_SVG=/branding/assets/logo-dark.svg
BRAND_LOGO_LIGHT=/branding/assets/logo.png
BRAND_LOGO_DARK=/branding/assets/logo-dark.png
BRAND_FAVICON=/branding/assets/favicon.ico

# Logo Sizes (optional - defaults are optimized)
BRAND_LOGO_HEIGHT_NAVBAR=32px
BRAND_LOGO_HEIGHT_LANDING=48px
BRAND_LOGO_HEIGHT_SIDEBAR=28px

# Contact & Support
BRAND_SUPPORT_EMAIL=support@yourcompany.com
BRAND_DOCS_URL=https://docs.yourcompany.com

# Theme Colors (optional - for future use)
BRAND_PRIMARY_COLOR=#1a1a1a
BRAND_SECONDARY_COLOR=#3b82f6
```

### Logo Specifications

See `web_ui/branding/assets/README.md` for detailed logo specifications.

**Quick specs:**
- **Format**: SVG preferred, PNG acceptable
- **Background**: Transparent
- **Navbar**: 32px height
- **Landing**: 48px height
- **Sidebar**: 28px height

## How It Works

### Automatic Fallback System

The branding system uses a smart fallback hierarchy:

1. **SVG Logo** (if exists) → Best quality, scalable
2. **PNG Logo** (if exists) → Good quality, fixed size
3. **Text Name** (always works) → Safe fallback

This means:
- ✅ App works perfectly without any logos
- ✅ No configuration required for basic setup
- ✅ Add logos when ready, they'll appear automatically
- ✅ Logo loading errors won't break the app

### Theme Support

The system automatically handles light/dark mode:

- Checks for `logo-dark.svg` or `logo-dark.png` in dark mode
- Falls back to light logo if dark version doesn't exist
- Text branding works in all themes

## Deployment Scenarios

### Scenario 1: Development/Testing
```env
BRAND_APP_NAME=WhisperHedge Dev
```
No logos needed, text-only branding.

### Scenario 2: Client Deployment
```env
BRAND_APP_NAME=ClientName
BRAND_DOMAIN=client.com
BRAND_SUPPORT_EMAIL=support@client.com
```
Add client logos to `branding/assets/`, done!

### Scenario 3: Multi-Tenant
Each deployment gets its own `.env` file with unique branding. Logos can be stored in different paths if needed.

## File Organization

```
web_ui/
├── branding/
│   ├── __init__.py           # Module exports
│   ├── config.py             # Configuration class
│   ├── components.py         # Reusable brand components
│   └── assets/
│       ├── README.md         # Logo specifications
│       ├── .gitkeep          # Keep folder in git
│       ├── logo.svg          # Your logos (gitignored)
│       ├── logo-dark.svg
│       └── favicon.ico
├── .env                      # Your config (gitignored)
└── .env.example              # Template with defaults
```

## Best Practices

### For Repository Maintainers

1. Keep default WhisperHedge branding in code
2. Don't commit custom client logos to git
3. Provide clear `.env.example` with all options
4. Document logo specifications

### For Clients/Deployers

1. Copy `.env.example` to `.env` first
2. Set at minimum: `BRAND_APP_NAME` and `BRAND_DOMAIN`
3. Add logos to `branding/assets/` if desired
4. Test in both light and dark modes
5. Keep logo files small (< 100KB)

## Troubleshooting

### Logos Not Appearing?

1. Check file names match exactly: `logo.svg`, `logo.png`, etc.
2. Verify files are in `web_ui/branding/assets/`
3. Restart the app after adding logos
4. Check browser console for loading errors

### Text Showing Instead of Logo?

This is expected behavior if:
- Logo files don't exist (intentional fallback)
- Logo files are in wrong location
- File names don't match expected names

### Want to Force Text-Only?

Simply don't add any logo files. The system will use text branding automatically.

## Advanced Customization

For deeper customization beyond branding (colors, layouts, etc.), you'll need to modify the source code. The branding system is intentionally simple and focused on the most common white-labeling needs.

## Support

For questions or issues with branding setup, contact the repository maintainer or refer to the main README.md.
