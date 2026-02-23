# API Keys & Authentication

API keys are how WhisperHedge securely connects to your trading platforms to monitor your LP positions. This section covers everything you need to know about managing API keys safely and effectively.

## Overview

WhisperHedge requires API keys to:

- ✅ Read your position data
- ✅ Calculate impermanent loss
- ✅ Monitor position health
- ✅ Track fee earnings

We **never** require trading permissions. All API keys should be **read-only**.

## Supported Platforms

### Hyperliquid

For Hyperliquid HLP positions, you'll need:

- API Key (public)
- API Secret (private)
- Subaccount name (if applicable)

[Get Hyperliquid API Keys →](hyperliquid-keys.md)

### Uniswap V3

For Uniswap V3 positions, you'll need:

- NFT Token ID
- Wallet address

[Find Your NFT ID →](../position-setup/uniswap-v3-nft-id.md)

## Key Concepts

### Read-Only vs Trading Permissions

**Read-Only (Required)**
- View positions
- Check balances
- Read transaction history
- Calculate metrics

**Trading (NEVER Required)**
- Place orders
- Cancel orders
- Transfer funds
- Modify positions

!!! danger "Never Grant Trading Permissions"
    WhisperHedge only needs read access. Never create API keys with trading, withdrawal, or transfer permissions.

### One Key Per Position

WhisperHedge requires a unique API key for each position you track. This is a security feature that:

- Limits exposure if a key is compromised
- Allows granular permission control
- Enables easy position removal
- Improves tracking accuracy

[Learn more about this requirement →](one-key-per-position.md)

### Subaccounts

Hyperliquid supports subaccounts, which are separate trading accounts under your main account. Each subaccount:

- Has its own API keys
- Maintains separate positions
- Requires separate tracking

[Understanding subaccounts →](subaccounts.md)

## Security Best Practices

### Creating Keys

- ✅ Use **read-only** permissions only
- ✅ Create separate keys for each position
- ✅ Use descriptive names/labels
- ✅ Record key creation dates

### Storing Keys

- ✅ Store keys securely (password manager)
- ✅ Never share keys publicly
- ✅ Don't commit keys to git repositories
- ✅ Keep API secrets private

### Managing Keys

- ✅ Rotate keys every 3-6 months
- ✅ Delete unused keys immediately
- ✅ Monitor key usage
- ✅ Revoke compromised keys instantly

### In WhisperHedge

- ✅ Keys are encrypted at rest
- ✅ Transmitted over HTTPS only
- ✅ Never logged or exposed
- ✅ Deleted when position is removed

[Full security guide →](../security/api-key-security.md)

## Common Tasks

### Adding Your First API Key

1. Generate a read-only key on your platform
2. Copy the API key and secret
3. Add a new position in WhisperHedge
4. Paste the credentials
5. Verify and save

[Step-by-step guide →](hyperliquid-keys.md)

### Rotating API Keys

1. Generate a new read-only key
2. Update the position in WhisperHedge
3. Verify the new key works
4. Delete the old key from your platform

[Rotation guide →](rotating-keys.md)

### Troubleshooting Key Issues

Common problems and solutions:

- Invalid key format
- Insufficient permissions
- Expired keys
- Rate limiting

[Troubleshooting →](../troubleshooting/api-key-issues.md)

## Platform-Specific Guides

### Hyperliquid

- [Extracting API Keys](hyperliquid-keys.md)
- [Understanding Subaccounts](subaccounts.md)
- [Setting Permissions](permissions.md)

### Uniswap V3

- [Finding NFT IDs](../position-setup/uniswap-v3-nft-id.md)
- [Wallet Connection](../position-setup/uniswap-v3-nft-id.md#wallet-address)

## Quick Reference

### Hyperliquid API Key Checklist

- [ ] Generated from Hyperliquid dashboard
- [ ] Read-only permissions only
- [ ] Correct subaccount (if applicable)
- [ ] Both key and secret copied
- [ ] Key tested and verified
- [ ] Old keys deleted after rotation

### Security Checklist

- [ ] Keys stored in password manager
- [ ] No trading permissions granted
- [ ] Unique key per position
- [ ] Keys rotated regularly
- [ ] Unused keys deleted
- [ ] Never shared publicly

## Need Help?

- **[Hyperliquid Key Extraction](hyperliquid-keys.md)** - Detailed walkthrough
- **[Permission Errors](../troubleshooting/api-key-issues.md)** - Fix common issues
- **[Security Questions](../security/api-key-security.md)** - Learn about our security
- **[Contact Support](../troubleshooting/contact-support.md)** - Get personalized help

---

**Next:** [Extract Hyperliquid API Keys →](hyperliquid-keys.md)
