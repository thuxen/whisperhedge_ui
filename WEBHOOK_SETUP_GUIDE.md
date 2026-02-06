# Stripe Webhook Setup Guide

This guide explains how to set up Stripe webhooks to automatically sync subscription and payment data to your database.

## 🎯 What Webhooks Do

Webhooks allow Stripe to notify your app when events happen:
- ✅ User completes checkout → Update subscription in DB
- ✅ Monthly payment succeeds → Log to billing history
- ✅ Payment fails → Mark account as past_due
- ✅ User cancels → Downgrade to free tier

## 📋 Prerequisites

1. **Database Migration** - Run the payment tracking migration:
   ```bash
   # Apply the migration to your Supabase database
   psql $DATABASE_URL < migrations/002_add_payment_tracking.sql
   ```

2. **Environment Variables** - Add to `.env`:
   ```bash
   STRIPE_WEBHOOK_SECRET=whsec_...  # Get this from Stripe Dashboard
   SUPABASE_SERVICE_KEY=...         # Service role key (not anon key!)
   ```

## 🧪 Local Testing with Stripe CLI

### 1. Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.4/stripe_1.19.4_linux_x86_64.tar.gz
tar -xvf stripe_1.19.4_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

### 2. Login to Stripe

```bash
stripe login
```

### 3. Forward Webhooks to Local Server

```bash
# Start your Reflex app first
reflex run

# In another terminal, forward webhooks
stripe listen --forward-to http://localhost:8000/api/stripe-webhook
```

This will output a webhook signing secret like:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
```

**Copy this secret** and add it to your `.env` file:
```bash
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### 4. Test the Webhook

```bash
# Trigger a test checkout.session.completed event
stripe trigger checkout.session.completed
```

Check your terminal - you should see:
```
[DEBUG] Creating checkout session...
User xxx upgraded to hobby
Payment succeeded for subscription sub_xxx
```

## 🚀 Production Setup

### 1. Deploy Your App

Make sure your app is deployed and accessible at a public URL (e.g., `https://yourdomain.com`)

### 2. Configure Webhook in Stripe Dashboard

1. Go to: https://dashboard.stripe.com/webhooks
2. Click **"Add endpoint"**
3. Enter your webhook URL:
   ```
   https://yourdomain.com/api/stripe-webhook
   ```
4. Select events to listen for:
   - ✅ `checkout.session.completed`
   - ✅ `customer.subscription.created`
   - ✅ `customer.subscription.updated`
   - ✅ `customer.subscription.deleted`
   - ✅ `invoice.payment_succeeded`
   - ✅ `invoice.payment_failed`

5. Click **"Add endpoint"**

### 3. Get Production Webhook Secret

After creating the endpoint, Stripe will show you the **Signing secret**.

Add it to your production environment variables:
```bash
STRIPE_WEBHOOK_SECRET=whsec_prod_xxxxxxxxxxxxx
```

### 4. Test Production Webhook

1. Go to your Stripe Dashboard → Webhooks
2. Click on your endpoint
3. Click **"Send test webhook"**
4. Select `checkout.session.completed`
5. Click **"Send test webhook"**

Check your production logs to verify it worked.

## 🔍 Monitoring Webhooks

### Check Webhook Logs in Stripe

1. Go to: https://dashboard.stripe.com/webhooks
2. Click on your endpoint
3. View recent webhook attempts and their status

### Check Database Logs

Query your database to see logged events:

```sql
-- View all payment events
SELECT * FROM payment_events 
ORDER BY event_timestamp DESC 
LIMIT 20;

-- View billing history
SELECT * FROM billing_history 
ORDER BY payment_date DESC 
LIMIT 20;

-- Check user subscription status
SELECT * FROM user_billing_summary 
WHERE user_id = 'your-user-id';
```

## 🐛 Troubleshooting

### Webhook Returns 400 Error

**Problem:** Stripe signature verification failed

**Solution:**
1. Check `STRIPE_WEBHOOK_SECRET` is set correctly
2. Make sure you're using the webhook secret (starts with `whsec_`), not API key
3. Verify the secret matches your environment (test vs production)

### Webhook Returns 500 Error

**Problem:** Database update failed

**Solution:**
1. Check `SUPABASE_SERVICE_KEY` is set (not anon key)
2. Verify database migration was applied
3. Check server logs for specific error

### Events Not Being Received

**Problem:** Stripe isn't sending webhooks

**Solution:**
1. Verify webhook endpoint is publicly accessible
2. Check Stripe Dashboard → Webhooks for delivery attempts
3. Ensure your app is running and `/api/stripe-webhook` endpoint exists

### Database Not Updating

**Problem:** Webhook received but DB not updated

**Solution:**
1. Check server logs for errors
2. Verify `SUPABASE_SERVICE_KEY` has write permissions
3. Check RLS policies allow service role to write

## 📊 What Gets Tracked

### payment_events Table
- Complete audit log of all Stripe events
- Raw event data for debugging
- Searchable by user, customer, subscription

### billing_history Table
- User-friendly payment history
- Shows in "Billing" section of dashboard
- Includes invoice URLs for users to download

### user_subscriptions Table
- Current subscription status
- Stripe customer/subscription IDs
- Billing period dates
- Cancellation status

## 🎉 Success Checklist

- [ ] Database migration applied
- [ ] Environment variables set
- [ ] Webhook endpoint registered in Stripe
- [ ] Test webhook sent successfully
- [ ] Database updated after test
- [ ] Production webhook configured
- [ ] Monitoring set up

## 📚 Next Steps

After webhooks are working:

1. **Add Billing Page** - Show users their payment history
2. **Email Notifications** - Alert users of failed payments
3. **Usage Tracking** - Log when users exceed limits (for overage billing)
4. **Admin Dashboard** - View all subscriptions and revenue

## 🔗 Useful Links

- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Webhook Event Reference](https://stripe.com/docs/api/events/types)
