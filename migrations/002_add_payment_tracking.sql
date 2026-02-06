-- =====================================================
-- MIGRATION: Add Payment and Billing Event Tracking
-- Created: 2026-02-06
-- Description: Track all Stripe events, payments, and subscription changes
-- =====================================================

-- =====================================================
-- TABLE: payment_events (Complete Stripe Event Log)
-- =====================================================
CREATE TABLE IF NOT EXISTS payment_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Stripe identifiers
    stripe_event_id TEXT UNIQUE NOT NULL,
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    stripe_invoice_id TEXT,
    stripe_payment_intent_id TEXT,
    
    -- Event details
    event_type TEXT NOT NULL, -- 'checkout.session.completed', 'invoice.paid', etc.
    event_status TEXT NOT NULL, -- 'succeeded', 'failed', 'pending'
    
    -- Financial details
    amount_cents INTEGER, -- Amount in cents
    currency TEXT DEFAULT 'usd',
    
    -- Plan details at time of event
    plan_tier_name TEXT,
    plan_display_name TEXT,
    
    -- Metadata
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    raw_event JSONB, -- Full Stripe event for debugging
    
    -- Timestamps
    event_timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Indexing
    CONSTRAINT payment_events_event_type_check 
        CHECK (event_type IN (
            'checkout.session.completed',
            'invoice.payment_succeeded',
            'invoice.payment_failed',
            'customer.subscription.created',
            'customer.subscription.updated',
            'customer.subscription.deleted',
            'customer.subscription.trial_will_end',
            'invoice.upcoming',
            'charge.succeeded',
            'charge.failed',
            'charge.refunded'
        ))
);

-- Indexes for payment_events
CREATE INDEX IF NOT EXISTS idx_payment_events_user_id ON payment_events(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_events_stripe_customer ON payment_events(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_payment_events_stripe_subscription ON payment_events(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS idx_payment_events_event_type ON payment_events(event_type);
CREATE INDEX IF NOT EXISTS idx_payment_events_event_timestamp ON payment_events(event_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_payment_events_status ON payment_events(event_status);

-- =====================================================
-- TABLE: billing_history (User-Friendly Payment Summary)
-- =====================================================
CREATE TABLE IF NOT EXISTS billing_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Payment details
    payment_date TIMESTAMPTZ NOT NULL,
    amount_cents INTEGER NOT NULL,
    currency TEXT DEFAULT 'usd',
    status TEXT NOT NULL, -- 'paid', 'failed', 'refunded', 'pending'
    
    -- What was billed
    billing_type TEXT NOT NULL, -- 'subscription', 'overage', 'one_time'
    plan_tier_name TEXT,
    description TEXT NOT NULL,
    
    -- Stripe references
    stripe_invoice_id TEXT,
    stripe_payment_intent_id TEXT,
    invoice_url TEXT, -- Link to Stripe hosted invoice
    
    -- Period covered
    period_start TIMESTAMPTZ,
    period_end TIMESTAMPTZ,
    
    -- Overage details (if applicable)
    overage_tvl DECIMAL(15,2),
    overage_positions INTEGER,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for billing_history
CREATE INDEX IF NOT EXISTS idx_billing_history_user_id ON billing_history(user_id);
CREATE INDEX IF NOT EXISTS idx_billing_history_payment_date ON billing_history(payment_date DESC);
CREATE INDEX IF NOT EXISTS idx_billing_history_status ON billing_history(status);
CREATE INDEX IF NOT EXISTS idx_billing_history_billing_type ON billing_history(billing_type);

-- =====================================================
-- UPDATE: user_subscriptions (Add Stripe tracking)
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
        'past_due',
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
-- VIEW: user_billing_summary (Easy Account Status Check)
-- =====================================================
CREATE OR REPLACE VIEW user_billing_summary AS
SELECT 
    us.user_id,
    us.plan_tier_id,
    pt.tier_name,
    pt.display_name,
    us.subscription_status,
    us.stripe_customer_id,
    us.stripe_subscription_id,
    us.current_period_start,
    us.current_period_end,
    us.cancel_at_period_end,
    
    -- Last successful payment
    (SELECT MAX(payment_date) 
     FROM billing_history 
     WHERE user_id = us.user_id 
     AND status = 'paid') as last_payment_date,
    
    -- Total paid (lifetime)
    (SELECT COALESCE(SUM(amount_cents), 0) 
     FROM billing_history 
     WHERE user_id = us.user_id 
     AND status = 'paid') as total_paid_cents,
    
    -- Failed payment count (last 90 days)
    (SELECT COUNT(*) 
     FROM billing_history 
     WHERE user_id = us.user_id 
     AND status = 'failed'
     AND payment_date > NOW() - INTERVAL '90 days') as recent_failed_payments,
    
    -- Account health indicator
    CASE 
        WHEN us.subscription_status = 'active' THEN 'healthy'
        WHEN us.subscription_status = 'past_due' THEN 'warning'
        WHEN us.subscription_status IN ('canceled', 'unpaid') THEN 'inactive'
        ELSE 'unknown'
    END as account_health
    
FROM user_subscriptions us
LEFT JOIN plan_tiers pt ON us.plan_tier_id = pt.id;

-- =====================================================
-- FUNCTION: Update timestamp on billing_history
-- =====================================================
CREATE OR REPLACE FUNCTION update_billing_history_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_billing_history_timestamp
    BEFORE UPDATE ON billing_history
    FOR EACH ROW
    EXECUTE FUNCTION update_billing_history_timestamp();

-- =====================================================
-- RLS Policies
-- =====================================================

-- payment_events: Users can only see their own events
ALTER TABLE payment_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY payment_events_select_own 
    ON payment_events FOR SELECT 
    USING (auth.uid() = user_id);

-- billing_history: Users can only see their own billing
ALTER TABLE billing_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY billing_history_select_own 
    ON billing_history FOR SELECT 
    USING (auth.uid() = user_id);

-- =====================================================
-- GRANT Permissions
-- =====================================================
GRANT SELECT ON payment_events TO authenticated;
GRANT SELECT ON billing_history TO authenticated;
GRANT SELECT ON user_billing_summary TO authenticated;

-- Service role needs full access for webhook processing
GRANT ALL ON payment_events TO service_role;
GRANT ALL ON billing_history TO service_role;
GRANT ALL ON user_subscriptions TO service_role;

COMMENT ON TABLE payment_events IS 'Complete log of all Stripe webhook events for audit trail';
COMMENT ON TABLE billing_history IS 'User-friendly payment history for displaying in UI';
COMMENT ON VIEW user_billing_summary IS 'Quick account status check with payment health indicators';
