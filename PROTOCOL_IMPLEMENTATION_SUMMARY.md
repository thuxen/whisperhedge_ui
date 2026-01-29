# Protocol Field Implementation Summary

## Overview
Successfully added `protocol` field to support multiple DEX protocols (Uniswap V3, Aerodrome, etc.) in the LP position management system.

## Changes Made

### 1. Database Schema (`SUPABASE_SCHEMA.sql`)
- Added `protocol TEXT NOT NULL DEFAULT 'uniswap_v3'` to `lp_positions` table
- Added `protocol TEXT NOT NULL DEFAULT 'uniswap_v3'` to `position_configs` table
- Updated UNIQUE constraints to include protocol:
  - `lp_positions`: `UNIQUE(user_id, protocol, network, nft_id)`
  - `position_configs`: `UNIQUE(user_id, protocol, nft_id, network)`

### 2. Protocol Configuration (`web_ui/protocol_config.py`)
New file created with:
- `SUPPORTED_PROTOCOLS` dictionary mapping protocol IDs to configuration
- Helper functions:
  - `get_protocol_config(protocol)` - Get full config for a protocol
  - `get_position_manager_address(protocol, network)` - Get contract address
  - `get_position_manager_abi(protocol)` - Get contract ABI
  - `get_supported_protocols()` - List all supported protocols
  - `get_protocol_display_name(protocol)` - Human-readable name
  - `get_protocols_for_network(network)` - Protocols available on a network

Currently supports:
- **Uniswap V3** on: Ethereum, Arbitrum, Base, Polygon, Optimism

### 3. State Management (`web_ui/lp_position_state.py`)
- Added `protocol` field to `LPPositionData` model
- Added `protocol` field to `LPPositionState` class
- Added `_fetch_protocol` temporary state variable
- Updated `fetch_position_data_handler()` to capture protocol from form
- Updated `fetch_position_data_worker()` to populate protocol field
- Updated `save_position_worker()` to include protocol in lp_data
- Updated `save_hedge_config()` to include protocol in config_data
- Updated `load_positions()` to read protocol from database and use it in config matching

### 4. UI Components (`web_ui/components/lp_positions.py`)
- Added **Protocol dropdown** to position lookup form (before Network and NFT ID)
- Protocol is selected at lookup time and becomes non-editable
- Added protocol display in confirmation step
- Currently shows only "uniswap_v3" option (more will be added as support is implemented)

### 5. Migration SQL (`MIGRATION_PROTOCOL_FIELD.sql`)
Created migration file with commands to:
1. Add `protocol` column to both tables
2. Drop old unique constraints
3. Add new unique constraints including protocol
4. Set existing positions to `'uniswap_v3'`
5. Verification queries

## Next Steps

### To Deploy:
1. **Run migration SQL in Supabase SQL Editor:**
   - Open `MIGRATION_PROTOCOL_FIELD.sql`
   - Execute all commands in Supabase dashboard
   - Verify with the included verification queries

2. **Test the UI:**
   - Add a new position and verify protocol dropdown appears
   - Confirm protocol is saved correctly
   - Verify existing positions load with `uniswap_v3` protocol

### To Add New Protocols:
1. **Update `protocol_config.py`:**
   ```python
   "aerodrome": {
       "name": "Aerodrome",
       "description": "Aerodrome concentrated liquidity on Base",
       "position_manager_addresses": {
           "base": "0x...",  # Contract address
       },
       "supported_networks": ["base"],
       "position_manager_abi": [...],  # Contract ABI
   }
   ```

2. **Update UI dropdown in `lp_positions.py`:**
   ```python
   rx.select(
       ["uniswap_v3", "aerodrome"],  # Add new protocol
       ...
   )
   ```

3. **Update `blockchain_utils.py`:**
   - Modify `fetch_uniswap_position()` to accept `protocol` parameter
   - Use `protocol_config.get_position_manager_address(protocol, network)`
   - Use `protocol_config.get_position_manager_abi(protocol)`

## Architecture Notes

### Two-Table System:
- **`lp_positions`**: Discovery/lookup log for all positions users have viewed
  - Used for tracking and potential indicator pre-fetching
  - Includes protocol field for proper identification

- **`position_configs`**: Active hedge configurations
  - Backend bot only hedges positions in this table
  - Includes protocol field for proper blockchain lookups

### Protocol Selection:
- Protocol is selected **at position lookup time**
- Protocol is **non-editable** after selection (positions don't change protocols)
- Each protocol has its own position manager contract address per network
- Protocol determines which ABI to use for blockchain queries

## Files Modified
- `SUPABASE_SCHEMA.sql` - Schema updates
- `web_ui/lp_position_state.py` - State management
- `web_ui/components/lp_positions.py` - UI components

## Files Created
- `web_ui/protocol_config.py` - Protocol configuration
- `MIGRATION_PROTOCOL_FIELD.sql` - Database migration
- `PROTOCOL_IMPLEMENTATION_SUMMARY.md` - This file

## Important Notes
- All existing positions will default to `protocol='uniswap_v3'`
- The unique constraint now includes protocol, allowing same NFT ID on different protocols
- Backend hedging bot will need to pass protocol to blockchain lookup functions
- Protocol field is required (NOT NULL) with default value for safety
