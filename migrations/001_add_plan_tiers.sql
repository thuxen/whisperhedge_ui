-- =====================================================
-- MIGRATION: Add Plan Tiers and User Subscriptions
-- Created: 2026-02-05
-- Description: Adds plan tier management and user subscription tracking
-- =====================================================

-- =====================================================
-- TABLE: plan_tiers (Master Plan Definitions)
-- =====================================================
CREATE TABLE IF NOT EXISTS plan_tiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tier_name TEXT NOT NULL UNIQUE, -- 'free', 'starter', 'professional', 'enterprise'
    display_name TEXT NOT NULL, -- 'Free', 'Starter', 'Professional', 'Enterprise'
    price_monthly DECIMAL(10,2) NOT NULL,
    max_tvl DECIMAL(15,2), -- NULL for unlimited
    max_positions INTEGER, -- NULL for unlimited
    rebalance_frequency TEXT NOT NULL, -- 'hourly', '15min', '5min', 'realtime'
    support_level TEXT NOT NULL, -- 'community', 'email', 'priority', 'dedicated'
    features JSONB DEFAULT '{}'::jsonb, -- Additional features as JSON
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for plan_tiers
CREATE INDEX IF NOT EXISTS idx_plan_tiers_tier_name ON plan_tiers(tier_name);
CREATE INDEX IF NOT EXISTS idx_plan_tiers_active ON plan_tiers(is_active);

-- =====================================================
-- TABLE: user_subscriptions (User's Current Plan + Overrides)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    plan_tier_id UUID REFERENCES plan_tiers(id),
    
    -- Snapshot of limits at subscription time (allows grandfathering)
    subscribed_tvl_limit DECIMAL(15,2),
    subscribed_position_limit INTEGER,
    subscribed_rebalance_frequency TEXT,
    
    -- Manual overrides (NULL means use subscribed value)
    override_tvl_limit DECIMAL(15,2),
    override_position_limit INTEGER,
    override_rebalance_frequency TEXT,
    override_support_level TEXT,
    
    -- Billing info
    stripe_subscription_id TEXT,
    stripe_customer_id TEXT,
    billing_cycle_start TIMESTAMPTZ,
    billing_cycle_end TIMESTAMPTZ,
    status TEXT DEFAULT 'active', -- 'active', 'cancelled', 'past_due', 'trialing'
    
    -- Beta/testing flags
    is_beta_tester BOOLEAN DEFAULT false,
    beta_notes TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id)
);

-- Indexes for user_subscriptions
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_user_id ON user_subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_plan_tier_id ON user_subscriptions(plan_tier_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status ON user_subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_stripe_customer ON user_subscriptions(stripe_customer_id);

-- =====================================================
-- VIEW: user_effective_limits (Computed Effective Limits)
-- =====================================================
CREATE OR REPLACE VIEW user_effective_limits AS
SELECT 
    us.user_id,
    us.plan_tier_id,
    pt.tier_name,
    pt.display_name,
    pt.price_monthly,
    
    -- Effective limits (override takes precedence, NULL means unlimited)
    COALESCE(us.override_tvl_limit, us.subscribed_tvl_limit, pt.max_tvl) as effective_tvl_limit,
    COALESCE(us.override_position_limit, us.subscribed_position_limit, pt.max_positions) as effective_position_limit,
    COALESCE(us.override_rebalance_frequency, us.subscribed_rebalance_frequency, pt.rebalance_frequency) as effective_rebalance_frequency,
    COALESCE(us.override_support_level, pt.support_level) as effective_support_level,
    
    -- Flags
    us.is_beta_tester,
    us.status as subscription_status,
    us.billing_cycle_end,
    
    -- Override indicators (for display)
    CASE WHEN us.override_tvl_limit IS NOT NULL THEN true ELSE false END as has_tvl_override,
    CASE WHEN us.override_position_limit IS NOT NULL THEN true ELSE false END as has_position_override,
    CASE WHEN us.override_rebalance_frequency IS NOT NULL THEN true ELSE false END as has_rebalance_override,
    
    pt.features
FROM user_subscriptions us
JOIN plan_tiers pt ON us.plan_tier_id = pt.id;

-- =====================================================
-- ROW LEVEL SECURITY
-- =====================================================
ALTER TABLE plan_tiers ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;

-- Plan tiers are readable by everyone (for pricing page)
CREATE POLICY "Plan tiers are publicly readable"
ON plan_tiers FOR SELECT
USING (true);

-- Users can only access their own subscription
CREATE POLICY "Users can only access their own subscription"
ON user_subscriptions FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- TRIGGERS
-- =====================================================
CREATE TRIGGER update_plan_tiers_updated_at
    BEFORE UPDATE ON plan_tiers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_subscriptions_updated_at
    BEFORE UPDATE ON user_subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SEED DATA: Insert Initial Plan Tiers
-- =====================================================
INSERT INTO plan_tiers (tier_name, display_name, price_monthly, max_tvl, max_positions, rebalance_frequency, support_level, features) VALUES
('free', 'Free', 0.00, 2500.00, 1, 'standard', 'community', 
 '{"standard_execution": true, "hyperliquid_integration": true, "all_strategies": true}'::jsonb),
 
('hobby', 'Hobby', 19.99, 10000.00, 3, 'standard', 'email', 
 '{"standard_execution": true, "email_alerts": true, "excess_tvl_fee": "0.1% (10 bps)"}'::jsonb),
 
('pro', 'Pro', 49.99, 50000.00, 10, 'priority', 'priority', 
 '{"priority_execution": true, "multi_dex_roadmap": true, "excess_tvl_fee": "0.05% (5 bps)"}'::jsonb),
 
('elite', 'Elite', 149.99, 250000.00, NULL, 'elite', 'direct', 
 '{"elite_priority_engine": true, "top_queue_rebalancing": true, "direct_dev_support": true, "unlimited_positions": true, "excess_tvl_fee": "0.05% (5 bps)"}'::jsonb)
ON CONFLICT (tier_name) DO NOTHING;

-- =====================================================
-- FUNCTION: Auto-assign free tier to new users
-- =====================================================
CREATE OR REPLACE FUNCTION assign_free_tier_to_new_user()
RETURNS TRIGGER AS $$
DECLARE
    free_tier_id UUID;
    free_tier_record RECORD;
BEGIN
    -- Get the free tier
    SELECT id, max_tvl, max_positions, rebalance_frequency 
    INTO free_tier_record
    FROM plan_tiers 
    WHERE tier_name = 'free' 
    LIMIT 1;
    
    -- Create subscription for new user
    INSERT INTO user_subscriptions (
        user_id, 
        plan_tier_id, 
        subscribed_tvl_limit, 
        subscribed_position_limit, 
        subscribed_rebalance_frequency,
        status,
        billing_cycle_start
    ) VALUES (
        NEW.id,
        free_tier_record.id,
        free_tier_record.max_tvl,
        free_tier_record.max_positions,
        free_tier_record.rebalance_frequency,
        'active',
        NOW()
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to auto-assign free tier on user signup
CREATE TRIGGER on_auth_user_created_assign_free_tier
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION assign_free_tier_to_new_user();

-- =====================================================
-- HELPER FUNCTIONS
-- =====================================================

-- Function to get user's effective limits
CREATE OR REPLACE FUNCTION get_user_limits(p_user_id UUID)
RETURNS TABLE (
    tier_name TEXT,
    display_name TEXT,
    price_monthly DECIMAL,
    effective_tvl_limit DECIMAL,
    effective_position_limit INTEGER,
    effective_rebalance_frequency TEXT,
    effective_support_level TEXT,
    is_beta_tester BOOLEAN,
    has_tvl_override BOOLEAN,
    has_position_override BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        uel.tier_name,
        uel.display_name,
        uel.price_monthly,
        uel.effective_tvl_limit,
        uel.effective_position_limit,
        uel.effective_rebalance_frequency,
        uel.effective_support_level,
        uel.is_beta_tester,
        uel.has_tvl_override,
        uel.has_position_override
    FROM user_effective_limits uel
    WHERE uel.user_id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
