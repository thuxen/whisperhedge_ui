-- ACTUAL DATABASE SCHEMA
-- This file reflects the TRUE schema as it exists in the Supabase database
-- Updated: 2026-01-18
-- This is a COMPLETE schema file that can be run to set up the entire database

-- =====================================================
-- TABLE: user_api_keys
-- =====================================================
CREATE TABLE IF NOT EXISTS user_api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    account_name TEXT NOT NULL,
    exchange TEXT NOT NULL DEFAULT 'hyperliquid',
    api_key TEXT,
    api_secret TEXT NOT NULL,
    is_master_account BOOLEAN DEFAULT true,
    wallet_address TEXT,
    subaccount_name TEXT,
    private_key TEXT,
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    account_value NUMERIC DEFAULT 0,
    available_balance NUMERIC DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for user_api_keys
CREATE INDEX IF NOT EXISTS idx_user_api_keys_user_id ON user_api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_user_api_keys_exchange ON user_api_keys(exchange);

-- =====================================================
-- TABLE: lp_positions
-- =====================================================
CREATE TABLE IF NOT EXISTS lp_positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    position_name TEXT NOT NULL,
    network TEXT NOT NULL,
    nft_id TEXT NOT NULL,
    pool_address TEXT NOT NULL,
    token0_symbol TEXT,
    token1_symbol TEXT,
    fee_tier TEXT,
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, network, nft_id)
);

-- Indexes for lp_positions
CREATE INDEX IF NOT EXISTS idx_lp_positions_user_id ON lp_positions(user_id);
CREATE INDEX IF NOT EXISTS idx_lp_positions_network ON lp_positions(network);
CREATE INDEX IF NOT EXISTS idx_lp_positions_nft_id ON lp_positions(nft_id);

-- =====================================================
-- TABLE: position_configs
-- =====================================================
CREATE TABLE IF NOT EXISTS position_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    position_name TEXT NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'active',
    
    -- LP Position Details
    network TEXT NOT NULL,
    nft_id TEXT NOT NULL,
    pool_address TEXT NOT NULL,
    token0_symbol TEXT NOT NULL,
    token0_address TEXT NOT NULL,
    token1_symbol TEXT NOT NULL,
    token1_address TEXT NOT NULL,
    fee_tier INTEGER NOT NULL,
    entry_price NUMERIC,
    position_size_usd NUMERIC,
    pa NUMERIC,
    pb NUMERIC,
    
    -- Hedge Configuration
    hedge_enabled BOOLEAN DEFAULT false,
    hedge_token0 BOOLEAN DEFAULT true,
    hedge_token1 BOOLEAN DEFAULT true,
    target_hedge_ratio NUMERIC DEFAULT 80.00,
    use_dynamic_hedging BOOLEAN DEFAULT false,
    dynamic_profile TEXT DEFAULT 'balanced',
    rebalance_cooldown_hours NUMERIC DEFAULT 8.00,
    delta_drift_threshold_pct NUMERIC DEFAULT 0.38,
    down_threshold NUMERIC DEFAULT -0.065,
    bounce_threshold NUMERIC DEFAULT -0.038,
    lookback_hours NUMERIC DEFAULT 6.0,
    drift_min_pct_of_capital NUMERIC DEFAULT 0.06,
    max_hedge_drift_pct NUMERIC DEFAULT 0.50,
    
    -- Hedge Token Mapping (JSONB for Hyperliquid symbols and decimals)
    hedge_tokens JSONB DEFAULT '{"token0": {"hl_symbol": "", "pool_symbol": "", "sz_decimals": 0, "price_decimals": 2}, "token1": {"hl_symbol": "", "pool_symbol": "", "sz_decimals": 0, "price_decimals": 2}}'::jsonb,
    
    -- API Key Reference
    hl_api_key_id UUID REFERENCES user_api_keys(id),
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    
    -- Constraints
    UNIQUE(user_id, position_name),
    UNIQUE(user_id, nft_id, network)
);

-- Indexes for position_configs
CREATE INDEX IF NOT EXISTS idx_position_configs_user_id ON position_configs(user_id);
CREATE INDEX IF NOT EXISTS idx_position_configs_user_status ON position_configs(user_id, status);
CREATE INDEX IF NOT EXISTS idx_position_configs_network_nft ON position_configs(network, nft_id);
CREATE INDEX IF NOT EXISTS idx_position_configs_hl_api_key_id ON position_configs(hl_api_key_id);

-- Note: Indexes for lp_positions and user_api_keys already created above

-- =====================================================
-- ROW LEVEL SECURITY
-- =====================================================
ALTER TABLE position_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE lp_positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can only access their own position configs"
ON position_configs FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can only access their own lp positions"
ON lp_positions FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can only access their own api keys"
ON user_api_keys FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- TRIGGERS
-- =====================================================
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

CREATE TRIGGER update_lp_positions_updated_at
    BEFORE UPDATE ON lp_positions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_api_keys_updated_at
    BEFORE UPDATE ON user_api_keys
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
