# Trading Accounts & Authentication

Trading accounts are how WhisperHedge securely connects to Hyperliquid to execute automated hedges for your LP positions. This section covers everything you need to know about managing trading accounts safely and effectively.

## Overview

WhisperHedge requires trading accounts to:

- ✅ Execute hedge trades on Hyperliquid
- ✅ Monitor position balances
- ✅ Manage delta exposure
- ✅ Automate IL mitigation

We require **trade-only** permissions. Trading accounts should have trading enabled but **withdrawals and transfers disabled** for security.

## Supported Platforms

### Hyperliquid

For automated hedging on Hyperliquid, you'll need:

- API Private Key (for signing transactions)
- Wallet Address (0x...)
- Master Account or Subaccount selection
- Subaccount name (if using sub-accounts)

[Set Up Hyperliquid Trading Account →](hyperliquid-keys.md)

### Uniswap V3

For Uniswap V3 positions, you'll need:

- NFT Token ID
- Wallet address

[Find Your NFT ID →](../position-setup/uniswap-v3-nft-id.md)

## Key Concepts

### Trade-Only vs Full Permissions

**Trade-Only (Required)**
- Place hedge orders
- Cancel orders
- Check balances
- View positions

**NEVER Enable These**
- Withdrawals
- Transfers
- Agent wallet permissions

!!! danger "Disable Withdrawals and Transfers"
    WhisperHedge only needs trading permissions to execute hedges. **Never** enable withdrawals or transfers on your API keys for maximum security.

### One Trading Account Per Position

WhisperHedge requires a dedicated trading account for each LP position you hedge. This is a security and operational feature that:

- Limits exposure if credentials are compromised
- Allows granular fund allocation per position
- Enables easy position removal
- Improves hedge tracking accuracy
- Prevents cross-position interference

[Learn more about this requirement →](one-key-per-position.md)

### Subaccounts

Hyperliquid supports subaccounts, which are separate trading accounts under your main wallet. Each subaccount:

- Shares the same API key as your master account
- Maintains separate balances and positions
- Requires its own dedicated funds for hedging
- Can be used as a separate trading account in WhisperHedge

[Understanding subaccounts →](subaccounts.md)

## Security Best Practices

### Creating Trading Accounts

- ✅ Use **trade-only** permissions (trading enabled, withdrawals/transfers disabled)
- ✅ Create separate trading accounts for each LP position
- ✅ Use descriptive account names in WhisperHedge
- ✅ Record key creation dates and expiration

### Storing Credentials

- ✅ Store API private keys securely (password manager)
- ✅ Never share private keys publicly
- ✅ Don't commit keys to git repositories
- ✅ Keep private keys encrypted

### Managing Trading Accounts

- ✅ Rotate API keys every 3-6 months (Hyperliquid max: 180 days)
- ✅ Delete unused trading accounts immediately
- ✅ Monitor account balances and usage
- ✅ Revoke compromised keys instantly

### In WhisperHedge

- ✅ Private keys are encrypted at rest
- ✅ Transmitted over HTTPS only
- ✅ Never logged or exposed in plaintext
- ✅ Deleted when trading account is removed

[Full security guide →](../security/api-key-security.md)

## Common Tasks

### Adding Your First Trading Account

1. Generate a trade-only API key on Hyperliquid
2. Copy the API private key
3. Go to Trading Accounts in WhisperHedge
4. Add new trading account with credentials
5. Verify balance and save

[Step-by-step guide →](hyperliquid-keys.md)

### Rotating Trading Account Credentials

1. Generate a new trade-only API key on Hyperliquid
2. Update the trading account in WhisperHedge
3. Verify the new key works (check balance)
4. Delete the old key from Hyperliquid

[Rotation guide →](rotating-keys.md)

### Troubleshooting Trading Account Issues

Common problems and solutions:

- Invalid private key format
- Insufficient trading permissions
- Expired API keys
- Insufficient balance for hedging

[Troubleshooting →](../troubleshooting/api-key-issues.md)

## Platform-Specific Guides

### Hyperliquid

- [Setting Up Trading Accounts](hyperliquid-keys.md)
- [Understanding Subaccounts](subaccounts.md)
- [Setting Permissions](permissions.md)

### Uniswap V3

- [Finding NFT IDs](../position-setup/uniswap-v3-nft-id.md)
- [Wallet Connection](../position-setup/uniswap-v3-nft-id.md#wallet-address)

## Quick Reference

### Hyperliquid Trading Account Checklist

- [ ] Generated from Hyperliquid dashboard
- [ ] Trade-only permissions (trading enabled, withdrawals/transfers disabled)
- [ ] Correct account type selected (Master or Sub-account)
- [ ] API private key copied securely
- [ ] Wallet address noted
- [ ] Account tested and balance verified
- [ ] Old keys deleted after rotation

### Security Checklist

- [ ] Private keys stored in password manager
- [ ] Withdrawals and transfers disabled
- [ ] Unique trading account per LP position
- [ ] Keys rotated regularly (every 3-6 months)
- [ ] Unused trading accounts deleted
- [ ] Never shared publicly

## Need Help?

- **[Hyperliquid Setup Guide](hyperliquid-keys.md)** - Detailed walkthrough
- **[Trading Account Issues](../troubleshooting/api-key-issues.md)** - Fix common issues
- **[Security Questions](../security/api-key-security.md)** - Learn about our security
- **[Contact Support](../troubleshooting/contact-support.md)** - Get personalized help

---

**Next:** [Set Up Hyperliquid Trading Account →](hyperliquid-keys.md)
