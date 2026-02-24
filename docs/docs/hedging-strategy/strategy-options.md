# Strategy Options

Choose the right hedging strategy based on your risk tolerance, market conditions, and investment goals.

## Strategy Types

### 1. Dynamic Delta Hedging

**Best for:** Most LP positions, varying market conditions
**Risk Level:** Moderate
**Adjustment Frequency:** Real-time

#### How It Works
- Continuously calculates optimal hedge ratio based on delta exposure
- Adjusts hedges as price moves and liquidity shifts
- Balances protection vs. funding costs dynamically

#### Advantages
- Maximum IL protection
- Adapts to market conditions
- Optimal capital efficiency

#### Considerations
- Higher monitoring requirements
- More frequent adjustments
- Potential for higher trading costs

#### Configuration
- **Hedge Ratio:** 70-90% (asymmetric)
- **Rebalance Threshold:** 0.5-1% delta change
- **Funding Limit:** 0.01% daily

---

### 2. Static Hedge Ratio

**Best for:** Stable markets, hands-off approach
**Risk Level:** Low to Moderate
**Adjustment Frequency:** Manual

#### How It Works
- Maintains a fixed hedge ratio regardless of market conditions
- Only rebalances when manually triggered
- Predictable costs and exposure

#### Advantages
- Simple to understand
- Predictable funding costs
- Lower monitoring overhead

#### Considerations
- Less responsive to market changes
- May over-hedge or under-hedge in certain conditions
- Manual intervention required

#### Configuration
- **Hedge Ratio:** 50-80% (fixed)
- **Rebalance Threshold:** Manual only
- **Funding Limit:** No limit (user discretion)

---

### 3. Volatility-Based Hedging

**Best for:** Volatile markets, active traders
**Risk Level:** Configurable
**Adjustment Frequency:** Dynamic

#### How It Works
- Scales hedge intensity based on market volatility
- Increases protection during high volatility
- Reduces hedging during calm periods

#### Advantages
- Cost-efficient in stable periods
- Enhanced protection when needed
- Adapts to market regime changes

#### Considerations
- Requires volatility monitoring
- Complex optimization logic
- May lag sudden volatility spikes

#### Configuration
- **Base Hedge Ratio:** 40-60%
- **Volatility Multiplier:** 1.5-3x during high vol
- **Volatility Threshold:** 2x historical average

---

## Advanced Options

### Funding-Aware Hedging

Automatically reduces hedge ratios when funding rates become prohibitive:

- **Funding Threshold:** Maximum acceptable funding rate
- **Hedge Reduction:** Scale down hedges when funding exceeds threshold
- **Recovery Mode:** Resume normal hedging when funding improves

### Time-Based Hedging

Adjust hedge ratios based on time patterns:

- **Intraday:** Higher hedging during active hours
- **Weekend:** Reduced hedging during low liquidity
- **News Events:** Pre-emptive hedging around major announcements

### Correlation Hedging

Consider cross-asset correlations:

- **Portfolio View:** Hedge based on overall exposure
- **Correlation Matrix:** Account for token relationships
- **Basket Hedging:** Optimize across multiple positions

## Risk Parameters

### Position Limits

- **Maximum Hedge Size:** 150% of LP value
- **Per-Token Limits:** Individual token exposure caps
- **Portfolio Limits:** Total hedging exposure

### Drawdown Protection

- **Soft Limits:** Warning at 10% drawdown
- **Hard Limits:** Stop hedging at 20% drawdown
- **Recovery:** Gradual resumption after stabilization

### Emergency Controls

- **Circuit Breakers:** Halt during extreme volatility
- **Manual Override:** User can disable automation
- **Safe Mode:** Conservative hedging during uncertainty

## Choosing Your Strategy

### Conservative Profile
- **Recommended:** Static Hedge Ratio (60-70%)
- **Focus:** Capital preservation
- **Market:** Stable, predictable conditions

### Moderate Profile
- **Recommended:** Dynamic Delta Hedging
- **Focus:** Balance protection and costs
- **Market:** Normal volatility conditions

### Aggressive Profile
- **Recommended:** Volatility-Based Hedging
- **Focus:** Maximum protection
- **Market:** High volatility or uncertainty

### Custom Profile
- **Recommended:** Mix of strategies
- **Focus:** Specific requirements
- **Market:** Varying conditions

## Strategy Switching

You can change strategies at any time:

1. **Current Position:** Strategy applies immediately
2. **New Positions:** Use new strategy by default
3. **Transition Period:** Gradual adjustment over 24-48 hours

## Performance Monitoring

Track strategy effectiveness:

- **IL Mitigation:** Protection vs. theoretical loss
- **Cost Efficiency:** Hedging costs vs. LP fees
- **Risk Metrics:** Volatility, drawdown, recovery
- **Optimization Opportunities:** Areas for improvement

## Next Steps

- [Risk Management](risk-management.md) - Safety parameters and controls
- [Automated Hedging](automated-hedging.md) - Technical implementation
- [Getting Started](../getting-started/index.md) - Set up your first strategy

## Need Help?

- Check our [FAQ](../faq.md)
- [Contact support](../troubleshooting/contact-support.md)
