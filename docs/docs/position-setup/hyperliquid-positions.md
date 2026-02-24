# Hyperliquid Positions

Learn how to track your Hyperliquid HLP (Hyperliquid Liquidity Provider) positions in WhisperHedge.

## What are HLP Positions?

HLP positions on Hyperliquid allow you to provide liquidity to the platform's perpetual futures markets. As a liquidity provider, you:

- Earn fees from traders
- Take on market risk
- Can experience impermanent loss
- Benefit from trading volume

## Requirements

To track Hyperliquid positions, you need:

1. **API Key** - Read-only access
2. **API Secret** - Private key for authentication
3. **Subaccount** (optional) - If using subaccounts

[How to get API keys →](../api-keys/hyperliquid-keys.md)

## Setting Up Tracking

### Step 1: Generate API Key

1. Log into Hyperliquid
2. Navigate to API settings
3. Create new API key with read-only permissions
4. Save key and secret securely

[Detailed guide →](../api-keys/hyperliquid-keys.md)

### Step 2: Add to WhisperHedge

1. Go to dashboard
2. Click "+ Add Position"
3. Select "Hyperliquid"
4. Enter API credentials
5. Specify subaccount (if applicable)
6. Verify and save

### Step 3: Verify Tracking

- Position data should load within 1-2 minutes
- Check that values display correctly
- Verify token balances match Hyperliquid
- Confirm fee earnings are tracked

## What Gets Tracked

### Position Metrics

- **Total Value** - USD value of your HLP position
- **Token Composition** - Breakdown of assets
- **Impermanent Loss** - IL percentage and amount
- **Fees Earned** - Total fees collected
- **Net P&L** - Fees minus IL

### Performance Data

- Historical value charts
- IL over time
- Fee accumulation
- APR calculations
- Risk metrics

## Multiple Positions

### Same Subaccount

If you have multiple HLP positions in the same subaccount:

- Create separate API key for each position
- Each key scoped to same subaccount
- Track independently in WhisperHedge

[Why one key per position →](../api-keys/one-key-per-position.md)

### Different Subaccounts

If using multiple subaccounts:

- Create API key for each subaccount
- Specify correct subaccount name
- Track each separately

[Understanding subaccounts →](../api-keys/subaccounts.md)

## Troubleshooting

### Position Not Updating

**Possible causes:**
- API key permissions insufficient
- Subaccount name incorrect
- Network connectivity issues
- Rate limiting

[Troubleshooting guide →](../troubleshooting/position-not-updating.md)

### Incorrect Values

**Possible causes:**
- Data sync in progress (wait 5-10 minutes)
- Wrong subaccount selected
- Position recently modified

**Solutions:**
- Manual refresh
- Verify subaccount name
- Wait for next automatic update

## Best Practices

### API Key Management

- ✅ Use read-only permissions only
- ✅ One key per position
- ✅ Rotate keys every 3-6 months
- ✅ Delete unused keys

### Monitoring

- ✅ Enable email notifications
- ✅ Check dashboard regularly
- ✅ Act on health warnings
- ✅ Review IL weekly

### Organization

- ✅ Use descriptive labels
- ✅ Group by strategy
- ✅ Track per subaccount
- ✅ Document key mappings

## Related Topics

- [Hyperliquid API Keys](../api-keys/hyperliquid-keys.md)
- [Subaccounts](../api-keys/subaccounts.md)
- [One Key Per Position](../api-keys/one-key-per-position.md)
