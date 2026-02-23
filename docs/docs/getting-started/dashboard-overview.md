# Dashboard Overview

Your WhisperHedge dashboard is the central hub for managing automated hedging across your LP positions. This guide will help you understand the interface and navigate efficiently.

## Dashboard Layout

The dashboard consists of several key sections:

### 1. Sidebar Navigation

Located on the left side, the sidebar provides quick access to:

- **Dashboard** - Main overview of all positions
- **LP Positions** - Manage your LP positions
- **API Keys** - Manage your connected platforms
- **Settings** - Account preferences and notifications

### Key Features

### Quick Actions

**Refresh All Positions**
Click the refresh button to update all position data from the blockchain.

**Add New Position**
Use the "+ Add Position" button to track a new LP position.

**Filter & Sort**
Click column headers to sort by value or IL%.

### Position Details

Click on any position to view:

- Historical performance charts
- Detailed IL calculations
- Token composition breakdown
- Fee earnings
- Transaction history

## Navigation Tips

### Keyboard Shortcuts

- `D` - Go to Dashboard
- `K` - Go to API Keys
- `S` - Go to Settings
- `R` - Refresh all positions

### Mobile View

On mobile devices, the sidebar collapses into a hamburger menu. Tap the menu icon to access navigation.

## Understanding Metrics

### Total Value Locked (TVL)

Your total TVL is the sum of all position values. This determines your plan tier limits.

!!! warning "TVL Limits"
    If your TVL exceeds your plan limit, position updates will pause until you upgrade.

### Impermanent Loss (IL)

IL is calculated as:

```
IL% = (Current Value - Hold Value) / Hold Value × 100
```

- **Negative IL** - You would have been better holding the tokens
- **Positive IL** - Your LP position outperformed holding

See our [IL guide](../features/impermanent-loss.md) for more details.

## Common Tasks

### Adding Your First Position

1. Click "+ Add Position"
2. Select protocol (Hyperliquid or Uniswap V3)
3. Enter API key or NFT ID
4. Confirm and save

[Detailed guide →](first-position.md)

### Setting Up Notifications

1. Go to Settings
2. Navigate to Notifications section
3. Toggle email notifications
4. Set alert thresholds
5. Test with "Send Test Email"

[Notification guide →](../features/notifications.md)

### Coming Soon

We're working on dashboard customization features:

- Custom position grouping
- Personalized metrics
- Dark/light theme toggle
- Widget rearrangement

## Troubleshooting

**Positions not updating?**

- Check your API key permissions
- Verify your plan hasn't exceeded limits
- Try manual refresh
- See [troubleshooting guide](../troubleshooting/position-not-updating.md)

**Dashboard loading slowly?**

- Clear browser cache
- Check internet connection
- Try a different browser
- Contact support if persists

---

**Next:** [Add Your First Position →](first-position.md)
