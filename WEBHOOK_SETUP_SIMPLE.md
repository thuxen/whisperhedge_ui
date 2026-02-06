# Simplified Webhook Setup Guide

This guide shows how to set up Stripe webhooks to sync subscription status to your database.

**Philosophy:** 
- ✅ Track subscription status locally (fast, reliable bot operations)
- ✅ Use Stripe Customer Portal for billing history (less code, Stripe handles it)
- ✅ Graceful degradation (past_due users keep access)

## 📋 Quick Setup

### 1. Run Database Migration

```bash
# Connect to your Supabase database
psql $DATABASE_URL < migrations/002_add_subscription_tracking.sql
```

This adds Stripe tracking fields to `user_subscriptions`:
- `stripe_customer_id`
- `stripe_subscription_id`
- `subscription_status`
- `current_period_start/end`
- `cancel_at_period_end`

### 2. Add Environment Variables

Add to your `.env` file:

```bash
# Stripe webhook secret (get from Stripe CLI or Dashboard)
STRIPE_WEBHOOK_SECRET=whsec_...

# Supabase service role key (NOT the anon key!)
SUPABASE_SERVICE_KEY=eyJhbGc...
```

### 3. Test Locally with Stripe CLI

#### Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.4/stripe_1.19.4_linux_x86_64.tar.gz
tar -xvf stripe_1.19.4_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

#### Forward Webhooks

```bash
# Terminal 1: Start your app
reflex run

# Terminal 2: Forward webhooks
stripe login
stripe listen --forward-to http://localhost:8000/api/stripe-webhook
```

Copy the webhook secret from the output:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

Add it to `.env`:
```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

#### Test It

```bash
# Trigger a test checkout event
stripe trigger checkout.session.completed
```

Check your terminal - you should see:
```
✅ User xxx upgraded to hobby
```

Check your database:
```sql
SELECT user_id, subscription_status, stripe_subscription_id 
FROM user_subscriptions 
WHERE stripe_subscription_id IS NOT NULL;
```

## 🚀 Production Setup

### 1. Configure Webhook in Stripe Dashboard

1. Go to: https://dashboard.stripe.com/webhooks
2. Click **"Add endpoint"**
3. Enter: `https://yourdomain.com/api/stripe-webhook`
4. Select events:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`
5. Copy the **Signing secret**
6. Add to production environment:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_prod_xxxxxxxxxxxxx
   ```

### 2. Enable Stripe Customer Portal

1. Go to: https://dashboard.stripe.com/settings/billing/portal
2. Enable the portal
3. Configure settings:
   - ✅ Allow customers to update payment methods
   - ✅ Allow customers to cancel subscriptions
   - ✅ Allow customers to view invoices

Now users can click "Manage Subscription" in your app and be taken to Stripe's portal to:
- View billing history
- Download invoices
- Update payment method
- Cancel subscription

## 📊 What Gets Synced

### Subscription Status Values

| Status | Meaning | User Has Access? |
|--------|---------|------------------|
| `active` | Subscription is active | ✅ Yes |
| `trialing` | In trial period | ✅ Yes |
| `past_due` | Payment failed | ✅ Yes (graceful!) |
| `canceled` | Subscription cancelled | ✅ Until period end |
| `unpaid` | Multiple payment failures | ❌ No |

### Graceful Degradation

Users with `past_due` status **still have access** to the bot. This gives them time to update their payment method without disrupting their positions.

## 🔍 Monitoring

### Check Subscription Status

```sql
-- View all active subscriptions
SELECT * FROM user_subscription_status 
WHERE subscription_status IN ('active', 'trialing', 'past_due');

-- Check specific user
SELECT * FROM user_subscription_status 
WHERE user_id = 'your-user-id';

-- Find users with payment issues
SELECT user_id, tier_name, subscription_status, warning_message
FROM user_subscription_status 
WHERE subscription_status = 'past_due';
```

### Check Webhook Logs

In Stripe Dashboard → Webhooks → Your endpoint → View logs

## 🐛 Troubleshooting

### Webhook Returns 400 Error

**Problem:** Signature verification failed

**Solution:**
1. Check `STRIPE_WEBHOOK_SECRET` is correct
2. Use webhook secret (starts with `whsec_`), not API key
3. Verify test vs production secret

### Subscription Not Updating

**Problem:** Webhook received but DB not updated

**Solution:**
1. Check `SUPABASE_SERVICE_KEY` is set (not anon key)
2. Verify migration was applied
3. Check server logs for errors

### User Still on Free Tier After Payment

**Problem:** Webhook didn't fire or failed

**Solution:**
1. Check Stripe Dashboard → Webhooks for delivery attempts
2. Manually trigger webhook from Stripe Dashboard
3. Check server logs for errors

## 🎯 What This Enables

✅ **Fast Bot Operations** - No API calls to check subscription  
✅ **Reliable Hedging** - Works even if Stripe is down  
✅ **Graceful Degradation** - Don't cut off users for payment hiccups  
✅ **Simple Billing** - Stripe handles invoices, receipts, history  
✅ **Less Code** - No need to build billing UI  

## 📚 Next Steps

After webhooks are working:

1. **Test the full flow:**
   - Sign up for paid plan
   - Verify subscription status updates
   - Check bot has correct limits
   - Test Stripe Customer Portal

2. **Add user notifications:**
   - Email when payment fails
   - Warning banner for past_due status
   - Reminder to update payment method

3. **Monitor subscription health:**
   - Track churn rate
   - Monitor failed payments
   - Identify users at risk

## 🔗 Useful Links

- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks)
- [Stripe Customer Portal](https://stripe.com/docs/billing/subscriptions/integrating-customer-portal)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
