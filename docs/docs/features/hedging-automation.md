# Automated Hedging

WhisperHedge's core feature: automated IL mitigation through intelligent perpetual hedging on Hyperliquid.

## How It Works

### 1. Position Monitoring
We continuously monitor your LP position:
- Token composition and ratios
- Active tick range (Uniswap V3)
- Current delta exposure
- Price divergence from entry

### 2. Hedge Calculation
Our algorithm determines optimal hedge size:
- Asymmetric under-hedging (not 1:1)
- Variance-based flexibility
- Funding rate awareness
- Net-profit optimization

### 3. Automated Execution
Hedges execute automatically on Hyperliquid:
- Perpetual futures positions
- Institutional-grade execution
- Deep liquidity
- Transparent on-chain

### 4. Continuous Optimization
The system adapts in real-time:
- Rebalances only when necessary
- Minimizes execution friction
- Monitors funding costs
- Protects against black swan events

## Hedging Strategy

### Asymmetric Under-Hedging

We don't chase "perfect zero" delta. Instead:

**Traditional approach:**
- Constant 1:1 hedge ratio
- Frequent rebalancing
- High execution costs
- Funding rate drain

**WhisperHedge approach:**
- Flexible variance-based hedging
- Rebalance only when needed
- Minimize execution costs
- Funding-aware optimization

### Funding Rate Optimization

Perpetual hedges have costs (funding rates). We optimize:

- Monitor funding vs LP fees
- Adjust hedge size dynamically
- Close hedges when too expensive
- Ensure net-positive returns

### Black Swan Protection

Catastrophic price moves shouldn't wipe out months of fees:

- Asymmetric protection
- Soft drawdown limits
- Emergency hedge activation
- Principal preservation focus

## Configuration

### Hedge Parameters

You can configure:

- **Hedge ratio** - How much to hedge (default: asymmetric)
- **Rebalance threshold** - When to adjust hedges
- **Funding limit** - Max acceptable funding rate
- **Risk tolerance** - Conservative to aggressive

### Position Linking

Link your LP position:

1. **Uniswap V3** - Provide NFT ID
2. **Hyperliquid HLP** - Already on same platform

### Hyperliquid API Keys

Provide trade-enabled API keys:

- **Trading permissions required** - To execute hedges
- **Restricted to trading only** - No withdrawal access
- **Separate key per position** - Security isolation

[API Key Setup →](../api-keys/hyperliquid-keys.md)

## Monitoring

### Dashboard View

Track your hedging performance:

- Current hedge positions
- Net P&L (LP fees + hedge P&L)
- Funding costs
- IL mitigation effectiveness

### Hedge Status

See real-time hedge information:

- Open perpetual positions
- Hedge ratio
- Funding rate
- Next rebalance estimate

### Performance Metrics

Measure effectiveness:

- IL without hedge (theoretical)
- IL with hedge (actual)
- IL mitigated (difference)
- Net profit after costs

## Safety Features

### Non-Custodial

- We never touch your LP principal
- Only execute hedges via API
- Your funds stay in your wallet
- Full transparency

### Risk Limits

- Maximum hedge size limits
- Funding rate cutoffs
- Emergency stop functionality
- Position size validation

### Monitoring & Alerts

- Unusual activity detection
- Funding spike warnings
- Hedge failure notifications
- System health monitoring

## Best Practices

### Starting Out

- Start with conservative settings
- Monitor for first few days
- Understand funding dynamics
- Adjust based on results

### Optimization

- Review weekly performance
- Adjust hedge ratio if needed
- Monitor funding vs fees
- Consider market conditions

### When to Adjust

Increase hedge ratio if:
- High volatility expected
- Large price moves likely
- Want more protection

Decrease hedge ratio if:
- Funding rates too high
- Stable market conditions
- Fees outpacing IL

## Related Topics

- [Impermanent Loss](impermanent-loss.md)
- [LP Positions](lp-tracking.md)
- [API Keys](../api-keys/hyperliquid-keys.md)
