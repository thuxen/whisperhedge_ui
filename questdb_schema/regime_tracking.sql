-- ============================================================================
-- Regime Tracking Table for Dynamic Config Analysis
-- ============================================================================
-- 
-- Purpose: Track regime changes and dynamic config decisions over time
-- 
-- Use Cases:
-- 1. Identify regime oscillation causing excessive rebalancing
-- 2. Correlate regime changes with trade frequency
-- 3. Validate hysteresis effectiveness after implementation
-- 4. Debug dynamic config decisions with full indicator context
-- 5. Grafana visualization of regime transitions
--
-- Update Frequency: Only when regime changes (not every hedge run)
-- Retention: Indefinite (regime changes are valuable historical data)
-- ============================================================================

CREATE TABLE IF NOT EXISTS regime_tracking (
    time TIMESTAMP,
    position_id SYMBOL INDEX,
    
    -- ========================================================================
    -- REGIME CLASSIFICATION
    -- ========================================================================
    -- What regime was detected and applied
    
    funding_regime SYMBOL,              -- 'positive_strong', 'positive_mild', 'neutral', 'negative'
    rebalance_aggression SYMBOL,        -- 'aggressive', 'normal', 'lazy'
    mrhl_regime SYMBOL,                 -- 'ultra_fast', 'fast', 'normal', 'slow', 'trend' (nullable)
    
    -- ========================================================================
    -- APPLIED CONFIG VALUES
    -- ========================================================================
    -- The actual config values that were applied to the hedger
    
    target_hedge_ratio DOUBLE,
    delta_drift_threshold_pct DOUBLE,
    rebalance_cooldown_hours DOUBLE,
    down_threshold DOUBLE,
    bounce_threshold DOUBLE,
    lookback_hours INT,
    
    -- ========================================================================
    -- INPUT INDICATORS (CORE)
    -- ========================================================================
    -- The key indicators that drove the regime classification
    
    corr_returns_7d DOUBLE,             -- 7-day log-returns correlation (primary MVHR driver)
    std_token0_7d DOUBLE,               -- 7-day token0 volatility
    std_token1_7d DOUBLE,               -- 7-day token1 volatility
    vol_ratio DOUBLE,                   -- Volatility ratio (token0/token1)
    funding_rate_daily DOUBLE,          -- Daily funding rate (% per day, positive = longs pay shorts)
    mrhl_hours DOUBLE,                  -- Mean reversion half-life (hours, nullable)
    
    -- ========================================================================
    -- VOLATILITY INDICATORS
    -- ========================================================================
    
    arv_7d_pct DOUBLE,                  -- Annualized Realized Volatility (7-day)
    atr_7d_pct DOUBLE,                  -- Average True Range (7-day)
    
    -- ========================================================================
    -- POOL METRICS
    -- ========================================================================
    
    pool_tvl_usd DOUBLE,                -- Pool total value locked (USD)
    pool_volume_24h_usd DOUBLE,         -- 24-hour trading volume (USD)
    pool_volume_tvl_ratio DOUBLE,       -- Volume/TVL ratio (liquidity efficiency)
    
    -- ========================================================================
    -- HYPERLIQUID DATA
    -- ========================================================================
    
    hl_open_interest_token0 DOUBLE,     -- Hyperliquid open interest for token0
    hl_open_interest_token1 DOUBLE,     -- Hyperliquid open interest for token1
    
    -- ========================================================================
    -- MVHR CALCULATION DETAILS
    -- ========================================================================
    -- Intermediate calculations for debugging
    
    mvhr_beta_raw DOUBLE,               -- Raw beta = corr × vol_ratio
    mvhr_base_ratio DOUBLE,             -- Base hedge ratio before funding adjustment
    
    -- ========================================================================
    -- REGIME CHANGE DETECTION
    -- ========================================================================
    -- Track transitions for hysteresis analysis
    
    regime_changed BOOLEAN,             -- True if any regime component changed
    config_changed BOOLEAN,             -- True if any config value changed
    previous_funding_regime SYMBOL,     -- Previous funding regime (for transition tracking)
    previous_rebalance_aggression SYMBOL,
    previous_mrhl_regime SYMBOL,
    
    -- ========================================================================
    -- METADATA
    -- ========================================================================
    
    dynamic_config_enabled BOOLEAN,     -- Was dynamic config enabled in position config?
    dynamic_config_applied BOOLEAN,     -- Was dynamic config actually applied?
    fallback_reason SYMBOL,             -- If fallback used: 'missing_indicators', 'disabled', 'error', etc.
    
    -- ========================================================================
    -- EXTENSIBLE INDICATORS (JSON)
    -- ========================================================================
    -- Future-proof storage for additional indicators without schema changes
    -- 
    -- Example JSON structure:
    -- {
    --   "atr_7d": 0.045,
    --   "atr_30d": 0.038,
    --   "corr_price_level_7d": 0.92,
    --   "corr_price_level_30d": 0.89,
    --   "arv_7d_pct": 45.2,
    --   "arv_30d_pct": 42.1,
    --   "pool_tvl_usd": 1250000,
    --   "pool_volume_24h_usd": 850000,
    --   "pool_volume_tvl_ratio": 0.68,
    --   "pool_price_change_24h_pct": -2.3,
    --   "hl_open_interest_token0": 12500,
    --   "hl_open_interest_token1": 8900,
    --   "indicator_age_minutes": 15,
    --   "indicator_freshness": "fresh"
    -- }
    
    indicators_json STRING              -- JSON blob for extensible indicator storage
    
) timestamp(time) PARTITION BY DAY;

-- ============================================================================
-- INDEXES
-- ============================================================================
-- position_id is already indexed via SYMBOL INDEX above
-- QuestDB automatically indexes timestamp column

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Find all regime changes in last 7 days
-- SELECT time, position_id, funding_regime, previous_funding_regime,
--        target_hedge_ratio, delta_drift_threshold_pct
-- FROM regime_tracking
-- WHERE regime_changed = true 
--   AND time > dateadd('d', -7, now())
-- ORDER BY time DESC;

-- Regime change frequency by position
-- SELECT position_id, 
--        COUNT(*) as total_regime_changes,
--        COUNT(*) FILTER (WHERE funding_regime != previous_funding_regime) as funding_regime_changes,
--        COUNT(*) FILTER (WHERE rebalance_aggression != previous_rebalance_aggression) as aggression_changes
-- FROM regime_tracking
-- WHERE time > dateadd('d', -30, now())
--   AND regime_changed = true
-- GROUP BY position_id
-- ORDER BY total_regime_changes DESC;

-- Correlation between regime changes and trades (within 5 minutes)
-- SELECT r.time as regime_change_time,
--        r.position_id,
--        r.funding_regime,
--        r.previous_funding_regime,
--        r.target_hedge_ratio,
--        t.time as trade_time,
--        t.coin,
--        t.direction,
--        t.size,
--        t.notional
-- FROM regime_tracking r
-- LEFT JOIN trades t ON r.position_id = t.position_id 
--   AND t.time BETWEEN r.time AND dateadd('m', 5, r.time)
-- WHERE r.regime_changed = true
--   AND r.time > dateadd('d', -7, now())
-- ORDER BY r.time DESC;

-- Get current regime for all positions
-- SELECT DISTINCT ON (position_id) 
--        position_id,
--        time,
--        funding_regime,
--        rebalance_aggression,
--        target_hedge_ratio,
--        delta_drift_threshold_pct,
--        corr_returns_7d
-- FROM regime_tracking
-- ORDER BY position_id, time DESC;

-- Regime stability analysis (time between changes)
-- SELECT position_id,
--        funding_regime,
--        AVG(time_diff_hours) as avg_hours_in_regime,
--        MIN(time_diff_hours) as min_hours_in_regime,
--        MAX(time_diff_hours) as max_hours_in_regime,
--        COUNT(*) as regime_occurrences
-- FROM (
--     SELECT position_id,
--            funding_regime,
--            DATEDIFF('hour', LAG(time) OVER (PARTITION BY position_id ORDER BY time), time) as time_diff_hours
--     FROM regime_tracking
--     WHERE regime_changed = true
--       AND time > dateadd('d', -30, now())
-- )
-- WHERE time_diff_hours IS NOT NULL
-- GROUP BY position_id, funding_regime
-- ORDER BY position_id, avg_hours_in_regime;
