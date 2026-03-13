-- QuestDB Schema for Fund Tracker
-- Table: fund_snapshots
-- Purpose: Store complete fund balance snapshots from periodic cron runs
-- Partition: Daily for efficient time-series queries

CREATE TABLE fund_snapshots (
    -- Time (designated timestamp column for QuestDB)
    time TIMESTAMP,
    
    -- Snapshot identifier (links all data from single script run)
    snapshot_id SYMBOL,
    
    -- Core GAV (Gross Asset Value) Metrics
    liquid_assets_total DOUBLE,
    defi_positions_total DOUBLE,
    hyperliquid_equity_total DOUBLE,
    total_gav DOUBLE,
    
    -- Percentage breakdowns
    liquid_assets_pct DOUBLE,
    defi_positions_pct DOUBLE,
    hyperliquid_equity_pct DOUBLE,
    
    -- Hyperliquid Summary Metrics
    hl_total_equity DOUBLE,
    hl_total_margin_used DOUBLE,
    hl_total_available DOUBLE,
    hl_total_notional DOUBLE,
    hl_account_count INT,
    
    -- JSON Data (full details for audit and deep analysis)
    -- Stores arrays of token/position/account objects
    liquid_tokens_json STRING,
    defi_positions_json STRING,
    hyperliquid_accounts_json STRING
    
) timestamp(time) PARTITION BY DAY;

-- Example queries:

-- Latest snapshot
-- SELECT * FROM fund_snapshots ORDER BY time DESC LIMIT 1;

-- GAV trend over last 30 days
-- SELECT time, total_gav, liquid_assets_total, defi_positions_total, hyperliquid_equity_total
-- FROM fund_snapshots 
-- WHERE time > dateadd('d', -30, now())
-- ORDER BY time DESC;

-- Hyperliquid utilization over time
-- SELECT time, hl_total_equity, hl_total_margin_used, 
--        (hl_total_margin_used / hl_total_equity * 100) as utilization_pct
-- FROM fund_snapshots
-- WHERE time > dateadd('d', -7, now())
-- ORDER BY time DESC;

-- Daily GAV change
-- SELECT time, total_gav, 
--        total_gav - LAG(total_gav) OVER (ORDER BY time) as daily_change
-- FROM fund_snapshots
-- ORDER BY time DESC;
