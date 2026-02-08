-- =====================================================
-- MIGRATION: Update Pricing Tiers - Add Expert, Update Elite
-- Created: 2026-02-08
-- Description: 
--   - Add new 'expert' tier ($89.99, $150k TVL)
--   - Update 'elite' tier price to $199.99 and TVL to $500k
--   - Remove position limits (set to NULL for unlimited)
--   - Update overage fees in features
-- =====================================================

-- Update Elite tier: new price $199.99, new TVL $500k, remove position limit
UPDATE plan_tiers
SET 
    price_monthly = 199.99,
    max_tvl = 500000.00,
    max_positions = NULL,
    features = '{"elite_priority_engine": true, "top_queue_rebalancing": true, "direct_dev_support": true, "unlimited_positions": true, "excess_tvl_fee": "0.05% (5 bps)"}'::jsonb,
    updated_at = NOW()
WHERE tier_name = 'elite';

-- Update Pro tier: remove position limit, update TVL to $50k
UPDATE plan_tiers
SET 
    max_tvl = 50000.00,
    max_positions = NULL,
    features = '{"priority_execution": true, "multi_dex_roadmap": true, "excess_tvl_fee": "0.05% (5 bps)"}'::jsonb,
    updated_at = NOW()
WHERE tier_name = 'pro';

-- Update Hobby tier: remove position limit, update TVL to $10k
UPDATE plan_tiers
SET 
    max_tvl = 10000.00,
    max_positions = NULL,
    features = '{"standard_execution": true, "email_alerts": true, "excess_tvl_fee": "0.1% (10 bps)"}'::jsonb,
    updated_at = NOW()
WHERE tier_name = 'hobby';

-- Update Free tier: keep hard cap, remove position limit
UPDATE plan_tiers
SET 
    max_tvl = 2500.00,
    max_positions = NULL,
    features = '{"standard_execution": true, "hyperliquid_integration": true, "all_strategies": true, "hard_cap": true}'::jsonb,
    updated_at = NOW()
WHERE tier_name = 'free';

-- Insert new Expert tier
INSERT INTO plan_tiers (tier_name, display_name, price_monthly, max_tvl, max_positions, rebalance_frequency, support_level, features)
VALUES (
    'expert',
    'Expert',
    89.99,
    150000.00,
    NULL,
    'priority',
    'priority',
    '{"priority_execution": true, "multi_dex_roadmap": true, "excess_tvl_fee": "0.05% (5 bps)"}'::jsonb
)
ON CONFLICT (tier_name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    price_monthly = EXCLUDED.price_monthly,
    max_tvl = EXCLUDED.max_tvl,
    max_positions = EXCLUDED.max_positions,
    rebalance_frequency = EXCLUDED.rebalance_frequency,
    support_level = EXCLUDED.support_level,
    features = EXCLUDED.features,
    updated_at = NOW();

-- Verify the changes
SELECT tier_name, display_name, price_monthly, max_tvl, max_positions, features
FROM plan_tiers
ORDER BY price_monthly;
