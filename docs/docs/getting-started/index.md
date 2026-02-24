# Getting Started with WhisperHedge

This guide will get you up and running with automated LP hedging in minutes. 

## Prerequisites

Before you start, make sure you have:

- ✅ A WhisperHedge account
- ✅ A Hyperliquid account
- ✅ An active Liquidity Pool position (check our supported LP protocols here)
- ✅ Your LP position's NFT Token ID

Each LP position you want to hedge requires its own unique Hyperliquid account, this can be the Master account or a Sub-Account, the Master and multiple Sub-Accounts can share the same API key, but they each require their own funds for hedging.

## Step 1: Create Your Hyperliquid API Keys

1. Log into Hyperliquid
2. Navigate to More > API 
3. Give the new API key a name, click Generate and Authorize API Wallet
4. Select the number of days validity for the key (max 180 days)
5. Copy the PRIVATE KEY (in red at the bottom), make sure you save this, it won't be displayed again.

We only require the PRIVATE KEY for the API account, the API WALLET ADDRESS is not required.

You can reuse the same PRIVATE KEY for multiple positions. However each LP position requires a separate Hyperliquid account/sub-account.

**Detailed instructions:** [Hyperliquid API Keys Guide](../api-keys/hyperliquid-keys.md)

## Step 2: Add Your API Key to WhisperHedge

1. Log into your WhisperHedge dashboard
2. Navigate to **Settings** in the sidebar
3. Click on **API Keys** tab
4. Click the **"+ Add API Key"** button
5. Fill in the following fields:
   - **Label** (optional) - Give this API key a friendly name (e.g., "Main Account" or "ETH-USDC Sub")
   - **API Private Key** - Paste your Hyperliquid PRIVATE KEY from Step 1
   - **Subaccount** (optional) - Enter the subaccount name if you're using a Hyperliquid subaccount
6. Click **"Save API Key"** to add it to your account

!!! success "API Key Added!"
    Your API key is now saved and can be used when adding LP positions. You can add multiple API keys for different Hyperliquid accounts/subaccounts.

## Step 3: Add Your LP Position

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

## Step 4: Configure Hedging Strategy

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
