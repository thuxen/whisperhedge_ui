-- Run this SQL in your Supabase SQL Editor to create the API keys table

-- Create table for storing user API keys
CREATE TABLE IF NOT EXISTS user_api_keys (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    account_name VARCHAR(100) NOT NULL,
    exchange VARCHAR(50) NOT NULL DEFAULT 'hyperliquid',
    api_key TEXT,
    api_secret TEXT NOT NULL,
    is_master_account BOOLEAN DEFAULT true,
    wallet_address TEXT,
    subaccount_name TEXT,
    private_key TEXT,
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, account_name)
);

-- Enable Row Level Security to ensure users can only access their own data
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only access their own API keys
CREATE POLICY "Users can only access their own API keys"
ON user_api_keys FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-update updated_at
CREATE TRIGGER update_user_api_keys_updated_at
    BEFORE UPDATE ON user_api_keys
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create table for storing LP positions
CREATE TABLE IF NOT EXISTS lp_positions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    position_name VARCHAR(100) NOT NULL,
    network VARCHAR(50) NOT NULL,
    nft_id VARCHAR(100) NOT NULL,
    pool_address TEXT,
    token0_symbol VARCHAR(20),
    token1_symbol VARCHAR(20),
    fee_tier VARCHAR(10),
    is_active BOOLEAN DEFAULT true,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, position_name)
);

-- Enable Row Level Security for lp_positions
ALTER TABLE lp_positions ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only access their own LP positions
CREATE POLICY "Users can only access their own LP positions"
ON lp_positions FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Create trigger to auto-update updated_at for lp_positions
CREATE TRIGGER update_lp_positions_updated_at
    BEFORE UPDATE ON lp_positions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- POSITION CONFIGS TABLE (Replaces .py config files)
-- ============================================================================

CREATE TABLE IF NOT EXISTS position_configs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    position_name VARCHAR(100) NOT NULL,
    position_number INT NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    
    -- LP Configuration (from blockchain + user input)
    network VARCHAR(50) NOT NULL,
    nft_position_id VARCHAR(100) NOT NULL,
    pool_address TEXT NOT NULL,
    token0_address TEXT NOT NULL,
    token0_symbol VARCHAR(20) NOT NULL,
    token0_decimals INT NOT NULL,
    token1_address TEXT NOT NULL,
    token1_symbol VARCHAR(20) NOT NULL,
    token1_decimals INT NOT NULL,
    fee_tier VARCHAR(10) NOT NULL,
    tick_lower INT,
    tick_upper INT,
    liquidity NUMERIC(78,0),
    position_size_usd NUMERIC(18,2),
    pa NUMERIC(18,8),
    pb NUMERIC(18,8),
    entry_price NUMERIC(18,8),
    derive_l_from_v BOOLEAN DEFAULT true,
    
    -- Hedge Configuration
    coin VARCHAR(20) NOT NULL,
    sz_decimals INT NOT NULL,
    price_decimals INT NOT NULL,
    hl_api_key_id UUID REFERENCES user_api_keys(id),
    target_hedge_ratio NUMERIC(5,4) DEFAULT 1.0,
    delta_drift_threshold_pct NUMERIC(5,4) DEFAULT 0.0034,
    drift_min_pct_of_capital NUMERIC(5,4) DEFAULT 0.001,
    max_hedge_drift_pct NUMERIC(5,4),
    use_maker_orders BOOLEAN DEFAULT true,
    maker_timeout_seconds INT DEFAULT 25,
    maker_price_offset_bps INT DEFAULT 5,
    
    -- Auto-close Configuration
    auto_close_enabled BOOLEAN DEFAULT false,
    auto_close_threshold NUMERIC(5,4),
    auto_close_cooldown_minutes INT DEFAULT 60,
    slippage_tolerance NUMERIC(5,4) DEFAULT 0.005,
    deadline_seconds INT DEFAULT 300,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_hedged_at TIMESTAMPTZ,
    
    UNIQUE(user_id, position_name),
    UNIQUE(user_id, nft_position_id, network)
);

-- Enable Row Level Security for position_configs
ALTER TABLE position_configs ENABLE ROW LEVEL SECURITY;

-- Create policy: Users can only access their own position configs
CREATE POLICY "Users can only access their own position configs"
ON position_configs FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Create trigger to auto-update updated_at for position_configs
CREATE TRIGGER update_position_configs_updated_at
    BEFORE UPDATE ON position_configs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create index for faster lookups
CREATE INDEX idx_position_configs_user_status ON position_configs(user_id, status);
CREATE INDEX idx_position_configs_position_name ON position_configs(position_name);
