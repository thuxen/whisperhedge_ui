# Understanding Hyperliquid Subaccounts

Hyperliquid subaccounts allow you to manage multiple trading strategies or positions under a single main account. This guide explains how subaccounts work and how to use them with WhisperHedge.

## What Are Subaccounts?

Subaccounts are separate trading accounts that exist under your main Hyperliquid account. Think of them as:

- **Separate wallets** - Each has its own balance and positions
- **Independent strategies** - Isolate different trading approaches
- **Organizational tools** - Keep positions organized by strategy or purpose

### Main Account vs Subaccounts

**Main Account:**
- Your primary Hyperliquid account
- Connected to your wallet
- Can create and manage subaccounts
- Has its own positions and balances

**Subaccounts:**
- Created from your main account
- Have unique names (e.g., "Strategy A", "HLP-ETH")
- Maintain separate balances
- Require separate API keys
- Can be funded from main account

## Why Use Subaccounts?

### Strategy Isolation

Keep different strategies separate:

```
Main Account
├── Subaccount: "Conservative HLP"
│   └── Low-risk, stable pairs
├── Subaccount: "Aggressive HLP"
│   └── High-risk, volatile pairs
└── Subaccount: "Arbitrage"
    └── Arbitrage positions
```

### Risk Management

- Limit exposure per strategy
- Prevent cross-contamination
- Easy to close entire strategy
- Clear P&L per approach

### Organization

- Track performance by strategy
- Separate personal vs business
- Manage multiple clients
- Clean accounting

## Creating Subaccounts

### In Hyperliquid

1. Log into Hyperliquid
2. Navigate to account settings
3. Find "Subaccounts" section
4. Click "Create Subaccount"
5. Enter a descriptive name
6. Fund the subaccount (optional)

!!! tip "Naming Convention"
    Use clear, descriptive names like:
    - "HLP-ETHUSDC-Conservative"
    - "Strategy-A-High-Risk"
    - "Client-ABC-Portfolio"

### Funding Subaccounts

To move funds to a subaccount:

1. Go to your main account
2. Select "Transfer to Subaccount"
3. Choose destination subaccount
4. Enter amount
5. Confirm transfer

Funds can be moved back to main account anytime.

## Using Subaccounts with WhisperHedge

### API Keys for Subaccounts

Each subaccount needs its own API key:

1. **Select the subaccount** when creating the API key in Hyperliquid
2. **Note the subaccount name** - You'll need this exact name
3. **Create read-only key** for that specific subaccount
4. **Use in WhisperHedge** by entering the subaccount name

### Adding Subaccount Positions

When adding a position in WhisperHedge:

1. Generate API key for the specific subaccount
2. Add position as normal
3. **Enter the exact subaccount name** in the subaccount field
4. Verify and save

!!! warning "Exact Name Required"
    The subaccount name must match exactly (including capitalization, spaces, special characters). "Strategy A" ≠ "strategy a" ≠ "StrategyA"

### Example Setup

**Scenario:** You have 3 HLP positions across 2 subaccounts

```
Main Account (not tracked)

Subaccount: "Conservative"
├── Position 1: ETH/USDC HLP
│   └── API Key 1 (read-only, for "Conservative")
└── Position 2: BTC/USDC HLP
    └── API Key 2 (read-only, for "Conservative")

Subaccount: "Aggressive"
└── Position 3: SOL/USDC HLP
    └── API Key 3 (read-only, for "Aggressive")
```

**In WhisperHedge:**

Position 1:
- API Key: [key1]
- API Secret: [secret1]
- Subaccount: "Conservative"

Position 2:
- API Key: [key2]
- API Secret: [secret2]
- Subaccount: "Conservative"

Position 3:
- API Key: [key3]
- API Secret: [secret3]
- Subaccount: "Aggressive"

## Common Patterns

### Strategy-Based Organization

```
Main Account
├── "Long-Term-Hold" - Conservative, low-fee pairs
├── "Active-Trading" - Frequent rebalancing
└── "Experimental" - Testing new strategies
```

### Risk-Based Organization

```
Main Account
├── "Low-Risk" - Stable pairs, tight ranges
├── "Medium-Risk" - Balanced approach
└── "High-Risk" - Volatile pairs, wide ranges
```

### Client-Based Organization

```
Main Account
├── "Personal" - Your own positions
├── "Client-A" - Client A's positions
└── "Client-B" - Client B's positions
```

## Tracking Subaccount Performance

### In WhisperHedge

Each position shows its subaccount in the dashboard:

| Position | Subaccount | Value | IL% |
|----------|------------|-------|-----|
| ETH/USDC | Conservative | $10K | -2% |
| BTC/USDC | Conservative | $15K | -1% |
| SOL/USDC | Aggressive | $5K | -8% |

### Filtering by Subaccount

Use dashboard filters to:

- View all positions in a subaccount
- Compare performance across subaccounts
- Aggregate metrics by strategy

## Best Practices

### Naming

- ✅ Use descriptive, clear names
- ✅ Include strategy or purpose
- ✅ Keep names consistent
- ✅ Avoid special characters if possible

### Organization

- ✅ One strategy per subaccount
- ✅ Document subaccount purposes
- ✅ Review subaccount structure quarterly
- ✅ Archive unused subaccounts

### Security

- ✅ Separate API keys per subaccount
- ✅ Limit funding to necessary amounts
- ✅ Monitor each subaccount independently
- ✅ Close subaccounts when done

### In WhisperHedge

- ✅ Track each subaccount separately
- ✅ Use consistent naming
- ✅ Label positions clearly
- ✅ Monitor aggregate metrics

## Troubleshooting

### "Subaccount Not Found"

**Causes:**
- Typo in subaccount name
- Wrong capitalization
- Extra spaces
- Subaccount doesn't exist

**Solutions:**
1. Copy exact name from Hyperliquid
2. Check for spaces before/after name
3. Verify capitalization matches
4. Confirm subaccount exists

### "No Positions in Subaccount"

**Causes:**
- API key is for wrong subaccount
- Positions exist in different subaccount
- Subaccount is empty

**Solutions:**
1. Verify API key subaccount selection
2. Check which subaccount has the position
3. Confirm position exists in Hyperliquid

### "Permission Denied"

**Cause:** API key not authorized for that subaccount

**Solution:**
1. Regenerate API key
2. Select correct subaccount during creation
3. Verify read permissions enabled

## Main Account Positions

### Tracking Main Account

To track positions in your main account (not a subaccount):

1. Create API key for main account
2. In WhisperHedge, leave subaccount field **empty**
3. Or enter "Main Account" if required

### When to Use Main Account

Use main account for:

- Single-strategy users
- Simple setups
- Testing WhisperHedge
- Personal positions only

Use subaccounts for:

- Multiple strategies
- Client management
- Risk isolation
- Complex setups

## Migration Strategies

### Moving to Subaccounts

If you're currently using main account and want to organize with subaccounts:

1. **Plan your structure** - Decide on subaccount names/purposes
2. **Create subaccounts** in Hyperliquid
3. **Transfer positions** (if possible) or close and reopen
4. **Update WhisperHedge** - Remove old positions, add new ones with subaccount names
5. **Generate new API keys** for each subaccount

### Consolidating Subaccounts

If you want to simplify:

1. **Close positions** in subaccounts you want to remove
2. **Transfer funds** back to main account
3. **Remove positions** from WhisperHedge
4. **Delete subaccounts** in Hyperliquid

## Advanced Topics

### Subaccount Limits

Hyperliquid may have limits on:

- Number of subaccounts per main account
- Transfers between accounts
- API key creation

Check Hyperliquid documentation for current limits.

### API Key Scope

API keys are scoped to:

- Specific subaccount (or main account)
- Cannot access other subaccounts
- Cannot access main account (if created for subaccount)

This is a security feature.

### Cross-Subaccount Transfers

Transfers between subaccounts:

- Must go through main account
- Cannot transfer directly between subaccounts
- Requires two transactions (sub→main, main→sub)

## Related Topics

- **[Hyperliquid API Keys](hyperliquid-keys.md)** - How to create keys
- **[One Key Per Position](one-key-per-position.md)** - Why separate keys matter
- **[Permissions](permissions.md)** - API key permissions explained
- **[Troubleshooting](../troubleshooting/api-key-issues.md)** - Fix common issues

---

**Next:** [API Key Permissions →](permissions.md)
