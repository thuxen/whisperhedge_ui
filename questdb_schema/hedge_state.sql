-- ============================================================================
-- QuestDB Table Schema: hedge_state
-- ============================================================================
-- Purpose: Unified state table for VOL_VOL hedge positions
-- Replaces: state_v5, hl_data, lp_data, hedge_runs (deprecated)
-- Partition: Daily for efficient time-series queries
-- Retention: Indefinite (critical operational data)
-- ============================================================================

CREATE TABLE IF NOT EXISTS hedge_state (
    -- Timestamp (designated timestamp column for QuestDB)
    time TIMESTAMP,
    
    -- Position Identification
    position_id SYMBOL INDEX,
    wallet_address SYMBOL CAPACITY 64 CACHE,
    network SYMBOL CAPACITY 16 CACHE,
    lp_position_id STRING,
    hl_vault_address SYMBOL CAPACITY 64 CACHE,
    
    -- Token Symbols
    token0_symbol SYMBOL CAPACITY 64 CACHE,
    token1_symbol SYMBOL CAPACITY 64 CACHE,
    hl_symbol0 SYMBOL CAPACITY 64 CACHE,
    hl_symbol1 SYMBOL CAPACITY 64 CACHE,
    
    -- Hyperliquid Market Data - Token 0
    hl_price_token0 DOUBLE,
    hl_oracle_price_token0 DOUBLE,
    hl_open_interest_token0 DOUBLE,
    hl_day_ntl_vlm_token0 DOUBLE,
    hl_funding_rate_token0 STRING,
    hl_premium_token0 STRING,
    
    -- Hyperliquid Market Data - Token 1
    hl_price_token1 DOUBLE,
    hl_oracle_price_token1 DOUBLE,
    hl_open_interest_token1 DOUBLE,
    hl_day_ntl_vlm_token1 DOUBLE,
    hl_funding_rate_token1 STRING,
    hl_premium_token1 STRING,
    
    -- Hyperliquid Ratio
    hl_ratio_token1_per_token0 DOUBLE,
    
    -- LP vs HL Basis
    ratio_lp_vs_hl_basis_bps INT,
    ratio_lp_vs_hl_basis_pct DOUBLE,
    
    -- LP Position Data
    lp_current_ratio DOUBLE,
    lp_current_tick INT,
    lp_liquidity DOUBLE,
    lp_token0_amount DOUBLE,
    lp_token1_amount DOUBLE,
    lp_value_usd DOUBLE,
    lp_pnl_usd DOUBLE,
    lp_pnl_pct DOUBLE,
    lp_delta_token0 DOUBLE,
    lp_entry_price DOUBLE,
    lp_pa DOUBLE,
    lp_pb DOUBLE,
    lp_last_rebalance_ratio DOUBLE,
    lp_ratio_change_pct DOUBLE,
    lp_utilization_pct DOUBLE,
    lp_distance_to_lower_pct DOUBLE,
    lp_distance_to_upper_pct DOUBLE,
    lp_il_usd DOUBLE,
    lp_il_pct DOUBLE,
    
    -- LP Pool State
    lp_pool_tick INT,
    lp_pool_sqrt_price_x96 STRING,
    lp_pool_liquidity STRING,
    lp_pool_is_inverted BOOLEAN,
    
    -- Hyperliquid Hedge Positions - Token 0
    hl_hedge_token0_current DOUBLE,
    hl_hedge_token0_target DOUBLE,
    hl_hedge_token0_adjustment DOUBLE,
    hl_hedge_token0_notional_usd DOUBLE,
    
    -- Hyperliquid Hedge Positions - Token 1
    hl_hedge_token1_current DOUBLE,
    hl_hedge_token1_target DOUBLE,
    hl_hedge_token1_adjustment DOUBLE,
    hl_hedge_token1_notional_usd DOUBLE,
    
    -- Hedge Metadata
    hl_hedge_gamma DOUBLE,
    hl_hedge_policy STRING,
    hl_hedge_action_status SYMBOL CAPACITY 64 CACHE,
    
    -- Hyperliquid Account State
    hl_account_value DOUBLE,
    hl_margin_used DOUBLE,
    hl_available DOUBLE,
    hl_notional_pos DOUBLE,
    
    -- Script Version
    run_version STRING
    
) TIMESTAMP(time) PARTITION BY DAY;

-- ============================================================================
-- Migration Commands (Run these to add new fields to existing table)
-- ============================================================================

-- Add wallet_address field (SYMBOL type for efficient indexing)
-- ALTER TABLE hedge_state ADD COLUMN wallet_address SYMBOL CAPACITY 64 CACHE;

-- Add network field (SYMBOL type for efficient indexing)
-- ALTER TABLE hedge_state ADD COLUMN network SYMBOL CAPACITY 16 CACHE;

-- Add lp_position_id field (STRING type to store the actual LP position ID)
-- ALTER TABLE hedge_state ADD COLUMN lp_position_id STRING;

-- Add hl_vault_address field (SYMBOL type for efficient indexing)
-- ALTER TABLE hedge_state ADD COLUMN hl_vault_address SYMBOL CAPACITY 64 CACHE;

-- ============================================================================
-- Example Queries
-- ============================================================================

-- Get latest state for all positions
SELECT * FROM hedge_state 
ORDER BY time DESC 
LIMIT 10;

-- Get latest state per position_id
SELECT * FROM hedge_state 
WHERE time > dateadd('m', -10, now())
ORDER BY time DESC;

-- Filter by wallet address (after migration)
SELECT * FROM hedge_state 
WHERE wallet_address = '0xYourWalletAddress'
  AND time > dateadd('d', -1, now())
ORDER BY time DESC;

-- Filter by network (after migration)
SELECT * FROM hedge_state 
WHERE network = 'ethereum'
  AND time > dateadd('d', -1, now())
ORDER BY time DESC;

-- Get positions for specific HL vault (after migration)
SELECT * FROM hedge_state 
WHERE hl_vault_address = '0xYourVaultAddress'
  AND time > dateadd('d', -1, now())
ORDER BY time DESC;
