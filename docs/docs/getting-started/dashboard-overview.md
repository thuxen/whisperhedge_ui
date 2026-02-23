# Dashboard Overview

Your WhisperHedge dashboard is the central hub for monitoring all your LP positions. This guide will help you understand the interface and navigate efficiently.

## Dashboard Layout

The dashboard consists of several key sections:

### 1. Sidebar Navigation

Located on the left side, the sidebar provides quick access to:

- **Dashboard** - Main overview of all positions
- **API Keys** - Manage your connected platforms
- **Settings** - Account preferences and notifications
- **Manage Plan** - View and upgrade your subscription

### 2. Plan Status Widget

At the top of the sidebar, you'll see your current plan status:

- **Plan Tier** - Free, Pro, or Premium
- **TVL Usage** - Current total value locked vs. limit
- **Positions** - Number of tracked positions vs. limit
- **Upgrade Button** - Quick access to plan upgrades

### 3. Positions Overview

The main content area displays all your tracked positions in a table format:

| Column | Description |
|--------|-------------|
| **Protocol** | Platform (Hyperliquid, Uniswap V3) |
| **Pair** | Trading pair (e.g., ETH/USDC) |
| **Current Value** | Total position value in USD |
| **IL %** | Impermanent loss percentage |
| **Health** | Position health indicator |
| **Actions** | Refresh, edit, delete buttons |

### 4. Position Health Indicators

Each position shows a health status:

- 🟢 **Healthy** - Position performing well
- 🟡 **Warning** - Approaching risk thresholds
- 🔴 **Critical** - Immediate attention needed

## Key Features

### Quick Actions

**Refresh All Positions**
Click the refresh button to update all position data from the blockchain.

**Add New Position**
Use the "+ Add Position" button to track a new LP position.

**Filter & Sort**
Click column headers to sort by value, IL%, or health status.

### Real-Time Updates

Positions automatically refresh every:

- **Free Tier** - Every 15 minutes
- **Pro Tier** - Every 5 minutes  
- **Premium Tier** - Every 1 minute

You can also manually refresh anytime.

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

### Position Health

Health is determined by:

- IL percentage thresholds
- Price volatility
- Liquidity depth
- Fee earnings vs. IL

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

### Upgrading Your Plan

1. Click "Upgrade" in the plan widget
2. Review plan options
3. Select your tier
4. Complete payment via Stripe
5. Instant activation

[Plan details →](../features/plan-tiers.md)

## Dashboard Customization

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
