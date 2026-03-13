-- ============================================================================
-- REGIME TRACKING TABLE MIGRATION
-- ============================================================================
-- 
-- Purpose: Drop and recreate regime_tracking table with corrected schema
-- 
-- Changes:
-- 1. Rename std_token_7d → std_token0_7d (consistent naming)
-- 2. Rename std_eth_7d → std_token1_7d (no hardcoded 'eth')
-- 3. Add arv_7d_pct (dedicated column for ARV)
-- 4. Add atr_7d_pct (dedicated column for ATR)
-- 5. Add pool metrics columns (TVL, volume, ratios)
-- 6. Add Hyperliquid open interest columns
-- 
-- WARNING: This will DELETE all existing regime_tracking data!
-- Only acceptable because we have < 7 days of data.
-- ============================================================================

-- Step 1: Drop existing table
DROP TABLE IF EXISTS regime_tracking;

-- Step 2: Create new table with corrected schema
CREATE TABLE IF NOT EXISTS regime_tracking (
    time TIMESTAMP,
    position_id SYMBOL INDEX,
    
    -- ========================================================================
    -- REGIME CLASSIFICATION
    -- ========================================================================
    
    funding_regime SYMBOL,              -- 'positive_strong', 'positive_mild', 'neutral', 'negative'
    rebalance_aggression SYMBOL,        -- 'aggressive', 'normal', 'lazy'
    mrhl_regime SYMBOL,                 -- 'ultra_fast', 'fast', 'normal', 'slow', 'trend' (nullable)
    
    -- ========================================================================
    -- APPLIED CONFIG VALUES
    -- ========================================================================
    
    target_hedge_ratio DOUBLE,
    delta_drift_threshold_pct DOUBLE,
    rebalance_cooldown_hours DOUBLE,
    down_threshold DOUBLE,
    bounce_threshold DOUBLE,
    lookback_hours INT,
    
    -- ========================================================================
    -- INPUT INDICATORS (CORE)
    -- ========================================================================
    
    corr_returns_7d DOUBLE,             -- 7-day log-returns correlation (primary MVHR driver)
    std_token0_7d DOUBLE,               -- 7-day token0 volatility (RENAMED from std_token_7d)
    std_token1_7d DOUBLE,               -- 7-day token1 volatility (RENAMED from std_eth_7d)
    vol_ratio DOUBLE,                   -- Volatility ratio (token0/token1)
    funding_rate_daily DOUBLE,          -- Daily funding rate (% per day)
    mrhl_hours DOUBLE,                  -- Mean reversion half-life (hours)
    
    -- ========================================================================
    -- VOLATILITY INDICATORS (NEW)
    -- ========================================================================
    
    arv_7d_pct DOUBLE,                  -- Annualized Realized Volatility (7-day)
    atr_7d_pct DOUBLE,                  -- Average True Range (7-day)
    
    -- ========================================================================
    -- POOL METRICS (NEW)
    -- ========================================================================
    
    pool_tvl_usd DOUBLE,                -- Pool total value locked (USD)
    pool_volume_24h_usd DOUBLE,         -- 24-hour trading volume (USD)
    pool_volume_tvl_ratio DOUBLE,       -- Volume/TVL ratio (liquidity efficiency)
    
    -- ========================================================================
    -- HYPERLIQUID DATA (NEW)
    -- ========================================================================
    
    hl_open_interest_token0 DOUBLE,     -- Hyperliquid open interest for token0
    hl_open_interest_token1 DOUBLE,     -- Hyperliquid open interest for token1
    
    -- ========================================================================
    -- MVHR CALCULATION DETAILS
    -- ========================================================================
    
    mvhr_beta_raw DOUBLE,               -- Raw beta from MVHR calculation
    mvhr_base_ratio DOUBLE,             -- Base hedge ratio before funding adjustments
    
    -- ========================================================================
    -- REGIME CHANGE DETECTION
    -- ========================================================================
    
    regime_changed BOOLEAN,             -- True if regime changed from previous entry
    config_changed BOOLEAN,             -- True if config values changed
    previous_funding_regime SYMBOL,     -- Previous funding regime (for change tracking)
    previous_rebalance_aggression SYMBOL,
    previous_mrhl_regime SYMBOL,
    
    -- ========================================================================
    -- METADATA
    -- ========================================================================
    
    dynamic_config_enabled BOOLEAN,     -- Is dynamic config enabled for this position?
    dynamic_config_applied BOOLEAN,     -- Was dynamic config successfully applied?
    fallback_reason SYMBOL,             -- If fallback used: 'missing_indicators', 'disabled', 'error'
    
    -- ========================================================================
    -- EXTENSIBLE INDICATORS (JSON)
    -- ========================================================================
    -- Future-proof storage for additional indicators without schema changes
    
    indicators_json STRING              -- JSON blob for extensible indicator storage
    
) timestamp(time) PARTITION BY DAY;
