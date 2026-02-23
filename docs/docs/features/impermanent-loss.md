# Impermanent Loss Monitoring

Track and understand impermanent loss (IL) across all your LP positions.

## What is Impermanent Loss?

Impermanent loss occurs when the price ratio of tokens in a liquidity pool changes compared to when you deposited them. You would have been better off holding the tokens instead of providing liquidity.

## How We Calculate IL

```
IL% = (Current Value - Hold Value) / Hold Value × 100
```

Where:
- **Current Value** = Your LP position value now
- **Hold Value** = Value if you had just held the tokens

### Example

You deposit $1000 worth of ETH/USDC (50/50):
- Initial: 0.5 ETH @ $2000 + 1000 USDC

ETH price doubles to $4000:
- If you held: 0.5 ETH @ $4000 + 1000 USDC = $3000
- As LP: ~0.35 ETH @ $4000 + ~1400 USDC = $2800
- IL: ($2800 - $3000) / $3000 = -6.7%

## IL Tracking Features

### Real-Time Monitoring
- Current IL percentage
- IL in USD
- Historical IL charts
- IL trends

### Alerts
- IL threshold warnings
- Significant IL changes
- Critical IL levels
- Email notifications

### Analysis
- IL vs fees earned
- Net P&L (fees - IL)
- Break-even analysis
- APR including IL

## Understanding IL Metrics

### Negative IL
- You're losing compared to holding
- Common in volatile markets
- May be offset by fees

### Positive IL
- You're gaining vs holding
- Rare but possible
- Usually in stable pairs

### IL + Fees
- Net result of LP position
- Fees can offset IL
- Important for profitability

## IL Mitigation

### Strategies
- Choose stable pairs
- Narrow price ranges (Uniswap V3)
- Monitor regularly
- Exit when IL is high

### When to Exit
- IL exceeds fee earnings
- Market becoming too volatile
- Better opportunities elsewhere
- Risk tolerance exceeded

## Related Topics

- [LP Tracking](lp-tracking.md)
- [Position Health](position-health.md)
- [Notifications](notifications.md)
