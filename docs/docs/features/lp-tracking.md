# LP Position Tracking

WhisperHedge provides comprehensive tracking for your liquidity provider positions across multiple protocols.

## What We Track

### Position Value
- Current USD value
- Token composition
- Historical value charts
- Value changes over time

### Performance Metrics
- Impermanent loss percentage
- Fee earnings (USD)
- Net P&L (fees - IL)
- APR calculations

### Position Details
- Token balances
- Price ranges (Uniswap V3)
- Liquidity depth
- Pool information

## Update Frequency

Position data updates based on your plan tier:

- **Free:** Every 15 minutes
- **Pro:** Every 5 minutes
- **Premium:** Every 1 minute

Plus manual refresh anytime.

[Learn more about tracking frequency →](../position-setup/tracking-frequency.md)

## Supported Protocols

- **Hyperliquid** - HLP positions
- **Uniswap V3** - Concentrated liquidity

[See all supported protocols →](../position-setup/supported-protocols.md)

## Dashboard Features

### Position List
- Sortable columns
- Filter by protocol
- Search by pair
- Health indicators

### Position Details
- Click any position for details
- Historical charts
- Detailed metrics
- Transaction history

### Quick Actions
- Manual refresh
- Edit position
- Delete position
- Export data

## Data Accuracy

We fetch data directly from:
- Blockchain RPCs
- Protocol APIs
- Price oracles

All calculations use industry-standard formulas for accuracy.

## Related Topics

- [Impermanent Loss](impermanent-loss.md)
- [Position Health](position-health.md)
- [Adding Positions](../getting-started/first-position.md)
