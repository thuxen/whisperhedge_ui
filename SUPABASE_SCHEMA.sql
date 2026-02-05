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
    protocol TEXT NOT NULL,
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
    UNIQUE(user_id, protocol, network, nft_id)
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
    protocol TEXT NOT NULL,
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
    UNIQUE(user_id, protocol, nft_id, network)
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

-- =====================================================
-- TABLE: plan_tiers (Master Plan Definitions)
-- =====================================================
-- Tiers: free ($0, 1 pos, $2.5k TVL), hobby ($19.99, 3 pos, $10k TVL),
--        pro ($49.99, 10 pos, $50k TVL), elite ($149.99, unlimited pos, $250k TVL)
CREATE TABLE IF NOT EXISTS plan_tiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier_name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    price_monthly DECIMAL(10,2) NOT NULL,
    max_tvl DECIMAL(15,2),
    max_positions INTEGER,
    rebalance_frequency TEXT NOT NULL,
    support_level TEXT NOT NULL,
    features JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_plan_tiers_tier_name ON plan_tiers(tier_name);
CREATE INDEX IF NOT EXISTS idx_plan_tiers_active ON plan_tiers(is_active);

-- =====================================================
-- TABLE: user_subscriptions (User's Current Plan + Overrides)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    plan_tier_id UUID REFERENCES plan_tiers(id),
    subscribed_tvl_limit DECIMAL(15,2),
    subscribed_position_limit INTEGER,
    subscribed_rebalance_frequency TEXT,
    override_tvl_limit DECIMAL(15,2),
    override_position_limit INTEGER,
    override_rebalance_frequency TEXT,
    override_support_level TEXT,
    stripe_subscription_id TEXT,
    stripe_customer_id TEXT,
    billing_cycle_start TIMESTAMPTZ,
    billing_cycle_end TIMESTAMPTZ,
    status TEXT DEFAULT 'active',
    is_beta_tester BOOLEAN DEFAULT false,
    beta_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id)
);

CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_plan_tier_id ON user_subscriptions(plan_tier_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status ON user_subscriptions(status);

-- =====================================================
-- VIEW: user_effective_limits
-- =====================================================
CREATE OR REPLACE VIEW user_effective_limits AS
SELECT 
    us.user_id,
    us.plan_tier_id,
    pt.tier_name,
    pt.display_name,
    pt.price_monthly,
    COALESCE(us.override_tvl_limit, us.subscribed_tvl_limit, pt.max_tvl) as effective_tvl_limit,
    COALESCE(us.override_position_limit, us.subscribed_position_limit, pt.max_positions) as effective_position_limit,
    COALESCE(us.override_rebalance_frequency, us.subscribed_rebalance_frequency, pt.rebalance_frequency) as effective_rebalance_frequency,
    COALESCE(us.override_support_level, pt.support_level) as effective_support_level,
    us.is_beta_tester,
    us.status as subscription_status,
    us.billing_cycle_end,
    CASE WHEN us.override_tvl_limit IS NOT NULL THEN true ELSE false END as has_tvl_override,
    CASE WHEN us.override_position_limit IS NOT NULL THEN true ELSE false END as has_position_override,
    pt.features
FROM user_subscriptions us
JOIN plan_tiers pt ON us.plan_tier_id = pt.id;

-- =====================================================
-- RLS for plan_tiers and user_subscriptions
-- =====================================================
ALTER TABLE plan_tiers ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Plan tiers are publicly readable"
ON plan_tiers FOR SELECT
USING (true);

CREATE POLICY "Users can only access their own subscription"
ON user_subscriptions FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- TRIGGERS for plan_tiers and user_subscriptions
-- =====================================================
CREATE TRIGGER update_plan_tiers_updated_at
    BEFORE UPDATE ON plan_tiers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_subscriptions_updated_at
    BEFORE UPDATE ON user_subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
