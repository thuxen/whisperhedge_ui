# API Key Permissions

Understanding API key permissions is crucial for security. This guide explains what permissions WhisperHedge needs and why you should never grant more than necessary.

## Required Permissions

WhisperHedge only needs **read-only** access to:

### ✅ Account Data
- View account balance
- Read position information
- Access transaction history
- Check account status

### ✅ Position Data
- Current position values
- Token balances
- Liquidity ranges (Uniswap V3)
- Position health metrics

### ✅ Historical Data
- Past transactions
- Fee earnings
- Price history
- Performance metrics

## Forbidden Permissions

WhisperHedge should **NEVER** have:

### ❌ Trading Permissions
- Place orders
- Cancel orders
- Modify positions
- Execute trades

### ❌ Transfer Permissions
- Withdraw funds
- Transfer between accounts
- Send tokens
- Move liquidity

### ❌ Account Modifications
- Change settings
- Create subaccounts
- Modify API keys
- Update account details

## Platform-Specific Permissions

### Hyperliquid

**Enable:**
- ✅ Read account data
- ✅ View positions
- ✅ View orders (historical)
- ✅ View balances
- ✅ View transaction history

**Disable:**
- ❌ Place orders
- ❌ Cancel orders
- ❌ Transfer
- ❌ Withdraw
- ❌ Modify account

### Uniswap V3

For Uniswap V3, we only need:
- ✅ NFT Token ID (public information)
- ✅ Wallet address (public information)

No API keys or special permissions required - all data is read from the blockchain.

## Why Read-Only?

### Security

**Principle of Least Privilege**

Only grant the minimum permissions necessary. If WhisperHedge only needs to read data, it should only have read permissions.

**Damage Limitation**

If an API key is compromised:
- **Read-only:** Attacker can only view data
- **Trading enabled:** Attacker can drain your account

### Trust

**Verifiable Security**

You can verify that WhisperHedge:
- Never asks for trading permissions
- Cannot execute trades
- Cannot move your funds
- Only monitors positions

### Compliance

**Best Practices**

Read-only access aligns with:
- Industry security standards
- Regulatory requirements
- Audit compliance
- Risk management policies

## Verifying Permissions

### Before Adding to WhisperHedge

**Check your API key:**

1. Log into your trading platform
2. Navigate to API key management
3. Find the key you're about to use
4. Verify permissions show only "Read" or "View"
5. Confirm no "Trade", "Withdraw", or "Transfer" permissions

### In Hyperliquid

Look for these indicators:

```
API Key: abc123...
Permissions:
  ✅ Read Account Data
  ✅ View Positions
  ✅ View Orders
  ❌ Place Orders (disabled)
  ❌ Cancel Orders (disabled)
  ❌ Transfer (disabled)
  ❌ Withdraw (disabled)
```

### After Adding to WhisperHedge

**Test the limitations:**

1. Try to place a trade in Hyperliquid
2. WhisperHedge should have no impact
3. Your trading should work normally
4. WhisperHedge only displays data

## Common Permission Issues

### "Permission Denied" Error

**Cause:** API key lacks read permissions

**Solution:**
1. Check key permissions in platform
2. Ensure read access is enabled
3. Regenerate key if necessary
4. Verify correct permissions selected

### "Invalid Permissions" Error

**Cause:** Key has wrong permission set

**Solution:**
1. Delete the API key
2. Create new key
3. Select only read permissions
4. Try again

### "Trading Permission Detected"

**Cause:** Key has trading permissions (security warning)

**Solution:**
1. **Immediately** delete the key from platform
2. Create new read-only key
3. Never use keys with trading permissions

## Permission Checklist

Before using an API key with WhisperHedge:

- [ ] Read/View permissions enabled
- [ ] Trading permissions disabled
- [ ] Transfer permissions disabled
- [ ] Withdrawal permissions disabled
- [ ] Account modification permissions disabled
- [ ] Key is for correct account/subaccount
- [ ] Key is newly created (not reused)

## Best Practices

### Creation

- ✅ Always select "Read-Only" when creating keys
- ✅ Double-check permissions before saving
- ✅ Test key in safe environment first
- ✅ Document permission set

### Monitoring

- ✅ Review key permissions monthly
- ✅ Audit for unexpected changes
- ✅ Check platform security logs
- ✅ Verify no unauthorized access

### Maintenance

- ✅ Rotate keys with same permission set
- ✅ Never upgrade permissions
- ✅ Delete keys with wrong permissions
- ✅ Keep permission records

## What WhisperHedge Does

### Data We Read

- Position values and composition
- Token balances
- Fee earnings
- Transaction history
- Price data
- Performance metrics

### Data We Calculate

- Impermanent loss
- Position health scores
- ROI and APR
- Risk metrics
- Alerts and notifications

### What We Never Do

- ❌ Execute trades
- ❌ Move funds
- ❌ Modify positions
- ❌ Change settings
- ❌ Access private keys
- ❌ Sign transactions

## Security Guarantees

### Technical Safeguards

**API Key Storage:**
- Encrypted at rest
- Transmitted over HTTPS only
- Never logged or exposed
- Deleted when position removed

**Access Control:**
- Keys used only for data fetching
- No trading functionality in codebase
- Read-only database queries
- Audit trail of all access

### Organizational Safeguards

**Policies:**
- No employee access to raw keys
- Automated key handling only
- Regular security audits
- Incident response plan

## Related Topics

- **[Hyperliquid API Keys](hyperliquid-keys.md)** - How to create read-only keys
- **[API Key Security](../security/api-key-security.md)** - Security deep dive
- **[Read-Only Permissions](../security/read-only-permissions.md)** - Why read-only matters
- **[What We Store](../security/what-we-store.md)** - Data we collect

---

**Next:** [Rotating API Keys →](rotating-keys.md)
