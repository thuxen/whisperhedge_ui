# LP Positions

WhisperHedge monitors your liquidity provider positions for automated hedging.

## What We Monitor

### Position Value
- Current USD value
- Token composition
- Value changes over time

### Performance Metrics
- Impermanent loss percentage
- Fee earnings (USD)
- Net P&L (fees - IL)

### Position Details
- Token balances
- Price ranges (Uniswap V3)
- Pool information

## Supported Protocols

- **Hyperliquid** - For hedging
- **Uniswap V3** - Concentrated liquidity

[See all supported protocols →](../position-setup/supported-protocols.md)

## Dashboard Features

### Position List
- View all positions
- Filter by protocol
- Search by pair

### Position Details
- Click any position for details
- Performance metrics
- Hedge status

### Quick Actions
- Manual refresh
- Edit position
- Delete position

## Data Accuracy

We fetch data directly from:
- Blockchain RPCs
- Protocol APIs
- Price oracles

## Related Topics

- [Impermanent Loss](impermanent-loss.md)
- [Hedging Strategy](../hedging-strategy/index.md)
- [Adding Positions](../getting-started/first-position.md)
