# Supported Protocols

WhisperHedge currently supports LP position tracking on the following protocols.

## Hyperliquid

**Status:** ✅ Fully Supported

### What We Track

- HLP (Hyperliquid Liquidity Provider) positions
- All trading pairs
- Main account and subaccounts
- Fee earnings
- Impermanent loss
- Position health

### Requirements

- Read-only API key
- API secret
- Subaccount name (if applicable)

[Setup guide →](hyperliquid-positions.md)

### Networks

- Arbitrum (primary)

## Uniswap V3

**Status:** ✅ Fully Supported

### What We Track

- Concentrated liquidity positions
- All trading pairs
- Fee earnings
- Impermanent loss
- Price range status
- Position health

### Requirements

- NFT Token ID
- Wallet address
- Network selection

[Setup guide →](uniswap-v3-nft-id.md)

### Networks

- Ethereum Mainnet
- Polygon
- Arbitrum
- Optimism
- Base

## Coming Soon

### Uniswap V2

**Status:** 🚧 Planned

- Classic AMM positions
- All V2 pairs
- Multiple networks

### Curve Finance

**Status:** 🚧 Planned

- Stable swap pools
- Crypto pools
- Fee tracking

### Balancer

**Status:** 🚧 Planned

- Weighted pools
- Stable pools
- Composable pools

### PancakeSwap

**Status:** 🚧 Planned

- V2 and V3 positions
- BSC network
- Fee tracking

## Protocol Comparison

| Protocol | Type | Networks | API Required | NFT ID Required |
|----------|------|----------|--------------|-----------------|
| Hyperliquid | Perp DEX | Arbitrum | ✅ Yes | ❌ No |
| Uniswap V3 | AMM | Multiple | ❌ No | ✅ Yes |

## Feature Support

### Hyperliquid

- ✅ Real-time position tracking
- ✅ Impermanent loss calculation
- ✅ Fee earnings tracking
- ✅ Subaccount support
- ✅ Historical data
- ✅ Health monitoring

### Uniswap V3

- ✅ Real-time position tracking
- ✅ Impermanent loss calculation
- ✅ Fee earnings tracking
- ✅ Price range monitoring
- ✅ Historical data
- ✅ Health monitoring
- ✅ Multi-network support

## Request New Protocol

Want to see a protocol added?

1. Check our [coming soon](../coming-soon/advanced-features.md) list
2. [Contact support](../troubleshooting/contact-support.md) with your request
3. Include:
   - Protocol name
   - Network
   - Your use case
   - Estimated TVL

We prioritize based on user demand and technical feasibility.

## Related Topics

- [Hyperliquid Positions](hyperliquid-positions.md)
- [Uniswap V3 NFT ID](uniswap-v3-nft-id.md)
- [Adding Your First Position](../getting-started/index.md)
