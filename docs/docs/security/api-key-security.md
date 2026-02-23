# API Key Security

How WhisperHedge protects your API keys and keeps your trading accounts secure.

## How We Handle API Keys

### Encryption at Rest

All API keys are encrypted in our database using:
- AES-256 encryption
- Unique encryption keys per environment
- Secure key management
- No plain text storage

### Encryption in Transit

API keys are transmitted securely:
- HTTPS/TLS 1.3 only
- Certificate pinning
- No HTTP fallback
- Secure WebSocket connections

### Access Control

API keys are protected by:
- Database-level encryption
- Row-level security (RLS)
- User-specific access only
- No cross-user access

### Automatic Deletion

Keys are deleted when:
- You remove a position
- You delete your account
- Position is inactive for 90 days (with warning)

## What We Never Do

### Never Store Plain Text

- ❌ No plain text API keys
- ❌ No plain text secrets
- ❌ No logging of credentials
- ❌ No debug output with keys

### Never Share Keys

- ❌ No employee access to raw keys
- ❌ No third-party sharing
- ❌ No analytics tracking
- ❌ No external services

### Never Use for Trading

- ❌ No trade execution
- ❌ No fund transfers
- ❌ No position modifications
- ❌ No account changes

## Security Measures

### Infrastructure

**Database Security:**
- Encrypted at rest
- Encrypted in transit
- Regular backups (encrypted)
- Access logging

**Application Security:**
- Secure coding practices
- Regular security audits
- Dependency scanning
- Vulnerability patching

**Network Security:**
- Firewall protection
- DDoS mitigation
- Rate limiting
- IP filtering (optional)

### Monitoring

**We Monitor For:**
- Unusual API usage patterns
- Failed authentication attempts
- Suspicious access patterns
- Rate limit violations

**Automated Alerts:**
- Security incidents
- Unusual activity
- System anomalies
- Failed access attempts

## Your Responsibilities

### Creating Keys

- ✅ Use read-only permissions only
- ✅ Create unique key per position
- ✅ Use descriptive names
- ✅ Store keys securely

### Managing Keys

- ✅ Rotate keys every 3-6 months
- ✅ Delete unused keys immediately
- ✅ Monitor key usage
- ✅ Report suspicious activity

### Storing Keys

- ✅ Use password manager
- ✅ Keep secrets encrypted
- ✅ Never commit to git
- ✅ Don't share publicly

## Security Incidents

### If You Suspect Compromise

1. **Immediately** delete the key from your trading platform
2. Remove the position from WhisperHedge
3. Generate new API key
4. Re-add position with new key
5. Review platform security logs
6. Contact support if needed

### If We Detect Issues

We will:
1. Immediately notify you via email
2. Temporarily disable affected positions
3. Provide incident details
4. Guide you through remediation
5. Investigate root cause

## Compliance

### Standards We Follow

- OWASP Top 10 security practices
- SOC 2 Type II principles
- GDPR data protection
- Industry best practices

### Regular Audits

- Quarterly security reviews
- Annual penetration testing
- Continuous vulnerability scanning
- Third-party security assessments

## Technical Details

### Encryption Specifications

**At Rest:**
- Algorithm: AES-256-GCM
- Key derivation: PBKDF2
- Unique keys per record
- Secure key rotation

**In Transit:**
- TLS 1.3
- Perfect forward secrecy
- Strong cipher suites
- Certificate validation

### Access Patterns

**Read Operations:**
- Decrypt only when needed
- Minimal exposure time
- Secure memory handling
- Immediate cleanup

**Write Operations:**
- Encrypt before storage
- Validate before saving
- Audit logging
- Rollback capability

## Comparison with Other Platforms

| Feature | WhisperHedge | Typical Platform |
|---------|--------------|------------------|
| Encryption at rest | ✅ AES-256 | ⚠️ Varies |
| Read-only requirement | ✅ Enforced | ❌ Optional |
| Automatic deletion | ✅ Yes | ❌ Manual |
| One key per position | ✅ Required | ❌ Not required |
| Key rotation reminders | ✅ Yes | ❌ No |

## FAQ

**Q: Can WhisperHedge employees see my API keys?**
A: No. Keys are encrypted and employees have no access to decryption keys.

**Q: What if WhisperHedge is hacked?**
A: Keys are encrypted. Attackers would need both database access and encryption keys.

**Q: How long are keys stored?**
A: Only while position is active. Deleted immediately when position is removed.

**Q: Can I audit key usage?**
A: Yes, we provide access logs showing when keys were used.

## Related Topics

- [Read-Only Permissions](read-only-permissions.md)
- [API Key Permissions](../api-keys/permissions.md)
- [Rotating Keys](../api-keys/rotating-keys.md)
- [Data Privacy](data-privacy.md)
