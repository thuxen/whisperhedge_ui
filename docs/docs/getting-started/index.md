# Getting Started with WhisperHedge

This guide will get you up and running with automated IL hedging in minutes. If you're semi-competent, this is all you need.

## Prerequisites

Before you start, make sure you have:

- ✅ A Hyperliquid account with API access
- ✅ An active LP position (Uniswap V3 NFT)
- ✅ Your LP position's NFT Token ID

## Step 1: Add Your Hyperliquid API Keys

Each LP position you want to hedge requires its own unique Hyperliquid API key with read-only permissions.

### Creating API Keys

1. Log into Hyperliquid
2. Navigate to API settings
3. Create a new API key with **read-only** permissions
4. Copy both the API key and secret (you'll need these in the next step)

!!! warning "One Key Per Position"
    You cannot reuse the same API key for multiple positions. Each position needs its own dedicated key.

**Detailed instructions:** [Hyperliquid API Keys Guide](../api-keys/hyperliquid-keys.md)

## Step 2: Add Your LP Position

### Navigate to Dashboard

After logging in, click the **"+ Add Position"** button on your dashboard.

### Enter Position Details

Fill in the following fields:

1. **API Key** - Your Hyperliquid read-only API key
2. **API Secret** - Your Hyperliquid API secret
3. **Subaccount** (optional) - Enter subaccount name if you're using Hyperliquid subaccounts
4. **Label** (optional) - Give this position a friendly name for easy identification
5. **NFT Token ID** - Your Uniswap V3 LP position NFT ID

**Need your NFT ID?** [How to find your Uniswap V3 NFT ID →](../position-setup/uniswap-v3-nft-id.md)

### Verify & Save

1. Click **"Verify Position"** to test the API connection
2. Review the position details displayed (protocol, pair, current value)
3. Click **"Save Position"** to activate automated hedging

!!! success "Position Added!"
    Your position will appear on the dashboard within seconds. The first data fetch may take 1-2 minutes.

## Step 3: Configure Hedging Strategy

Once your position is added, configure your automated hedging strategy:

- **Variance-based rebalancing** - Hedge when delta exposure exceeds your threshold
- **Asymmetric under-hedging** - Optimize for net profit vs. perfect hedging
- **Funding-rate awareness** - Factor in perpetual funding costs

**Full strategy options:** [Hedging Strategy Guide](../hedging-strategy/index.md)

## Understanding Your Dashboard

Once your position is active, you'll see:

- **Protocol & Pair** - Platform (e.g., Uniswap V3) and trading pair (e.g., ETH/USDC)
- **Current Value** - Total USD value of your LP position
- **Token Amounts** - Quantity of each token in the pool
- **Impermanent Loss** - IL percentage and USD amount
- **Fees Earned** - Total fees collected from the LP position
- **Hedge Status** - Current hedge ratio and perpetual position details

## Troubleshooting

### "Invalid API Key"

- Verify the key is copied correctly (no extra spaces)
- Ensure the key has read permissions enabled
- Check if the key is for the correct account/subaccount
- Try generating a new key

### "Position Already Tracked"

You cannot add the same position twice. To update a position:

1. Delete the existing position from your dashboard
2. Add it again with the updated details

### Position Not Updating

- Wait 1-2 minutes for the initial data fetch
- Check that your API key hasn't been revoked
- Verify the NFT ID is correct

**More help:** [Troubleshooting Guide](../troubleshooting/index.md)

---

**That's it!** Your LP position is now protected with automated IL hedging. WhisperHedge will monitor your delta exposure and execute hedge trades on Hyperliquid as needed.

## Need Help?

- [FAQ](../faq.md) - Common questions
- [API Key Issues](../troubleshooting/api-key-issues.md) - API problems
- [Contact Support](../troubleshooting/contact-support.md) - Get personalized help
