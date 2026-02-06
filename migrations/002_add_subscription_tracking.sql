-- =====================================================
-- MIGRATION: Add Subscription Tracking (Simplified)
-- Created: 2026-02-06
-- Description: Track subscription status locally, use Stripe API for billing history
-- =====================================================

-- =====================================================
-- UPDATE: user_subscriptions (Add Stripe tracking fields)
-- =====================================================
ALTER TABLE user_subscriptions 
ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT,
ADD COLUMN IF NOT EXISTS stripe_subscription_id TEXT,
ADD COLUMN IF NOT EXISTS subscription_status TEXT DEFAULT 'active',
ADD COLUMN IF NOT EXISTS current_period_start TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS current_period_end TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS cancel_at_period_end BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS cancelled_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS trial_end TIMESTAMPTZ;

-- Add constraint for subscription status
ALTER TABLE user_subscriptions
DROP CONSTRAINT IF EXISTS user_subscriptions_status_check;

ALTER TABLE user_subscriptions
ADD CONSTRAINT user_subscriptions_status_check 
    CHECK (subscription_status IN (
        'active',
        'trialing',
        'past_due',      -- Payment failed but still has access
        'canceled',
        'unpaid',
        'incomplete',
        'incomplete_expired',
        'paused'
    ));

-- Indexes for Stripe lookups
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_stripe_customer 
    ON user_subscriptions(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_stripe_subscription 
    ON user_subscriptions(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_user_subscriptions_status 
    ON user_subscriptions(subscription_status);

-- =====================================================
-- VIEW: user_subscription_status (Quick Status Check)
-- =====================================================
CREATE OR REPLACE VIEW user_subscription_status AS
SELECT 
    us.user_id,
    us.plan_tier_id,
    pt.tier_name,
    pt.display_name,
    pt.price_monthly,
    us.subscription_status,
    us.stripe_customer_id,
    us.stripe_subscription_id,
    us.current_period_start,
    us.current_period_end,
    us.cancel_at_period_end,
    
    -- Effective limits (with overrides)
    COALESCE(us.override_tvl_limit, us.subscribed_tvl_limit, pt.max_tvl) as effective_tvl_limit,
    COALESCE(us.override_position_limit, us.subscribed_position_limit, pt.max_positions) as effective_position_limit,
    
    -- Access status (graceful - allow access even if past_due)
    CASE 
        WHEN us.subscription_status IN ('active', 'trialing', 'past_due') THEN true
        WHEN us.subscription_status = 'canceled' AND us.current_period_end > NOW() THEN true
        ELSE false
    END as has_access,
    
    -- Warning flags
    CASE 
        WHEN us.subscription_status = 'past_due' THEN 'Payment failed - please update payment method'
        WHEN us.cancel_at_period_end THEN 'Subscription will cancel at period end'
        WHEN us.subscription_status = 'canceled' THEN 'Subscription cancelled'
        ELSE NULL
    END as warning_message
    
FROM user_subscriptions us
LEFT JOIN plan_tiers pt ON us.plan_tier_id = pt.id;

-- =====================================================
-- GRANT Permissions
-- =====================================================
GRANT SELECT ON user_subscription_status TO authenticated;

-- Service role needs full access for webhook processing
GRANT ALL ON user_subscriptions TO service_role;

COMMENT ON VIEW user_subscription_status IS 'Quick subscription status check with graceful access control';
COMMENT ON COLUMN user_subscriptions.subscription_status IS 'Stripe subscription status - past_due users still have access';
