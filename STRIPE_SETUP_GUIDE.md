# Stripe Setup Guide for WhisperHedge

This guide walks you through setting up Stripe for subscription billing.

## Step 1: Create Stripe Account

1. Go to https://stripe.com and create an account
2. Complete business verification (can start in test mode first)
3. Get your API keys from the Stripe Dashboard

## Step 2: Create Products and Prices in Stripe

### Create Products

In Stripe Dashboard → Products → Add Product, create these 3 products:

#### 1. Hobby Plan
- **Name:** WhisperHedge Hobby
- **Description:** 3 LP Positions, $10,000 Included TVL
- **Pricing:** $19.99/month recurring
- **Billing Period:** Monthly
- Copy the **Price ID** (starts with `price_`)

#### 2. Pro Plan
- **Name:** WhisperHedge Pro
- **Description:** 10 LP Positions, $50,000 Included TVL
- **Pricing:** $49.99/month recurring
- **Billing Period:** Monthly
- Copy the **Price ID** (starts with `price_`)

#### 3. Elite Plan
- **Name:** WhisperHedge Elite
- **Description:** Unlimited LP Positions, $250,000 Included TVL
- **Pricing:** $149.99/month recurring
- **Billing Period:** Monthly
- Copy the **Price ID** (starts with `price_`)

**Note:** Free tier doesn't need a Stripe product since it's $0.

## Step 3: Set Environment Variables

Add these to your `.env` file:

```bash
# Stripe API Keys
STRIPE_SECRET_KEY=sk_test_... # or sk_live_... for production
STRIPE_PUBLISHABLE_KEY=pk_test_... # or pk_live_... for production

# Stripe Price IDs (from Step 2)
STRIPE_PRICE_HOBBY=price_...
STRIPE_PRICE_PRO=price_...
STRIPE_PRICE_ELITE=price_...

# Stripe Webhook Secret (from Step 4)
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Step 4: Set Up Webhooks

### 4.1 Create Webhook Endpoint

In Stripe Dashboard → Developers → Webhooks → Add Endpoint:

**Endpoint URL:** `https://yourdomain.com/api/stripe-webhook`

**Events to listen to:**
- `checkout.session.completed` - When user completes payment
- `customer.subscription.updated` - When subscription status changes
- `customer.subscription.deleted` - When subscription is cancelled

### 4.2 Get Webhook Secret

After creating the webhook, Stripe will show you a **Signing Secret** (starts with `whsec_`).

Copy this and add it to your `.env` as `STRIPE_WEBHOOK_SECRET`.

### 4.3 Test Webhooks Locally (Development)

For local testing, use Stripe CLI:

```bash
# Install Stripe CLI
# https://stripe.com/docs/stripe-cli

# Login
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/api/stripe-webhook

# This will give you a webhook secret for testing
# Use this in your .env for local development
```

## Step 5: Enable Customer Portal

In Stripe Dashboard → Settings → Billing → Customer Portal:

1. **Activate** the customer portal
2. Configure settings:
   - ✅ Allow customers to update payment methods
   - ✅ Allow customers to cancel subscriptions
   - ✅ Allow customers to switch plans
3. Set cancellation behavior:
   - **Recommended:** Cancel at end of billing period (prevents immediate loss of access)

## Step 6: Install Stripe Python Package

```bash
pip install stripe
# or
uv pip install stripe
```

Add to `requirements.txt`:
```
stripe>=8.0.0
```

## Step 7: Implement Backend Integration

The following files have been created for you:

### `web_ui/services/stripe_service.py`
- `create_checkout_session()` - Creates Stripe checkout for plan upgrades
- `create_customer_portal_session()` - Creates portal session for subscription management
- `get_subscription_details()` - Retrieves subscription info
- `verify_webhook_signature()` - Verifies webhook authenticity

### `web_ui/api/stripe_webhook.py`
- `handle_checkout_completed()` - Updates DB when payment succeeds
- `handle_subscription_updated()` - Updates DB when subscription changes
- `handle_subscription_deleted()` - Downgrades to free when cancelled
- `process_stripe_webhook()` - Main webhook processor

### `web_ui/pages/manage_plan.py`
- Full plan management page with all 4 tiers
- Shows current usage and limits
- Upgrade/downgrade buttons
- Link to Stripe customer portal

## Step 8: Create Webhook API Endpoint

You need to create a FastAPI/Reflex API endpoint to receive Stripe webhooks.

Create `web_ui/api/__init__.py`:

```python
from fastapi import APIRouter, Request, HTTPException
from ..services.stripe_service import verify_webhook_signature
from .stripe_webhook import process_stripe_webhook

router = APIRouter()

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    # Verify webhook signature
    event = verify_webhook_signature(payload, sig_header)
    if not event:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Process the event
    success = process_stripe_webhook(event)
    
    if success:
        return {"status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Processing failed")
```

## Step 9: Update ManagePlanState Methods

In `web_ui/pages/manage_plan.py`, implement these methods:

```python
def load_current_plan(self):
    """Load user's current plan from Supabase"""
    # Query user_effective_limits view
    result = supabase.table("user_effective_limits").select("*").eq("user_id", self.user_id).single().execute()
    
    if result.data:
        self.current_tier_name = result.data["tier_name"]
        self.current_display_name = result.data["display_name"]
        self.current_price = result.data["price_monthly"]
        # ... set other fields

def create_checkout_session(self, tier_name: str):
    """Create Stripe checkout session"""
    from ..services.stripe_service import create_checkout_session
    
    checkout_url = create_checkout_session(
        user_id=self.user_id,
        user_email=self.user_email,
        tier_name=tier_name,
        success_url=f"{self.base_url}/manage-plan?success=true",
        cancel_url=f"{self.base_url}/manage-plan?cancelled=true",
    )
    
    if checkout_url:
        # Redirect to Stripe checkout
        return rx.redirect(checkout_url)

def manage_subscription(self):
    """Open Stripe customer portal"""
    from ..services.stripe_service import create_customer_portal_session
    
    portal_url = create_customer_portal_session(
        customer_id=self.stripe_customer_id,
        return_url=f"{self.base_url}/manage-plan",
    )
    
    if portal_url:
        return rx.redirect(portal_url)
```

## Step 10: Test the Flow

### Test Mode (Recommended First)

1. Use test API keys (start with `sk_test_` and `pk_test_`)
2. Use Stripe test card: `4242 4242 4242 4242`
3. Any future expiry date, any CVC

### Test Scenarios

1. **Upgrade from Free to Hobby**
   - Click "Manage Plan" in sidebar
   - Select Hobby plan
   - Complete checkout with test card
   - Verify user_subscriptions updated in Supabase
   - Verify limits updated

2. **Upgrade from Hobby to Pro**
   - Should prorate the difference
   - Verify subscription updated

3. **Cancel Subscription**
   - Click "Manage Subscription in Stripe"
   - Cancel in customer portal
   - Verify webhook downgrades to free at period end

4. **Update Payment Method**
   - Use customer portal
   - Add new card, remove old

## Step 11: Go Live

1. **Switch to Live Mode** in Stripe Dashboard
2. **Update environment variables** with live keys (`sk_live_`, `pk_live_`)
3. **Update webhook endpoint** to production URL
4. **Complete Stripe verification** (business details, bank account)
5. **Test with real card** (small amount)
6. **Monitor** Stripe Dashboard for payments and issues

## Important Notes

### Security
- ✅ Never expose `STRIPE_SECRET_KEY` in frontend code
- ✅ Always verify webhook signatures
- ✅ Use HTTPS in production
- ✅ Store Stripe keys in environment variables, never in code

### Billing
- Stripe charges **2.9% + $0.30** per successful card charge
- Monthly subscriptions are billed automatically
- Failed payments trigger `invoice.payment_failed` webhook (handle this!)

### Customer Experience
- Users can upgrade/downgrade anytime
- Prorated charges/credits are automatic
- Cancellations can be immediate or at period end (configure in portal)

### Webhooks
- Webhooks may be sent multiple times - make handlers idempotent
- Respond with 200 status quickly (< 5 seconds)
- Process heavy logic asynchronously if needed

## Troubleshooting

### Webhook not receiving events
- Check webhook URL is publicly accessible
- Verify webhook secret is correct
- Check Stripe Dashboard → Webhooks for delivery attempts and errors

### Checkout session not creating
- Verify price IDs are correct
- Check API key has correct permissions
- Look for errors in Stripe Dashboard → Logs

### Subscription not updating in database
- Check webhook is receiving events
- Verify Supabase credentials are correct
- Check webhook handler logs for errors

## Support

- **Stripe Docs:** https://stripe.com/docs
- **Stripe Support:** https://support.stripe.com
- **Test Cards:** https://stripe.com/docs/testing
