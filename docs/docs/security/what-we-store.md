# What We Store

Transparency about the data we collect and store.

## Data We Store

### Account Data
- **Email address** - For authentication and notifications
- **Account creation date** - For record keeping
- **Plan tier** - Free, Pro, or Premium
- **Notification preferences** - Email settings

### Position Data
- **API keys** (encrypted) - For Hyperliquid positions
- **NFT IDs** - For Uniswap V3 positions
- **Position values** - Historical tracking
- **Performance metrics** - IL, fees, health scores

### Usage Data
- **Login timestamps** - Security monitoring
- **Feature usage** - Product improvement
- **Error logs** - Debugging (no sensitive data)

## Data We Don't Store

### Never Stored
- ❌ Passwords (passwordless system)
- ❌ Private keys
- ❌ Trading history (beyond tracked positions)
- ❌ Personal information (name, address, phone)
- ❌ Payment details (handled by Stripe)

### Automatically Deleted
- Magic link tokens (after use or expiration)
- Session tokens (after logout or timeout)
- API keys (when position removed)
- Position data (when position deleted)

## Data Retention

### Active Accounts
- Position data: Retained while position is active
- Historical data: Up to 1 year
- Account data: While account is active

### Deleted Accounts
- All data deleted within 30 days
- Backups purged within 90 days
- No data retention after deletion

## Data Location

- **Primary:** US-based servers
- **Backups:** Encrypted, US-based
- **CDN:** Global (for static assets only)

## Third-Party Services

### Supabase (Database & Auth)
- Stores encrypted data
- Handles authentication
- SOC 2 Type II certified

### Stripe (Payments)
- Processes payments only
- We don't store card details
- PCI DSS compliant

### Analytics
- Google Analytics (anonymized)
- Mixpanel (usage patterns)
- No PII shared

## Your Data Rights

- **Access:** Request copy of your data
- **Export:** Download your data
- **Delete:** Remove your account and all data
- **Correct:** Update incorrect information

[Contact support](../troubleshooting/contact-support.md) to exercise these rights.

## Related Topics

- [Data Privacy](data-privacy.md)
- [API Key Security](api-key-security.md)
- [Account Security](account-security.md)
