# Adding Your First Position

This guide walks you through adding your first LP position to WhisperHedge for automated hedging protection.

## Before You Start

Make sure you have:

- ✅ A WhisperHedge account (signed up and logged in)
- ✅ A Hyperliquid account with API key
- ✅ Your Liquidity Pool NFT ID

## Step-by-Step: Adding a Position

### Step 1: Navigate to Dashboard

After logging in, you'll be on your dashboard. Click the **"+ Add Position"** button.

### Step 2: Enter Your Details

1. **API Key** - Paste your Hyperliquid read-only API key
2. **API Secret** - Paste your API secret
3. **Subaccount** (optional) - Enter subaccount name if applicable
4. **Label** (optional) - Give this position a friendly name
5. **NFT Token ID** - Your Liquidity Pool NFT ID

[How to get Hyperliquid API keys →](../api-keys/hyperliquid-keys.md)

[How to find your NFT ID →](../position-setup/uniswap-v3-nft-id.md)

!!! warning "One API Key Per Position"
    Each position requires its own unique API key. You cannot reuse the same key for multiple positions.

### Step 3: Verify & Save

1. Click **"Verify Position"** to test the connection
2. Review the position details shown
3. Click **"Save Position"** to start hedging

!!! success "Position Added!"
    Your position will appear on the dashboard within seconds. The first data fetch may take 1-2 minutes.

## Understanding Position Data

Once added, you'll see:

- **Protocol & Pair** - Platform and trading pair
- **Current Value** - Total USD value of the position
- **Token Amounts** - Quantity of each token
- **Impermanent Loss** - IL percentage and USD amount
- **Fees Earned** - Total fees collected

## Common Issues

### "Invalid API Key"

- Verify the key is copied correctly (no extra spaces)
- Ensure the key has read permissions
- Check if the key is for the correct account/subaccount
- Try generating a new key

### "Position Already Tracked"

You cannot add the same position twice. If you need to update it:

1. Delete the existing position
2. Add it again with new details

## Need Help?

- **[API Key Issues](../troubleshooting/api-key-issues.md)** - Common API problems
- **[Position Not Updating](../troubleshooting/position-not-updating.md)** - Sync issues
- **[Contact Support](../troubleshooting/contact-support.md)** - Get personalized help

---

**Congratulations!** Your position is now being hedged.
