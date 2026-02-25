# Extracting Hyperliquid API Keys

This guide shows you how to generate read-only API keys from your Hyperliquid account to use with WhisperHedge.

## Prerequisites

- Active Hyperliquid account
- Access to Hyperliquid web interface
- Understanding of which subaccount to use (if applicable)

## Step-by-Step Guide

### Step 1: Log Into Hyperliquid

1. Go to [app.hyperliquid.xyz](https://app.hyperliquid.xyz)
2. Connect your wallet
3. Ensure you're on the correct network (Arbitrum)

### Step 2: Navigate to API Settings

1. Click on your **profile/account icon** (top right)
2. Select **"API Keys"** or **"Settings"**
3. Navigate to the **API Management** section

!!! info "Location May Vary"
    The exact location of API settings may change with Hyperliquid UI updates. Look for "API", "Developer", or "Settings" sections.

### Step 3: Create New API Key

1. Click **"Create New API Key"** or **"Generate Key"**
2. You'll be prompted to set permissions

### Step 4: Set Read-Only Permissions

**CRITICAL:** Only enable read permissions:

✅ **Enable These:**
- Read account data
- View positions
- View orders
- View balances
- View transaction history

❌ **NEVER Enable These:**
- Place orders
- Cancel orders
- Transfer funds
- Withdraw
- Modify account settings

!!! danger "Trading Permissions"
    Never grant trading, withdrawal, or transfer permissions to API keys used with WhisperHedge. We only need read access.

### Step 5: Select Subaccount (If Applicable)

If you use Hyperliquid subaccounts:

1. Choose the specific subaccount for this key
2. Or select "Main Account" if not using subaccounts
3. Remember which subaccount you selected

[Learn more about subaccounts →](subaccounts.md)

### Step 6: Name Your Key

Give your API key a descriptive name:

- ✅ Good: "WhisperHedge - Main HLP Position"
- ✅ Good: "WhisperHedge - Subaccount A - ETH/USDC"
- ❌ Bad: "Key1"
- ❌ Bad: "Test"

This helps you manage multiple keys later.

### Step 7: Generate and Copy

1. Click **"Generate"** or **"Create"**
2. **Copy the API Key** - This is your public identifier
3. **Copy the API Secret** - This is your private key

!!! warning "Save Immediately"
    The API Secret is usually only shown once. Save it immediately in a secure location (password manager). If you lose it, you'll need to generate a new key.

### Step 8: Store Securely

Store both the API Key and Secret in:

- Password manager (recommended)
- Encrypted notes
- Secure vault

**Never:**
- Share them publicly
- Commit them to git
- Store in plain text files
- Email them to yourself

### Step 9: Add to WhisperHedge

1. Go to your WhisperHedge dashboard
2. Click **"+ Add Position"**
3. Select **"Hyperliquid"**
4. Paste your **API Key**
5. Paste your **API Secret**
6. Enter **Subaccount name** (if applicable)
7. Click **"Verify Position"**

!!! tip "One Key Per Position"
    Remember: Each position needs its own unique API key. If you have multiple HLP positions, create a separate key for each one. [Learn why →](one-key-per-position.md)

## Verification

After adding the key to WhisperHedge, you should see:

- ✅ Position data loads successfully
- ✅ Current value displays
- ✅ Token balances shown
- ✅ No error messages

If you see errors, check:

- Key permissions are correct (read-only)
- Subaccount name matches (if using subaccounts)
- No typos in key or secret
- Key hasn't been deleted from Hyperliquid

## Managing Multiple Keys

### For Multiple Positions

If you have multiple HLP positions:

1. Create a separate API key for each position
2. Use descriptive names to track them
3. Note which key corresponds to which position
4. Delete keys when positions are closed

### For Multiple Subaccounts

If you use multiple subaccounts:

1. Create keys specific to each subaccount
2. Clearly label which subaccount each key is for
3. Track positions separately per subaccount

[Understanding subaccounts →](subaccounts.md)

## Security Considerations

### Key Permissions

Always verify your key has:

- ✅ Read-only access
- ✅ No trading permissions
- ✅ No withdrawal permissions
- ✅ No transfer permissions

### Key Rotation

Rotate your API keys periodically:

- Every 3-6 months (recommended)
- After any security concern
- When removing team members
- If key may have been exposed

[How to rotate keys →](rotating-keys.md)

### Compromised Keys

If you suspect a key is compromised:

1. **Immediately** delete it from Hyperliquid
2. Remove the position from WhisperHedge
3. Generate a new key
4. Re-add the position with the new key

## Troubleshooting

### "Invalid API Key"

**Possible causes:**
- Key was copied incorrectly (extra spaces, missing characters)
- Key was deleted from Hyperliquid
- Wrong subaccount selected
- Key permissions insufficient

**Solutions:**
- Copy the key again carefully
- Verify key exists in Hyperliquid
- Check subaccount name matches
- Regenerate key with correct permissions

### "Permission Denied"

**Cause:** API key doesn't have read permissions

**Solution:**
1. Delete the current key
2. Create a new key
3. Ensure read permissions are enabled
4. Try again

### "Subaccount Not Found"

**Cause:** Subaccount name doesn't match

**Solution:**
- Verify exact subaccount name in Hyperliquid
- Check for typos, spaces, capitalization
- Use "Main Account" if not using subaccounts

[More troubleshooting →](../troubleshooting/api-key-issues.md)

## Best Practices

### Creation

- ✅ Create keys only when needed
- ✅ Use descriptive names
- ✅ Document which position each key is for
- ✅ Set read-only permissions

### Storage

- ✅ Use a password manager
- ✅ Keep secrets encrypted
- ✅ Never share keys
- ✅ Back up securely

### Maintenance

- ✅ Review keys monthly
- ✅ Delete unused keys
- ✅ Rotate keys regularly
- ✅ Monitor for suspicious activity

### In WhisperHedge

- ✅ One key per position
- ✅ Remove keys when closing positions
- ✅ Update keys after rotation
- ✅ Verify keys work after adding

## Related Topics

- **[Subaccounts](subaccounts.md)** - Understanding Hyperliquid subaccounts
- **[Permissions](permissions.md)** - Detailed permission breakdown
- **[One Key Per Position](one-key-per-position.md)** - Why this requirement exists
- **[Rotating Keys](rotating-keys.md)** - How to update keys safely
- **[API Key Security](../security/api-key-security.md)** - Security deep dive

---

**Next:** [Understanding Subaccounts →](subaccounts.md)
