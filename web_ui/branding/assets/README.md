# Branding Assets

This directory contains your custom branding assets (logos, favicons, etc.).

## Quick Start

**No logo?** The app will automatically use text-based branding. No action needed!

**Want to add your logo?** Simply drop your logo files here and restart the app.

## Supported Files

### Logos

Place your logo files in this directory with these exact names:

- `logo.svg` - Light mode logo (SVG format, recommended)
- `logo-dark.svg` - Dark mode logo (SVG format, optional)
- `logo.png` - Light mode logo (PNG format, fallback)
- `logo-dark.png` - Dark mode logo (PNG format, optional)

**Priority:** The app will use SVG if available, otherwise PNG. If no dark mode logo is provided, the light logo will be used in dark mode.

### Favicon

- `favicon.ico` - Browser tab icon (16x16 or 32x32 pixels)

## Logo Specifications

### Recommended Formats

- **SVG (Preferred)**: Scalable, crisp at any size, small file size
- **PNG**: Use if SVG is not available

### Size Guidelines

**Navbar Logo:**
- Height: 32px (auto-width)
- Recommended: Horizontal logo or icon + text

**Landing Page Logo:**
- Height: 48px (auto-width)
- Recommended: Full logo with text

**Sidebar Logo:**
- Height: 28px (auto-width)
- Recommended: Compact version or icon only

### Design Tips

- Use transparent backgrounds for PNG files
- Ensure logos are readable at small sizes
- Test in both light and dark modes
- Keep file sizes small (< 100KB recommended)

## Customization via Environment Variables

You can override default paths in your `.env` file:

```env
BRAND_LOGO_LIGHT_SVG=/custom/path/logo.svg
BRAND_LOGO_DARK_SVG=/custom/path/logo-dark.svg
BRAND_LOGO_LIGHT=/custom/path/logo.png
BRAND_LOGO_DARK=/custom/path/logo-dark.png
BRAND_FAVICON=/custom/path/favicon.ico
```

## File Structure

```
branding/assets/
├── README.md          # This file
├── .gitkeep           # Keeps directory in git
├── logo.svg           # Your light mode logo (SVG)
├── logo-dark.svg      # Your dark mode logo (SVG, optional)
├── logo.png           # Your light mode logo (PNG, fallback)
├── logo-dark.png      # Your dark mode logo (PNG, optional)
└── favicon.ico        # Your favicon
```

## Notes

- These files are gitignored by default (except README.md and .gitkeep)
- The app will work perfectly fine without any logos
- Logo loading failures will gracefully fallback to text
- Changes require app restart to take effect
