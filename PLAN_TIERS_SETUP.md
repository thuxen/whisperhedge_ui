# Plan Tiers Setup Guide

## Step 1: Run the Migration SQL in Supabase

Copy and paste the entire contents of `migrations/001_add_plan_tiers.sql` into the Supabase SQL Editor and execute it.

This will:
- Create `plan_tiers` table with 4 tiers (Free, Starter, Professional, Enterprise)
- Create `user_subscriptions` table for tracking user plans
- Create `user_effective_limits` view for easy limit queries
- Set up Row Level Security policies
- Insert seed data for all 4 plan tiers
- Create auto-assignment trigger for new users (assigns Free tier)

## Step 2: Verify the Setup

Run these queries in Supabase SQL Editor to verify:

```sql
-- Check plan tiers were created
SELECT * FROM plan_tiers ORDER BY price_monthly;

-- Check if any users have subscriptions
SELECT * FROM user_subscriptions;

-- View effective limits for all users
SELECT * FROM user_effective_limits;
```

## Step 3: Manual Operations

### Give a User Beta Tester Access (Unlimited Everything)

```sql
UPDATE user_subscriptions 
SET 
    is_beta_tester = true,
    override_tvl_limit = NULL, -- NULL = unlimited
    override_position_limit = NULL, -- NULL = unlimited
    override_rebalance_frequency = 'realtime',
    beta_notes = 'Early adopter - full access for testing'
WHERE user_id = 'USER_UUID_HERE';
```

### Give a User Custom Limits (Not Beta, Just Higher Limits)

```sql
UPDATE user_subscriptions 
SET 
    override_tvl_limit = 500000.00, -- Custom TVL limit
    override_position_limit = 25, -- Custom position limit
    beta_notes = 'Special arrangement - custom limits'
WHERE user_id = 'USER_UUID_HERE';
```

### Upgrade a User to a Specific Tier

```sql
-- First, get the tier ID
SELECT id, tier_name, display_name FROM plan_tiers WHERE tier_name = 'professional';

-- Then update the user's subscription
UPDATE user_subscriptions 
SET 
    plan_tier_id = 'TIER_UUID_FROM_ABOVE',
    subscribed_tvl_limit = 250000.00,
    subscribed_position_limit = 10,
    subscribed_rebalance_frequency = '5min',
    billing_cycle_start = NOW(),
    billing_cycle_end = NOW() + INTERVAL '30 days'
WHERE user_id = 'USER_UUID_HERE';
```

### Check a Specific User's Effective Limits

```sql
SELECT * FROM user_effective_limits WHERE user_id = 'USER_UUID_HERE';
```

### List All Beta Testers

```sql
SELECT 
    us.user_id,
    au.email,
    us.is_beta_tester,
    us.beta_notes,
    uel.effective_tvl_limit,
    uel.effective_position_limit
FROM user_subscriptions us
JOIN auth.users au ON us.user_id = au.id
JOIN user_effective_limits uel ON us.user_id = uel.user_id
WHERE us.is_beta_tester = true;
```

### Remove Beta Status (Return to Normal Plan)

```sql
UPDATE user_subscriptions 
SET 
    is_beta_tester = false,
    override_tvl_limit = NULL, -- Remove override, use plan limit
    override_position_limit = NULL,
    override_rebalance_frequency = NULL,
    beta_notes = NULL
WHERE user_id = 'USER_UUID_HERE';
```

## Plan Tier Details

### Free Tier
- **Price:** $0/month
- **TVL Limit:** $10,000
- **Positions:** 1
- **Rebalance:** Hourly
- **Support:** Community

### Starter Tier
- **Price:** $29/month
- **TVL Limit:** $50,000
- **Positions:** 3
- **Rebalance:** Every 15 minutes
- **Support:** Email

### Professional Tier
- **Price:** $99/month
- **TVL Limit:** $250,000
- **Positions:** 10
- **Rebalance:** Every 5 minutes
- **Support:** Priority

### Enterprise Tier
- **Price:** $499/month
- **TVL Limit:** Unlimited
- **Positions:** Unlimited
- **Rebalance:** Realtime
- **Support:** Dedicated

## Understanding Overrides

The system has two types of limits:

1. **Subscribed Limits** - Snapshot of plan limits when user subscribed (allows grandfathering)
2. **Override Limits** - Manual overrides set by admin (takes precedence)

**Effective Limit Calculation:**
```
effective_limit = override_limit ?? subscribed_limit ?? plan_tier_limit
```

**NULL in override means:**
- For beta testers: Unlimited
- For regular users: Use subscribed limit

## Database Schema

### plan_tiers
- Master definition of all available plans
- Publicly readable (for pricing page)
- Admin-only write access

### user_subscriptions
- One row per user
- Contains subscribed limits (snapshot at subscription time)
- Contains override limits (for manual adjustments)
- User can only see their own subscription

### user_effective_limits (VIEW)
- Computed view combining plan + subscription + overrides
- Shows final effective limits for each user
- Used by application to check limits
