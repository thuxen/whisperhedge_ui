# API Key Schema Standardization

## Overview
This document explains the standardization of API key column naming in the database schema to support multiple exchanges and maintain consistency.

## Changes Made

### 1. Column Naming Convention
**Standardized on:** `hl_api_key_id`

**Rationale:**
- The `hl_` prefix distinguishes this as the Hyperliquid API key reference
- Keeps the door open for future multi-exchange support (e.g., `binance_api_key_id`, `dydx_api_key_id`)
- Already exists in the database schema (`SUPABASE_SETUP.sql`)
- Avoids confusion with the generic `api_key` field in `user_api_keys` table

### 2. Multi-Exchange Support

The schema is already designed for multiple exchanges:

#### `user_api_keys` Table
```sql
CREATE TABLE user_api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    account_name VARCHAR(100),
    exchange VARCHAR(50) DEFAULT 'hyperliquid',  -- ✓ Supports any exchange
    api_key TEXT,
    api_secret TEXT,
    wallet_address TEXT,
    ...
);
```

**Supported exchanges:**
- `hyperliquid` (current)
- `binance` (future)
- `dydx` (future)
- `bybit` (future)
- Any other exchange can be added without schema changes

#### `position_configs` Table
```sql
CREATE TABLE position_configs (
    ...
    hl_api_key_id UUID REFERENCES user_api_keys(id),  -- For Hyperliquid hedging
    ...
);
```

**Future expansion:**
When adding new exchanges, simply add new columns:
```sql
ALTER TABLE position_configs ADD COLUMN binance_api_key_id UUID REFERENCES user_api_keys(id);
ALTER TABLE position_configs ADD COLUMN dydx_api_key_id UUID REFERENCES user_api_keys(id);
```

### 3. Migration Path

#### For Existing Deployments
Run `STANDARDIZE_API_KEY_COLUMN.sql` which:
1. Ensures `hl_api_key_id` column exists
2. Migrates data from old `hedge_wallet_id` column (if it exists)
3. Drops the old `hedge_wallet_id` column
4. Adds unique constraint for 1-to-1 API key limitation

#### For New Deployments
Just run `SUPABASE_SETUP.sql` - the schema is already correct.

### 4. Code Changes

All code now consistently uses `hl_api_key_id`:

**Files updated:**
- `web_ui/api_key_state.py` - Usage detection query
- `web_ui/lp_position_state.py` - Save/load hedge configuration

**Before:**
```python
# Inconsistent naming
config.get("hedge_wallet_id", "")
supabase.table("position_configs").eq("hedge_wallet_id", key_id)
```

**After:**
```python
# Consistent naming
config.get("hl_api_key_id", "")
supabase.table("position_configs").eq("hl_api_key_id", key_id)
```

## Benefits

1. **Consistency** - Database and code use the same column name
2. **Clarity** - `hl_api_key_id` clearly indicates it's for Hyperliquid
3. **Extensibility** - Easy to add other exchanges without confusion
4. **Maintainability** - No more checking multiple column names
5. **Type Safety** - Single source of truth for column naming

## Future Exchange Integration

When adding a new exchange (e.g., Binance):

1. **No changes needed to `user_api_keys`** - Just set `exchange='binance'`
2. **Add new column to `position_configs`:**
   ```sql
   ALTER TABLE position_configs 
   ADD COLUMN binance_api_key_id UUID REFERENCES user_api_keys(id);
   ```
3. **Update UI** - Add exchange selector in hedge configuration
4. **Update bot logic** - Route hedging to appropriate exchange based on selected API key

## Database Constraints

### 1-to-1 API Key Limitation
```sql
CREATE UNIQUE INDEX unique_api_key_per_position 
ON position_configs (hl_api_key_id) 
WHERE hl_api_key_id IS NOT NULL;
```

This ensures:
- One API key can only be assigned to one position
- NULL values are allowed (positions without hedging)
- Database-level enforcement prevents race conditions

## Testing Checklist

- [ ] Run `STANDARDIZE_API_KEY_COLUMN.sql` on existing database
- [ ] Verify API keys page shows correct "In Use" status
- [ ] Verify LP positions page loads API keys correctly
- [ ] Create new position and assign API key
- [ ] Edit existing position and verify API key persists
- [ ] Try to assign same API key to two positions (should fail with unique constraint)
- [ ] Delete position and verify API key becomes "Available" again

## Rollback Plan

If issues arise, the migration can be reversed:

```sql
-- Add back hedge_wallet_id column
ALTER TABLE position_configs ADD COLUMN hedge_wallet_id UUID REFERENCES user_api_keys(id);

-- Copy data back
UPDATE position_configs SET hedge_wallet_id = hl_api_key_id WHERE hl_api_key_id IS NOT NULL;

-- Drop unique constraint
DROP INDEX IF EXISTS unique_api_key_per_position;
```

However, this should not be necessary as the changes are backward compatible.
