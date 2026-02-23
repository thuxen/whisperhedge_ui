# Read-Only Permissions

Why WhisperHedge only requires read-only API access and never needs trading permissions.

## What is Read-Only Access?

Read-only permissions allow WhisperHedge to:

### ✅ View Data
- Position information
- Account balances
- Transaction history
- Fee earnings
- Token holdings

### ❌ Never Modify
- Cannot place trades
- Cannot cancel orders
- Cannot transfer funds
- Cannot withdraw assets
- Cannot change settings

## Why Read-Only?

### 1. Security

**Principle of Least Privilege**

We only request the minimum permissions needed. Since we only need to monitor positions, we only need read access.

**Damage Limitation**

If an API key is compromised:
- **Read-only:** Attacker can only view data
- **Trading enabled:** Attacker can drain your account

### 2. Trust

**Verifiable Security**

You can verify that:
- We never ask for trading permissions
- We cannot execute trades
- We cannot move your funds
- We only monitor positions

**Transparency**

Our read-only requirement proves we:
- Don't have hidden functionality
- Can't access your funds
- Are transparent about capabilities
- Prioritize your security

### 3. Compliance

**Best Practices**

Read-only access aligns with:
- Security industry standards
- Regulatory requirements
- Audit compliance
- Risk management

## What We Can Do

With read-only access, we can:

### Monitor Positions
- Track position values
- Calculate impermanent loss
- Monitor fee earnings
- Assess position health

### Calculate Metrics
- Historical performance
- ROI and APR
- Risk scores
- Alerts and notifications

### Provide Insights
- Position analysis
- Performance comparisons
- Health warnings
- Optimization suggestions

## What We Cannot Do

With read-only access, we cannot:

### Trading
- ❌ Place buy/sell orders
- ❌ Cancel existing orders
- ❌ Modify position sizes
- ❌ Execute any trades

### Transfers
- ❌ Withdraw funds
- ❌ Transfer between accounts
- ❌ Send tokens
- ❌ Move liquidity

### Account Changes
- ❌ Change settings
- ❌ Create subaccounts
- ❌ Modify API keys
- ❌ Update account details

## Verification

### How to Verify

**Before Adding Keys:**
1. Check key permissions in platform
2. Confirm only "Read" or "View" enabled
3. Verify no "Trade" or "Transfer" permissions
4. Test that trading still works normally

**After Adding Keys:**
1. Try placing a trade in your platform
2. WhisperHedge should have no impact
3. Your trading should work normally
4. WhisperHedge only displays data

### Red Flags

If a platform asks for:
- ❌ Trading permissions
- ❌ Withdrawal permissions
- ❌ Transfer permissions
- ❌ Account modification rights

**Do not provide these permissions to WhisperHedge or any monitoring service.**

## Platform Comparison

### Hyperliquid

**Read-Only Includes:**
- ✅ View positions
- ✅ View balances
- ✅ View orders (historical)
- ✅ View transaction history

**Read-Only Excludes:**
- ❌ Place orders
- ❌ Cancel orders
- ❌ Transfer
- ❌ Withdraw

### Uniswap V3

**No API Key Needed:**
- ✅ All data is on-chain (public)
- ✅ Only need NFT ID
- ✅ No permissions required
- ✅ Cannot execute any actions

## Security Benefits

### Compromised Key Scenario

**With Read-Only:**
```
Attacker gets API key
→ Can view your positions
→ Can see your balances
→ Cannot trade
→ Cannot steal funds
→ Limited damage
```

**With Trading Enabled:**
```
Attacker gets API key
→ Can view your positions
→ Can execute trades
→ Can drain your account
→ Can transfer funds
→ Total loss possible
```

### Risk Comparison

| Scenario | Read-Only | Trading Enabled |
|----------|-----------|-----------------|
| Data exposure | ⚠️ Low risk | ⚠️ Low risk |
| Fund loss | ✅ No risk | 🚨 High risk |
| Unauthorized trades | ✅ No risk | 🚨 High risk |
| Account takeover | ✅ No risk | 🚨 High risk |

## Industry Standards

### What Others Do

**Legitimate monitoring services:**
- ✅ Request read-only only
- ✅ Explain why
- ✅ Provide security guarantees
- ✅ Never ask for trading access

**Suspicious services:**
- 🚨 Request trading permissions
- 🚨 Don't explain why
- 🚨 Vague about security
- 🚨 Pressure you to grant access

### Our Commitment

We commit to:
- ✅ Never requesting trading permissions
- ✅ Never adding trading functionality
- ✅ Maintaining read-only requirement
- ✅ Transparent about capabilities

## FAQ

**Q: Why can't I use a trading-enabled key?**
A: For your security. We enforce read-only to prevent potential fund loss.

**Q: What if I accidentally use a trading key?**
A: Delete it immediately and create a read-only key.

**Q: Can you add trading features later?**
A: No. We will never add trading functionality. Our focus is monitoring only.

**Q: How do I verify you're read-only?**
A: Check our code (open source), verify key permissions, test that trading still works.

**Q: What if my platform doesn't support read-only?**
A: Contact us. We may not support that platform for security reasons.

## Related Topics

- [API Key Security](api-key-security.md)
- [API Key Permissions](../api-keys/permissions.md)
- [What We Store](what-we-store.md)
- [Data Privacy](data-privacy.md)
