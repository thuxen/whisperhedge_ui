# Missing Hedge Configuration Fields - Implementation Summary

## Overview
Added three critical hedge configuration fields that were missing from the initial schema implementation:
1. `lookback_hours` - Pullback filter momentum analysis window
2. `drift_min_pct_of_capital` - Safety parameter for minimum drift size
3. `max_hedge_drift_pct` - Safety parameter for maximum allowed drift

## Changes Made

### 1. Database Schema
**File: `ADD_MISSING_HEDGE_FIELDS.sql`**
- Added SQL migration to add three new columns to `position_configs` table
- Added column comments for documentation
- Default values: lookback_hours=6.0, drift_min_pct_of_capital=0.06, max_hedge_drift_pct=0.50

**File: `ACTUAL_SCHEMA.sql`**
- Updated schema documentation to include the three new fields

### 2. Python Data Models
**File: `web_ui/lp_position_state.py`**

**LPPositionData model (lines 33-35):**
```python
lookback_hours: float = 6.0
drift_min_pct_of_capital: float = 0.06
max_hedge_drift_pct: float = 0.50
```

**LPPositionState class (lines 81-83):**
```python
lookback_hours: float = 6.0
drift_min_pct_of_capital: float = 0.06
max_hedge_drift_pct: float = 0.50
```

### 3. Setter Methods
**File: `web_ui/lp_position_state.py` (lines 162-187)**

Added three setter methods to parse dropdown values:
- `set_lookback_hours()` - Maps "Aggressive (4h)", "Balanced (6h)", "Conservative (12h)"
- `set_drift_min_pct_of_capital()` - Maps "Aggressive (4%)", "Balanced (6%)", "Conservative (10%)"
- `set_max_hedge_drift_pct()` - Maps "Aggressive (40%)", "Balanced (50%)", "Conservative (70%)"

### 4. Database Operations
**File: `web_ui/lp_position_state.py`**

**load_positions (lines 483-485):**
```python
lookback_hours=float(config.get("lookback_hours", 6.0)),
drift_min_pct_of_capital=float(config.get("drift_min_pct_of_capital", 0.06)),
max_hedge_drift_pct=float(config.get("max_hedge_drift_pct", 0.50)),
```

**save_hedge_config (lines 700-702):**
```python
"lookback_hours": float(self.lookback_hours),
"drift_min_pct_of_capital": float(self.drift_min_pct_of_capital),
"max_hedge_drift_pct": float(self.max_hedge_drift_pct),
```

**Debug logging (lines 715-717):**
```python
print(f"  lookback_hours: {config_data.get('lookback_hours')}")
print(f"  drift_min_pct_of_capital: {config_data.get('drift_min_pct_of_capital')}")
print(f"  max_hedge_drift_pct: {config_data.get('max_hedge_drift_pct')}")
```

### 5. UI Form Components
**File: `web_ui/components/lp_positions.py` (lines 667-731)**

Added three new form fields in the hedge configuration section:

**Lookback Hours:**
- Dropdown with options: "Aggressive (4h)", "Balanced (6h)", "Conservative (12h)"
- Tooltip: "Pullback filter: How far back to look for momentum before hedging"
- Help text: "Momentum analysis window"

**Min Drift % of Capital:**
- Dropdown with options: "Aggressive (4%)", "Balanced (6%)", "Conservative (10%)"
- Tooltip: "Safety: Minimum drift size before hedging (as % of position)"
- Help text: "Minimum position size threshold"

**Max Hedge Drift %:**
- Dropdown with options: "Aggressive (40%)", "Balanced (50%)", "Conservative (70%)"
- Tooltip: "Safety: Maximum allowed delta drift before forcing a hedge"
- Help text: "Maximum drift before forced hedge"

### 6. Position Card Display
**File: `web_ui/components/lp_positions.py` (lines 153-180)**

Added display of the three new fields in the hedging settings section:

**Row 2 (4 columns):**
- Delta Drift | Down Threshold | Bounce Threshold | **Lookback Hours**

**Row 3 (4 columns):**
- **Min Drift % Capital** | **Max Hedge Drift** | (empty) | (empty)

## Field Descriptions and Defaults

### lookback_hours
- **Purpose:** Pullback filter momentum analysis window
- **Default:** 6.0 hours (Balanced)
- **Options:**
  - Conservative: 12h (more forgiving of trends)
  - Balanced: 6h
  - Aggressive: 4h (quicker reaction)

### drift_min_pct_of_capital
- **Purpose:** Minimum drift size before hedging (as % of position)
- **Default:** 0.06 (6% - Balanced)
- **Options:**
  - Conservative: 0.10 (10% - fewer tiny trades)
  - Balanced: 0.06 (6%)
  - Aggressive: 0.04 (4% - capture more small moves)

### max_hedge_drift_pct
- **Purpose:** Maximum allowed delta drift before forcing a hedge
- **Default:** 0.50 (50% - Balanced)
- **Options:**
  - Conservative: 0.70 (70% - more drift allowed)
  - Balanced: 0.50 (50%)
  - Aggressive: 0.40 (40% - more frequent protection)

## Database Migration Required

**IMPORTANT:** Before deploying, run the SQL migration:

```bash
# Connect to Supabase and run:
psql -h your-db-host -U postgres -d postgres -f ADD_MISSING_HEDGE_FIELDS.sql
```

Or execute directly in Supabase SQL Editor:
```sql
ALTER TABLE position_configs
ADD COLUMN IF NOT EXISTS lookback_hours NUMERIC DEFAULT 6.0,
ADD COLUMN IF NOT EXISTS drift_min_pct_of_capital NUMERIC DEFAULT 0.06,
ADD COLUMN IF NOT EXISTS max_hedge_drift_pct NUMERIC DEFAULT 0.50;
```

## Testing Checklist

- [ ] Run database migration
- [ ] Create new LP position with all fields
- [ ] Verify fields save correctly to database
- [ ] Edit existing position and update new fields
- [ ] Verify fields display correctly on position card
- [ ] Test all three dropdown options for each field
- [ ] Verify default values are applied correctly
- [ ] Check that hedge bot can read these fields from database

## Files Modified

1. `ADD_MISSING_HEDGE_FIELDS.sql` - New migration file
2. `ACTUAL_SCHEMA.sql` - Schema documentation
3. `web_ui/lp_position_state.py` - Data models, setters, save/load logic
4. `web_ui/components/lp_positions.py` - UI form and display

## Next Steps

1. **Run database migration** on Supabase
2. **Test the UI** - Create/edit positions with new fields
3. **Update hedge bot** to read these fields from database instead of config file
4. **Deploy to VPS** following the deployment guide

## Notes

These fields were originally in the static config file but were missed during the initial database schema implementation. They are critical for:
- **Pullback filtering** (lookback_hours)
- **Safety limits** (drift_min_pct_of_capital, max_hedge_drift_pct)

All three fields are now fully integrated into the UI and database with proper defaults matching the "Balanced" profile from the original config.
