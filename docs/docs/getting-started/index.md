# Getting Started with WhisperHedge

This guide will get you up and running with automated LP hedging in minutes. 

## Prerequisites

Before you start, make sure you have:

- ✅ A WhisperHedge account
- ✅ A Hyperliquid account
- ✅ An active Liquidity Pool position (check our supported LP protocols here)
- ✅ Your LP position's NFT Token ID

## Understanding Hyperliquid Account Structure

Your Hyperliquid **wallet** (0x address) can contain multiple **trading accounts**:

- 1 Master account
- Multiple Sub-accounts 

**Key points:**

- ✅ One API key works for all trading accounts in your wallet
- ✅ Each LP position you hedge needs its own dedicated trading account (Master or Sub-Account)
- ✅ Each trading account needs its own funds for hedging
- ✅ You need 100k USD of trading volume before you can create Sub-Accounts. If you need to hedge multiple LP positions, you may need multiple Wallet accounts on Hyperliquid, each will require its own API key.

## Step 1: Create Your Hyperliquid API Key

1. Log into Hyperliquid
2. Navigate to More > API 
3. Give the new API key a name, click Generate and Authorize API Wallet
4. Select the number of days validity for the key (max 180 days)
5. Copy the PRIVATE KEY (in red at the bottom), make sure you save this, it won't be displayed again.

The API WALLET ADDRESS is not required.

**Remember:** One API key works across all trading accounts in your wallet, but each LP position needs its own dedicated trading account.

**Detailed instructions:** [Hyperliquid API Keys Guide](../trading-accounts/hyperliquid-keys.md)

## Step 2: Add Your Trading Account to WhisperHedge

1. Navigate to **Trading Accounts** in the sidebar
2. In the **"Add New Trading Account"** box
3. Fill in the following fields:
   - **Account Name** - Give this trading account a name (e.g., "Main Account" or "ETH-USDC Sub")
   - **Exchange** - Leave this as hyperliquid
   - **API Secret** - Paste your Hyperliquid PRIVATE KEY from Step 1
   - **Master Wallet Address / Sub-Account Address** - Enter your main wallet address or the Sub-Account address
   - **Master Account or Sub-Account** - If you're using your Master account, check this box, otherwise leave it unchecked
   - **Notes** (optional) - For any notes you want to add
4. Click **"Add Trading Account"** to save it

!!! success "Trading Account Added!"
    Your trading account is now saved and can be assigned to LP positions for hedging. You can verify this works by clicking the **Check Balance** button. If it works, you should see your wallet balance displayed.

## Step 3: Add Your LP Position

### Navigate to Dashboard

Navigate to **LP Positions** in the sidebar

### Fetch Position Details

In the **"Add New LP Position"** section

1. Select Protocol (e.g., Uniswap V3)
2. Select Network (e.g., Ethereum, Arbitrum, Base, Polygon, Optimism)
3. Enter Position NFT ID
4. Click **Fetch Position Data**

**Need your NFT ID?** [How to find your NFT ID →](../position-setup/finding-nft-id.md)

### Save Position

This should fetch your position details and display them along with the hedging configuration options.

At this point if **Hedging Enabled** is unticked, you can go ahead and save your position.

Fill in the following fields:

1. **Position Name** - Give this position a friendly name for easy identification
2. **Network** - Select the blockchain network (e.g., Arbitrum, Base)
3. **NFT Token ID** - Your Uniswap V3 LP position NFT ID
4. **Trading Account** - Select which trading account to use for hedging this position
5. **Hedge Ratio** - Set your desired hedge ratio (e.g., 80% for asymmetric hedging)

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

### "Trading Account Connection Failed"

- Verify the private key is copied correctly (no extra spaces)
- Ensure the key has trading permissions enabled
- Check if the wallet address and subaccount name are correct
- Try generating a new API key on Hyperliquid

### "Position Already Tracked"

You cannot add the same position twice. To update a position:

1. Delete the existing position from your dashboard
2. Add it again with the updated details

### Position Not Updating

- Wait 1-2 minutes for the initial data fetch
- Check that your trading account credentials are still valid
- Verify the NFT ID is correct

**More help:** [Troubleshooting Guide](../troubleshooting/index.md)

---

**That's it!** Your LP position is now protected with automated IL hedging. WhisperHedge will monitor your delta exposure and execute hedge trades on Hyperliquid as needed.

## Need Help?

- [FAQ](../faq.md) - Common questions
- [Troubleshooting Guide](../troubleshooting/index.md) - Common issues
- [Contact Support](../troubleshooting/contact-support.md) - Get personalized help
