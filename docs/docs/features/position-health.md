# Position Health Monitoring

WhisperHedge monitors your positions and alerts you to potential issues before they become problems.

## Health Indicators

### 🟢 Healthy
- IL within acceptable range
- Fees offsetting IL
- Position performing well
- No immediate concerns

### 🟡 Warning
- IL increasing
- Approaching risk thresholds
- Volatility rising
- Attention recommended

### 🔴 Critical
- High IL
- Significant losses
- Immediate action needed
- Risk of major loss

## Health Factors

We consider multiple factors:

### Impermanent Loss
- Current IL percentage
- IL trend (increasing/decreasing)
- IL vs historical average

### Fee Performance
- Fee earnings rate
- Fees vs IL comparison
- APR calculations

### Market Conditions
- Price volatility
- Liquidity depth
- Trading volume

### Position Specifics
- Time in position
- Entry vs current prices
- Range status (Uniswap V3)

## Alerts & Notifications

### When You'll Be Notified

- 🚨 Critical health warnings
- ⚠️ IL threshold exceeded
- 📉 Significant value drops
- 🔴 Position at high risk

### Notification Channels

- Email (all tiers)
- Pushover (coming soon)
- Telegram (coming soon)

[Configure notifications →](notifications.md)

## Health Score

Each position gets a health score (0-100):

- **90-100:** Excellent
- **70-89:** Good
- **50-69:** Fair
- **30-49:** Poor
- **0-29:** Critical

## Taking Action

### When Health is Poor

1. Review position details
2. Check IL vs fees
3. Consider market conditions
4. Decide: hold, adjust, or exit

### Exit Strategies

- Close position entirely
- Reduce position size
- Adjust price range (Uniswap V3)
- Wait for market stabilization

## Related Topics

- [Impermanent Loss](impermanent-loss.md)
- [Notifications](notifications.md)
- [LP Tracking](lp-tracking.md)
