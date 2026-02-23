# Security Overview

Security is our top priority at WhisperHedge. This section explains how we protect your data and API keys.

## Core Security Principles

### 1. Read-Only Access
We only require read-only API keys. We can never:
- Execute trades
- Transfer funds
- Modify your positions
- Access your private keys

[Learn more →](read-only-permissions.md)

### 2. Data Encryption
- API keys encrypted at rest
- All data transmitted over HTTPS
- Secure database storage
- No plain text secrets

[Learn more →](api-key-security.md)

### 3. Minimal Data Collection
We only collect what's necessary:
- Email address
- Position data (from APIs)
- Usage metrics

We never collect:
- Passwords (passwordless auth)
- Private keys
- Trading history beyond positions
- Personal information

[Learn more →](what-we-store.md)

### 4. Passwordless Authentication
- Magic link authentication
- No password database to breach
- Time-limited access tokens
- Secure PKCE flow

[Learn more →](account-security.md)

## What We Protect

### Your API Keys
- Encrypted storage
- Secure transmission
- Automatic deletion
- Never logged or exposed

[API Key Security →](api-key-security.md)

### Your Data
- Position information
- Performance metrics
- Email address
- Account settings

[Data Privacy →](data-privacy.md)

### Your Account
- Magic link authentication
- Session management
- Access control
- Audit logging

[Account Security →](account-security.md)

## Security Features

- ✅ HTTPS everywhere
- ✅ Encrypted API key storage
- ✅ Read-only permissions only
- ✅ Passwordless authentication
- ✅ Regular security audits
- ✅ Automatic key deletion
- ✅ Session timeout
- ✅ Rate limiting

## Best Practices

### For You

- ✅ Use read-only API keys
- ✅ Rotate keys regularly
- ✅ Secure your email account
- ✅ Enable 2FA on email
- ✅ Don't share magic links
- ✅ Delete unused positions

### For Us

- ✅ Encrypt all sensitive data
- ✅ Regular security audits
- ✅ Minimal data collection
- ✅ Secure infrastructure
- ✅ Incident response plan
- ✅ Transparent practices

## Related Topics

- [API Key Security](api-key-security.md)
- [Read-Only Permissions](read-only-permissions.md)
- [Data Privacy](data-privacy.md)
- [Account Security](account-security.md)
- [What We Store](what-we-store.md)
