# Rotating API Keys

Regular API key rotation is a security best practice. This guide shows you how to safely rotate your WhisperHedge API keys without disrupting position tracking.

## Why Rotate Keys?

### Security Benefits

**Limit Exposure Window**

Even if a key is compromised, regular rotation limits the time an attacker can use it.

**Detect Breaches**

If old keys continue to be used after rotation, you know there's unauthorized access.

**Compliance**

Many security standards require periodic key rotation.

**Fresh Start**

Rotating keys ensures clean separation between time periods for auditing.

## Rotation Schedule

### Recommended Frequency

**High-Value Positions:**
- Rotate every 1-3 months
- More frequent if handling large amounts
- After any security concern

**Medium-Value Positions:**
- Rotate every 3-6 months
- Standard security practice
- Balances security and convenience

**Low-Value Positions:**
- Rotate every 6-12 months
- Minimum recommended frequency
- Still important for security

### Triggers for Immediate Rotation

Rotate immediately if:

- 🚨 Suspected key compromise
- 🚨 Employee/team member leaves
- 🚨 Security breach at platform
- 🚨 Key accidentally exposed (git, email, etc.)
- 🚨 Unusual activity detected
- 🚨 Platform recommends rotation

## Rotation Process

### Step-by-Step Guide

#### Step 1: Create New API Key

1. Log into your trading platform (e.g., Hyperliquid)
2. Navigate to API key management
3. Create a new API key with:
   - Read-only permissions
   - Same subaccount as old key
   - Descriptive name (include date)
4. Save the new key and secret securely

**Example naming:**
```
Old: WhisperHedge-ETH-USDC-2024-01
New: WhisperHedge-ETH-USDC-2024-04
```

#### Step 2: Update WhisperHedge

1. Go to WhisperHedge dashboard
2. Find the position using the old key
3. Click "Edit" or "Update API Key"
4. Enter the new API key and secret
5. Click "Verify" to test the connection
6. Save the changes

!!! tip "Test First"
    Always verify the new key works before deleting the old one.

#### Step 3: Verify New Key Works

1. Check that position data loads
2. Manually refresh the position
3. Verify all metrics display correctly
4. Wait 5-10 minutes for full sync

#### Step 4: Delete Old Key

1. Return to your trading platform
2. Find the old API key
3. Delete or revoke it
4. Confirm deletion

!!! warning "Don't Delete Too Soon"
    Wait until you've confirmed the new key works before deleting the old one.

#### Step 5: Update Records

1. Update your password manager
2. Note rotation date in your records
3. Set reminder for next rotation
4. Document any issues encountered

### Quick Rotation Checklist

- [ ] Create new API key (read-only)
- [ ] Save new key securely
- [ ] Update key in WhisperHedge
- [ ] Verify position data loads
- [ ] Test manual refresh
- [ ] Wait 5-10 minutes
- [ ] Delete old key from platform
- [ ] Update password manager
- [ ] Record rotation date
- [ ] Set next rotation reminder

## Rotation Strategies

### Staggered Rotation

If you have multiple positions, don't rotate all keys at once:

**Week 1:** Rotate positions 1-3
**Week 2:** Rotate positions 4-6  
**Week 3:** Rotate positions 7-9

**Benefits:**
- Reduces workload
- Easier to troubleshoot issues
- Less disruptive
- Spreads out risk

### Batch Rotation

Rotate all keys at once:

**Benefits:**
- Gets it done quickly
- Consistent rotation dates
- Easier to remember

**Drawbacks:**
- More time-consuming
- Higher risk of errors
- All positions affected if issues

### Event-Based Rotation

Rotate keys when specific events occur:

- Platform security update
- Quarterly security review
- Team member changes
- After travel/conferences
- Regulatory audit

## Automation & Reminders

### Calendar Reminders

Set recurring calendar events:

```
Every 3 months:
"Rotate WhisperHedge API Keys - Positions 1-5"

Every 6 months:
"Rotate WhisperHedge API Keys - All Positions"
```

### Password Manager

Many password managers support:
- Expiration dates on entries
- Automatic rotation reminders
- Audit logs
- Security scores

### Spreadsheet Tracking

Track rotation in a spreadsheet:

| Position | Current Key | Created | Last Rotated | Next Rotation |
|----------|-------------|---------|--------------|---------------|
| ETH/USDC | WH-ETH-04 | 2024-04-01 | 2024-04-01 | 2024-07-01 |
| BTC/USDC | WH-BTC-03 | 2024-03-15 | 2024-03-15 | 2024-06-15 |

## Troubleshooting Rotation

### New Key Not Working

**Symptoms:**
- "Invalid API Key" error
- Position not updating
- Permission denied

**Solutions:**
1. Verify key was copied correctly (no spaces)
2. Check permissions are read-only
3. Confirm correct subaccount
4. Try regenerating the key
5. Revert to old key temporarily

### Position Data Lost

**Symptoms:**
- Historical data missing
- Metrics reset to zero
- Charts empty

**Solutions:**
1. Wait 10-15 minutes for resync
2. Manually refresh position
3. Check if position ID changed
4. Contact support if persists

### Old Key Still Active

**Symptoms:**
- Old key works after deletion
- Platform shows key as active

**Solutions:**
1. Verify deletion in platform
2. Clear browser cache
3. Log out and back in
4. Check if key was actually deleted

## Best Practices

### Before Rotation

- ✅ Choose low-activity time
- ✅ Have new key ready
- ✅ Backup current configuration
- ✅ Notify team if applicable

### During Rotation

- ✅ Test new key thoroughly
- ✅ Keep old key active until verified
- ✅ Document any issues
- ✅ Update one position at a time

### After Rotation

- ✅ Verify all positions working
- ✅ Delete old keys promptly
- ✅ Update documentation
- ✅ Set next rotation reminder

## Emergency Rotation

### Suspected Compromise

If you suspect a key is compromised:

1. **Immediately** delete the key from platform
2. Create new key
3. Update WhisperHedge
4. Review platform security logs
5. Check for unauthorized activity
6. Change password if needed
7. Enable 2FA if not already active

### Mass Rotation

If you need to rotate all keys urgently:

1. **Prioritize** by position value (high to low)
2. **Batch process** in groups of 3-5
3. **Verify** each batch before continuing
4. **Document** any issues
5. **Review** security logs after completion

## Rotation Records

### What to Track

Keep records of:
- Key creation dates
- Rotation dates
- Reason for rotation
- Any issues encountered
- Time taken
- Platform used

### Sample Record

```
Position: ETH/USDC HLP
Old Key: WH-ETH-2024-01
New Key: WH-ETH-2024-04
Rotation Date: 2024-04-01
Reason: Scheduled quarterly rotation
Issues: None
Time Taken: 5 minutes
Next Rotation: 2024-07-01
```

## Multiple Position Rotation

### Efficient Process

For rotating 10+ positions:

1. **Prepare:** Create all new keys first
2. **Organize:** List positions by priority
3. **Execute:** Update 3-5 at a time
4. **Verify:** Test each batch
5. **Clean up:** Delete old keys in batches
6. **Document:** Record all changes

### Time Estimates

- Single position: 5-10 minutes
- 5 positions: 30-45 minutes
- 10 positions: 1-1.5 hours
- 20+ positions: 2-3 hours

## Related Topics

- **[Hyperliquid API Keys](hyperliquid-keys.md)** - Creating new keys
- **[One Key Per Position](one-key-per-position.md)** - Why separate keys
- **[API Key Security](../security/api-key-security.md)** - Security best practices
- **[Troubleshooting](../troubleshooting/api-key-issues.md)** - Fix common issues

---

**Next:** [Position Setup Overview →](../position-setup/index.md)
