-- Position Configs Table Schema
-- Stores LP position configurations with hedge settings
-- Based on core_hedger_v5 config structure but simplified for database storage

CREATE TABLE position_configs (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Position Metadata
    position_name TEXT NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'paused', 'closed')),
    
    -- LP Configuration (from LP_CONFIG in bot)
    network TEXT NOT NULL, -- 'ethereum', 'arbitrum', 'base', etc.
    nft_id TEXT NOT NULL, -- LP_POSITION_ID from bot
    pool_address TEXT NOT NULL,
    token0_symbol TEXT NOT NULL,
    token0_address TEXT NOT NULL,
    token1_symbol TEXT NOT NULL,
    token1_address TEXT NOT NULL,
    fee_tier INTEGER NOT NULL,
    entry_price DECIMAL(20, 10),
    position_size_usd DECIMAL(20, 2),
    
    -- Hedge Configuration (from HEDGE_CONFIG in bot)
    hedge_enabled BOOLEAN DEFAULT false,
    hedge_token0 BOOLEAN DEFAULT true,
    hedge_token1 BOOLEAN DEFAULT true,
    target_hedge_ratio DECIMAL(5, 2) DEFAULT 80.00, -- 0.00 = dynamic, 10-100 = static %
    hedge_wallet_id UUID REFERENCES user_api_keys(id), -- hl_vault_address + api_secret from bot
    
    -- Dynamic Hedging Configuration (from HEDGE_CONFIG.enable_dynamic_config)
    use_dynamic_hedging BOOLEAN DEFAULT false,
    dynamic_profile TEXT DEFAULT 'balanced' CHECK (dynamic_profile IN ('balanced', 'whisper_dynamic', 'aggressive_upside', 'aggressive_downside', 'volatility_adaptive')),
    rebalance_cooldown_hours DECIMAL(5, 2) DEFAULT 8.00,
    delta_drift_threshold_pct DECIMAL(5, 2) DEFAULT 0.38,
    down_threshold DECIMAL(6, 3) DEFAULT -0.065,
    bounce_threshold DECIMAL(6, 3) DEFAULT -0.038,
    
    -- Hedge Token Mappings (from HEDGE_TOKENS in bot)
    -- NOTE: Consider moving to centralized token_mapping.json for consistency
    -- Stored as JSONB for per-position flexibility if needed
    hedge_tokens JSONB DEFAULT '{
        "token0": {"pool_symbol": "", "hl_symbol": "", "sz_decimals": 0, "price_decimals": 2},
        "token1": {"pool_symbol": "", "hl_symbol": "", "sz_decimals": 0, "price_decimals": 2}
    }'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id, network, nft_id)
);

-- Indexes for performance
CREATE INDEX idx_position_configs_user_id ON position_configs(user_id);
CREATE INDEX idx_position_configs_status ON position_configs(status);
CREATE INDEX idx_position_configs_network_nft ON position_configs(network, nft_id);
CREATE INDEX idx_position_configs_hedge_enabled ON position_configs(hedge_enabled) WHERE hedge_enabled = true;

-- Disable Row Level Security since we're controlling access in backend code
-- The backend filters all queries by user_id from the authenticated session
ALTER TABLE position_configs DISABLE ROW LEVEL SECURITY;

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_position_configs_updated_at
    BEFORE UPDATE ON position_configs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE position_configs IS 'Stores LP position configurations with hedge settings for the hedging bot';
COMMENT ON COLUMN position_configs.target_hedge_ratio IS 'Static hedge ratio 10-100%, or 0 for dynamic hedging';
COMMENT ON COLUMN position_configs.hedge_tokens IS 'Token mapping for Hyperliquid symbol translation and decimals. Consider using centralized token_mapping.json instead.';
COMMENT ON COLUMN position_configs.dynamic_profile IS 'Dynamic hedging strategy: balanced, whisper_dynamic, aggressive_upside, aggressive_downside, volatility_adaptive';
COMMENT ON COLUMN position_configs.rebalance_cooldown_hours IS 'Minimum hours between rebalance operations (1-36 hours typical)';
COMMENT ON COLUMN position_configs.delta_drift_threshold_pct IS 'Percentage drift threshold to trigger rebalance (0.14-0.80 typical range)';
