# Hedging Strategy

Protect your liquidity positions from impermanent loss with automated hedging strategies on Hyperliquid.

## Overview

WhisperHedge provides automated hedging strategies that dynamically adjust your exposure to protect against impermanent loss while maintaining your liquidity position. Our strategies use sophisticated algorithms to monitor market conditions and execute trades on Hyperliquid.

## Key Benefits

- **Automated Protection**: No manual intervention required
- **Real-Time Monitoring**: Continuous market analysis and position tracking
- **Risk Management**: Built-in safeguards and configurable risk parameters
- **Capital Efficiency**: Optimize hedging ratios for maximum protection with minimal capital

## Strategy Types

### 1. Dynamic Delta Hedging
Automatically adjusts hedge ratios based on market volatility and your position's delta exposure.

- **Best for**: Most LP positions
- **Adjustment frequency**: Real-time
- **Risk level**: Moderate

### 2. Static Hedge Ratio
Maintains a fixed hedge ratio based on your risk tolerance.

- **Best for**: Stable market conditions
- **Adjustment frequency**: Manual
- **Risk level**: Low to moderate

### 3. Volatility-Based Hedging
Scales hedging intensity based on market volatility indicators.

- **Best for**: Volatile markets
- **Adjustment frequency**: Dynamic
- **Risk level**: Configurable

## Getting Started

1. **Add API Keys**: Set up your Hyperliquid API keys with read-only permissions
2. **Add Position**: Connect your LP position for monitoring
3. **Configure Strategy**: Choose and customize your hedging strategy
4. **Monitor Performance**: Track hedging effectiveness and IL protection

## Risk Management

- **Position Limits**: Maximum exposure per strategy
- **Drawdown Protection**: Automatic reduction of hedge ratios during extreme market moves
- **Collateral Requirements**: Maintain sufficient margin for hedging positions
- **Stop-Loss Protection**: Emergency safeguards for market crashes

## Next Steps

- [Automated Hedging](automated-hedging.md) - Learn about our automated hedging implementation
- [Strategy Options](strategy-options.md) - Detailed strategy configurations
- [Risk Management](risk-management.md) - Risk parameters and safety measures

## Need Help?

- Check our [FAQ](../faq.md)
- [Contact support](../troubleshooting/contact-support.md)
