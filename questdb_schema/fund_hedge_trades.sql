-- ============================================================================
-- Fund Hedge Trades Table
-- ============================================================================
-- Logs all hedge trades executed by the fund_hedging.py script
-- Tracks market orders placed to maintain delta-neutral exposure

CREATE TABLE IF NOT EXISTS fund_hedge_trades (
    -- Trade identification
    coin SYMBOL CAPACITY 128 CACHE,           -- Market symbol (ETH, LINK, AAVE, etc.)
    direction SYMBOL CAPACITY 16 CACHE,       -- LONG or SHORT (typically SHORT for hedges)
    order_type SYMBOL CAPACITY 32 CACHE,      -- Order type (e.g., 'market', 'limit')
    
    -- Trade execution details
    size DOUBLE,                              -- Order size in base asset units
    price DOUBLE,                             -- Execution price (average fill price)
    notional DOUBLE,                          -- Notional value (size * price)
    
    -- Order status
    success INT,                              -- 1 if successful, 0 if failed
    order_id STRING,                          -- Hyperliquid order ID (if successful)
    error STRING,                             -- Error message (if failed)
    
    -- Fee information
    fee_amount DOUBLE,                        -- Fee amount in fee token
    fee_token SYMBOL CAPACITY 16 CACHE,       -- Token used for fees (typically USDC)
    fee_usd DOUBLE,                           -- Fee in USD
    
    -- Trade context
    reason SYMBOL CAPACITY 64 CACHE,          -- Reason for trade (e.g., 'macro_hedge_adjustment', 'rebalance_hedge')
    target_size DOUBLE,                       -- Target position size after trade
    previous_size DOUBLE,                     -- Position size before trade
    
    -- Market regime context (for ETH hedges)
    market_regime SYMBOL CAPACITY 32 CACHE,   -- Market regime (e.g., 'CALM BULL', 'BEAR PANIC')
    eth_arv DOUBLE,                           -- ETH ARV at time of trade (if applicable)
    lp_hedge_ratio DOUBLE,                    -- LP hedge ratio used (if applicable)
    
    -- Timestamp
    time TIMESTAMP                            -- Trade execution timestamp
) timestamp(time) PARTITION BY WEEK WAL
WITH maxUncommittedRows=500000, o3MaxLag=600000us;

-- ============================================================================
-- Example Queries
-- ============================================================================

-- Get all hedge trades for the last 7 days
-- SELECT * FROM fund_hedge_trades 
-- WHERE time > dateadd('d', -7, now())
-- ORDER BY time DESC;

-- Get trade summary by coin
-- SELECT coin, 
--        COUNT(*) as trade_count,
--        SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_trades,
--        SUM(notional) as total_notional,
--        SUM(fee_usd) as total_fees
-- FROM fund_hedge_trades
-- WHERE time > dateadd('d', -30, now())
-- GROUP BY coin;

-- Get ETH hedge trades with market regime
-- SELECT time, direction, size, price, notional, 
--        market_regime, eth_arv, lp_hedge_ratio
-- FROM fund_hedge_trades
-- WHERE coin = 'ETH' AND time > dateadd('d', -7, now())
-- ORDER BY time DESC;

-- Get failed trades for debugging
-- SELECT time, coin, direction, size, error
-- FROM fund_hedge_trades
-- WHERE success = 0 AND time > dateadd('d', -7, now())
-- ORDER BY time DESC;
