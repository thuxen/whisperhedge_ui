# Tracking Frequency

WhisperHedge updates your position data at different intervals based on your subscription plan.

## Update Intervals

### Free Tier
**Every 15 minutes**

- Suitable for long-term positions
- Less frequent updates
- Good for stable pairs
- Adequate for most users

### Pro Tier
**Every 5 minutes**

- More frequent monitoring
- Better for active positions
- Catch changes faster
- Recommended for medium-risk positions

### Premium Tier
**Every 1 minute**

- Near real-time tracking
- Ideal for high-value positions
- Quick response to market changes
- Best for active management

## Manual Refresh

All tiers can manually refresh anytime:

1. Click the refresh button on dashboard
2. Or click refresh on individual position
3. Data updates within seconds
4. No limit on manual refreshes

!!! tip "Manual Refresh"
    Use manual refresh when you need immediate data, regardless of your plan tier.

## What Gets Updated

### Each Update Cycle

- Current position value
- Token balances
- Price data
- Impermanent loss
- Fee earnings
- Health status

### Real-Time vs Delayed

**Real-Time (all tiers):**
- Manual refresh
- Critical alerts
- Health warnings

**Scheduled (plan-dependent):**
- Automatic updates
- Historical data
- Performance metrics

## Why Different Frequencies?

### Technical Reasons

**Blockchain Data:**
- Fetching data costs resources
- API rate limits exist
- Network latency varies

**Server Load:**
- More frequent = more server resources
- Balancing cost and performance
- Ensuring reliability

### Practical Reasons

**Most positions don't need minute-by-minute updates:**
- LP positions change gradually
- Fees accumulate over time
- IL develops slowly

**Higher frequency for active traders:**
- Quick response to market moves
- Better risk management
- More informed decisions

## Choosing the Right Tier

### Free Tier (15 min) is Good For:

- Long-term hold positions
- Stable pair LPs
- Low-risk strategies
- Learning the platform
- Small positions (<$10K)

### Pro Tier (5 min) is Good For:

- Active position management
- Medium-risk strategies
- Multiple positions
- Moderate volatility pairs
- Medium positions ($10K-$100K)

### Premium Tier (1 min) is Good For:

- High-value positions
- Volatile pairs
- Active rebalancing
- Professional traders
- Large positions (>$100K)

## Notifications

Regardless of update frequency, you'll receive instant notifications for:

- 🚨 Critical health warnings
- ⚠️ Significant IL changes
- 📉 Major value drops
- 🔴 Position at risk

[Configure notifications →](../features/notifications.md)

## Historical Data

All tiers get full historical data:

- Past position values
- IL over time
- Fee accumulation
- Performance charts

Update frequency only affects real-time monitoring, not historical records.

## API Rate Limits

### Hyperliquid

- Free tier: Well within limits
- Pro tier: Optimized for efficiency
- Premium tier: Dedicated allocation

### Blockchain RPCs

- Multiple RPC providers
- Automatic failover
- Rate limit management
- No impact on your tracking

## Upgrading for Frequency

If you need more frequent updates:

1. Go to [Manage Plan](https://whisperhedge.com/manage-plan)
2. Select higher tier
3. Complete payment
4. Instant activation
5. Immediate frequency increase

[View plan details →](../features/plan-tiers.md)

## Technical Details

### Update Process

1. **Scheduled trigger** - Based on plan tier
2. **Data fetch** - Query blockchain/APIs
3. **Calculate metrics** - IL, fees, health
4. **Update database** - Store new values
5. **Notify if needed** - Send alerts
6. **Display update** - Refresh dashboard

### Accuracy

All tiers get the same data accuracy:

- Same data sources
- Same calculations
- Same precision
- Only timing differs

## Best Practices

### Match Frequency to Strategy

- **Passive LPs** - Free tier sufficient
- **Active monitoring** - Pro tier recommended
- **Professional trading** - Premium tier ideal

### Use Manual Refresh

- Before making decisions
- After major market moves
- When checking specific positions
- To verify alerts

### Enable Notifications

- Don't rely solely on checking dashboard
- Set up email alerts
- Configure thresholds appropriately
- Act on critical warnings

## Related Topics

- [Plan Tiers](../features/plan-tiers.md)
- [Notifications](../features/notifications.md)
- [Position Health](../features/position-health.md)
