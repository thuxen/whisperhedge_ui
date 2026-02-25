# One Trading Account Per Position

WhisperHedge requires a dedicated trading account for each position you track. This page explains why this requirement exists and how to manage multiple trading accounts effectively.

## The Requirement

**Each LP position must have its own dedicated trading account.**

You cannot:
- ❌ Use the same trading account for multiple positions
- ❌ Share trading accounts between positions
- ❌ Reuse trading accounts after deleting a position

You must:
- ✅ Create a new trading account for each position
- ✅ Use unique trading accounts per position
- ✅ Delete trading accounts when removing positions

## Why This Requirement Exists

### 1. Security Isolation

**Principle of Least Privilege**

Each trading account should have access to only what it needs. By using separate trading accounts:

- Compromised credentials affects only one position
- Easier to identify which position had the breach
- Simpler to revoke access to specific positions
- Reduced blast radius of security incidents

**Example Scenario:**

```
❌ Bad: One trading account for all positions
If key is compromised → All positions at risk

✅ Good: One trading account per position
If key is compromised → Only that position at risk
```

### 2. Granular Control

**Position-Level Management**

Separate trading accounts allow you to:

- Remove individual positions without affecting others
- Rotate keys for specific positions
- Grant temporary access to specific positions
- Audit access per position

### 3. Accurate Tracking

**Data Integrity**

Using separate trading accounts ensures:

- Clear mapping between keys and positions
- No confusion about which data belongs where
- Easier troubleshooting
- Better audit trails

### 4. Compliance & Best Practices

**Industry Standards**

This approach aligns with:

- API security best practices
- Principle of least privilege
- Defense in depth strategy
- Regulatory compliance requirements

## How It Works

### Adding Multiple Positions

**Scenario:** You have 3 HLP positions to track

**Step 1:** Create 3 separate API keys in Hyperliquid

```
Position 1: ETH/USDC
└── API Key 1 (read-only)

Position 2: BTC/USDC  
└── API Key 2 (read-only)

Position 3: SOL/USDC
└── API Key 3 (read-only)
```

**Step 2:** Add each position to WhisperHedge with its unique key

```
WhisperHedge Dashboard:
├── Position 1: ETH/USDC → Uses API Key 1
├── Position 2: BTC/USDC → Uses API Key 2
└── Position 3: SOL/USDC → Uses API Key 3
```

### Managing Multiple Keys

**Organization Tips:**

Use descriptive names when creating keys:

```
Hyperliquid API Keys:
├── "WhisperHedge - ETH/USDC Position"
├── "WhisperHedge - BTC/USDC Position"
└── "WhisperHedge - SOL/USDC Position"
```

**Tracking Keys:**

Keep a record (in password manager):

| Position | API Key Name | Created | Last Rotated |
|----------|--------------|---------|--------------|
| ETH/USDC | WH-ETH-001 | 2024-01-15 | 2024-01-15 |
| BTC/USDC | WH-BTC-001 | 2024-01-20 | 2024-01-20 |
| SOL/USDC | WH-SOL-001 | 2024-02-01 | 2024-02-01 |

## Common Questions

### "Can't I just use one key for everything?"

**No.** While technically some platforms might allow this, WhisperHedge enforces the one-key-per-position rule for security and data integrity.

### "This seems like a lot of work"

**It's worth it.** The security benefits far outweigh the minor inconvenience:

- 5 minutes to create a key
- Protects your entire portfolio
- Industry best practice
- Peace of mind

### "What if I have 10 positions?"

**Create 10 keys.** Yes, it takes more time initially, but:

- Each key is quick to create (1-2 minutes)
- You only do it once per position
- Security scales with your portfolio
- Easier to manage than dealing with a breach

### "Can I reuse a key after deleting a position?"

**Not recommended.** Best practice:

1. Delete the position from WhisperHedge
2. Delete the API key from Hyperliquid
3. Create a fresh key for new positions

This ensures clean separation and prevents confusion.

## Practical Examples

### Example 1: Adding 3 Positions

**Scenario:** You want to track 3 HLP positions

**Process:**

1. **Create API Key 1** in Hyperliquid
   - Name: "WhisperHedge - Position 1"
   - Permissions: Read-only
   - Subaccount: "Main" (or specific subaccount)

2. **Add Position 1** in WhisperHedge
   - Protocol: Hyperliquid
   - API Key: [key1]
   - API Secret: [secret1]

3. **Repeat for Position 2**
   - Create new API Key 2
   - Add Position 2 with Key 2

4. **Repeat for Position 3**
   - Create new API Key 3
   - Add Position 3 with Key 3

### Example 2: Replacing a Position

**Scenario:** You close Position 1 and open a new position

**Process:**

1. **Remove Position 1** from WhisperHedge
2. **Delete API Key 1** from Hyperliquid
3. **Create new API Key 4** for the new position
4. **Add new position** with Key 4

Don't reuse Key 1 - create a fresh key.

### Example 3: Multiple Subaccounts

**Scenario:** 2 positions in Subaccount A, 1 in Subaccount B

**Process:**

1. **Create Key 1** for Subaccount A, Position 1
2. **Create Key 2** for Subaccount A, Position 2
3. **Create Key 3** for Subaccount B, Position 1

Each position gets its own key, even within the same subaccount.

## Security Benefits in Detail

### Breach Containment

**Scenario:** API Key 2 is compromised

**With separate trading accounts:**
- Only Position 2 data is exposed
- Positions 1 and 3 remain secure
- Revoke only Key 2
- Other positions unaffected

**With shared key:**
- All positions exposed
- Must revoke key affecting all positions
- Must recreate all positions
- Significant disruption

### Audit Trail

**With separate trading accounts:**

```
2024-02-15: Key 1 accessed Position 1 data
2024-02-15: Key 2 accessed Position 2 data
2024-02-15: Key 3 accessed Position 3 data
```

Clear, traceable, auditable.

**With shared key:**

```
2024-02-15: Key 1 accessed... something?
```

Unclear which position was accessed.

### Rotation Strategy

**With separate trading accounts:**

- Rotate keys on different schedules
- High-value positions: rotate monthly
- Low-value positions: rotate quarterly
- Stagger rotations to reduce work

**With shared key:**

- Must rotate all at once
- All positions affected
- More disruptive
- Higher risk of errors

## Best Practices

### Creation

- ✅ Create keys as needed (don't pre-create)
- ✅ Use descriptive names
- ✅ Document which position each key is for
- ✅ Store keys securely immediately

### Management

- ✅ Track keys in password manager
- ✅ Note creation dates
- ✅ Set rotation reminders
- ✅ Review keys monthly

### Deletion

- ✅ Delete trading accounts when removing positions
- ✅ Don't leave orphaned keys
- ✅ Clean up regularly
- ✅ Audit key list quarterly

### Organization

- ✅ Consistent naming convention
- ✅ Group by strategy or subaccount
- ✅ Tag keys with metadata
- ✅ Keep records up to date

## Troubleshooting

### "I accidentally used the same key twice"

**Solution:**

1. Remove one of the positions
2. Create a new trading account
3. Re-add the position with the new key

### "I lost track of which key is for which position"

**Prevention:**

- Use descriptive names when creating keys
- Keep a spreadsheet or note
- Use password manager tags/categories

**Recovery:**

1. List all positions in WhisperHedge
2. List all API keys in Hyperliquid
3. Match by creation date or name
4. Update documentation

### "This is too many keys to manage"

**Solutions:**

- Use a password manager (highly recommended)
- Create keys only for active positions
- Close positions you're not actively monitoring
- Consider if you need to track all positions

## Tools & Tips

### Password Managers

Recommended for storing API keys:

- **1Password** - Excellent for API credentials
- **Bitwarden** - Open source, affordable
- **LastPass** - Popular choice
- **KeePass** - Offline option

### Naming Convention

Suggested format:

```
WhisperHedge-[Protocol]-[Pair]-[Date]

Examples:
- WhisperHedge-HL-ETHUSDC-2024-02
- WhisperHedge-HL-BTCUSDC-2024-02
- WhisperHedge-UNI-Position1-2024-02
```

### Spreadsheet Template

Track your keys:

| Position | Protocol | Pair | API Key Name | Created | Rotated | Subaccount |
|----------|----------|------|--------------|---------|---------|------------|
| Pos 1 | Hyperliquid | ETH/USDC | WH-HL-ETH-01 | 2024-02-01 | 2024-02-01 | Main |
| Pos 2 | Hyperliquid | BTC/USDC | WH-HL-BTC-01 | 2024-02-05 | 2024-02-05 | Conservative |

## Related Topics

- **[Hyperliquid API Keys](hyperliquid-keys.md)** - How to create keys
- **[Rotating Keys](rotating-keys.md)** - How to update keys
- **[API Key Security](../security/api-key-security.md)** - Security deep dive
- **[Subaccounts](subaccounts.md)** - Managing multiple subaccounts

---

**Next:** [Rotating API Keys →](rotating-keys.md)
