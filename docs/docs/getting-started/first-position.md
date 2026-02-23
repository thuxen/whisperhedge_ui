# Adding Your First Position

This guide walks you through adding your first LP position to WhisperHedge. We'll cover both Hyperliquid and Uniswap V3 positions.

## Before You Start

Make sure you have:

- ✅ A WhisperHedge account (signed up and logged in)
- ✅ An active LP position on Hyperliquid or Uniswap V3
- ✅ API keys or NFT ID ready (see below)

## Choose Your Protocol

### Hyperliquid Positions

For Hyperliquid HLP positions, you'll need:

1. **Hyperliquid API Key** - Read-only access to your account
2. **Subaccount Name** (if using subaccounts)

[How to get Hyperliquid API keys →](../api-keys/hyperliquid-keys.md)

### Uniswap V3 Positions

For Uniswap V3 positions, you'll need:

1. **NFT Token ID** - The unique ID of your LP position NFT
2. **Wallet Address** - The address holding the NFT

[How to find your NFT ID →](../position-setup/uniswap-v3-nft-id.md)

## Step-by-Step: Adding a Position

### Step 1: Navigate to Dashboard

After logging in, you'll be on your dashboard. Click the **"+ Add Position"** button.

### Step 2: Select Protocol

Choose your protocol:

- **Hyperliquid** - For HLP positions
- **Uniswap V3** - For concentrated liquidity positions

### Step 3: Enter Details

#### For Hyperliquid:

1. **API Key** - Paste your read-only API key
2. **API Secret** - Paste your API secret
3. **Subaccount** (optional) - Enter subaccount name if applicable
4. **Label** (optional) - Give this position a friendly name

!!! warning "One API Key Per Position"
    Each position requires its own unique API key. You cannot reuse the same key for multiple positions. [Learn why →](../api-keys/one-key-per-position.md)

#### For Uniswap V3:

1. **NFT Token ID** - Enter your position's NFT ID
2. **Wallet Address** - Enter the wallet holding the NFT
3. **Network** - Select the network (Ethereum, Polygon, etc.)
4. **Label** (optional) - Give this position a friendly name

### Step 4: Verify & Save

1. Click **"Verify Position"** to test the connection
2. Review the position details shown
3. Click **"Save Position"** to start tracking

!!! success "Position Added!"
    Your position will appear on the dashboard within seconds. The first data fetch may take 1-2 minutes.

## Understanding Position Data

Once added, you'll see:

### Basic Information

- **Protocol & Pair** - Platform and trading pair
- **Current Value** - Total USD value of the position
- **Token Amounts** - Quantity of each token
- **Price Range** (Uniswap V3) - Your liquidity range

### Performance Metrics

- **Impermanent Loss** - IL percentage and USD amount
- **Fees Earned** - Total fees collected
- **Net P&L** - Fees minus IL
- **APR** - Annualized return rate

### Health Status

- **Health Score** - Overall position health (0-100)
- **Risk Level** - Low, Medium, High
- **Alerts** - Any active warnings

## Common Issues

### "Invalid API Key"

**Hyperliquid:**

- Verify the key is copied correctly (no extra spaces)
- Ensure the key has read permissions
- Check if the key is for the correct account/subaccount
- Try generating a new key

**Uniswap V3:**

- Verify the NFT ID is correct
- Ensure the wallet address owns the NFT
- Check you're on the correct network

### "Position Already Tracked"

You cannot add the same position twice. If you need to update it:

1. Delete the existing position
2. Add it again with new details

### "Plan Limit Exceeded"

Your current plan has limits on:

- Total TVL (value locked)
- Number of positions

[Upgrade your plan →](../features/plan-tiers.md) to track more positions.

## Next Steps

After adding your first position:

### 1. Set Up Notifications

Configure alerts for position health changes:

[Notification setup guide →](../features/notifications.md)

### 2. Add More Positions

Track all your LP positions in one place:

- Each Hyperliquid position needs its own API key
- Add multiple Uniswap V3 positions with different NFT IDs

### 3. Monitor Performance

Check your dashboard regularly to:

- Track impermanent loss
- Monitor fee earnings
- Assess position health
- Make informed decisions

### 4. Understand the Metrics

Learn more about what you're seeing:

- [LP Tracking Details →](../features/lp-tracking.md)
- [Impermanent Loss Explained →](../features/impermanent-loss.md)
- [Position Health Indicators →](../features/position-health.md)

## Best Practices

### Security

- ✅ Always use **read-only** API keys
- ✅ Never share your API secrets
- ✅ Rotate keys periodically
- ✅ Delete unused positions

### Organization

- ✅ Use descriptive labels for positions
- ✅ Group similar positions together
- ✅ Review positions weekly
- ✅ Remove closed positions promptly

### Monitoring

- ✅ Enable email notifications
- ✅ Set appropriate alert thresholds
- ✅ Check dashboard daily (or use notifications)
- ✅ Act on critical health warnings

## Need Help?

- **[API Key Issues](../troubleshooting/api-key-issues.md)** - Common API problems
- **[Position Not Updating](../troubleshooting/position-not-updating.md)** - Sync issues
- **[Contact Support](../troubleshooting/contact-support.md)** - Get personalized help

---

**Congratulations!** You've added your first position. Now explore the [Features](../features/index.md) to get the most out of WhisperHedge.
