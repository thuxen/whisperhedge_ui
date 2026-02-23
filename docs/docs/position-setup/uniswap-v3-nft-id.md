# Finding Your Uniswap V3 NFT ID

Uniswap V3 positions are represented as NFTs (Non-Fungible Tokens). Each position has a unique Token ID that you need to track it in WhisperHedge.

## What is an NFT ID?

When you provide liquidity on Uniswap V3, you receive an NFT that represents your position. This NFT has a unique Token ID (a number) that identifies your specific position.

**Example:** `123456`

## How to Find Your NFT ID

### Method 1: Uniswap Interface

1. Go to [app.uniswap.org](https://app.uniswap.org)
2. Connect your wallet
3. Click on "Pool" in the top navigation
4. Find your position in the list
5. Click on the position to view details
6. Look for "Token ID" or "NFT ID" in the position details

### Method 2: Etherscan (Ethereum)

1. Go to [etherscan.io](https://etherscan.io)
2. Search for your wallet address
3. Click on "ERC-721 Tokens" tab
4. Find "Uniswap V3: Positions NFT"
5. Click to view your NFTs
6. The Token ID is shown for each position

### Method 3: Wallet (MetaMask, etc.)

Some wallets display NFTs:

1. Open your wallet
2. Navigate to NFTs or Collectibles section
3. Find "Uniswap V3 Positions"
4. Click on your position
5. View the Token ID in the details

### Method 4: Block Explorer

For other networks (Polygon, Arbitrum, etc.):

1. Go to the appropriate block explorer:
   - Polygon: polygonscan.com
   - Arbitrum: arbiscan.io
   - Optimism: optimistic.etherscan.io
2. Follow same steps as Etherscan method

## What You'll Also Need

### Wallet Address

The wallet address that holds the NFT:

**Example:** `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

### Network

The blockchain network where your position exists:

- Ethereum Mainnet
- Polygon
- Arbitrum
- Optimism
- Base

## Adding to WhisperHedge

Once you have your NFT ID:

1. Go to WhisperHedge dashboard
2. Click "+ Add Position"
3. Select "Uniswap V3"
4. Enter:
   - NFT Token ID
   - Wallet address
   - Network
5. Click "Verify Position"
6. Save

## Troubleshooting

### "NFT ID Not Found"

**Causes:**
- Wrong network selected
- NFT ID doesn't exist
- Position was closed
- Wrong wallet address

**Solutions:**
- Verify network matches where position was created
- Check NFT ID is correct (no typos)
- Confirm position still exists
- Verify wallet address owns the NFT

### "Invalid NFT ID"

**Causes:**
- Non-numeric characters
- NFT ID is for different protocol
- Copy/paste error

**Solutions:**
- Ensure ID is just numbers (e.g., 123456)
- Verify it's a Uniswap V3 position NFT
- Re-copy the ID carefully

## Multiple Positions

If you have multiple Uniswap V3 positions:

- Each position has its own unique NFT ID
- Add each position separately
- Use descriptive labels to track them
- All positions from same wallet can be tracked

## Related Topics

- [Supported Protocols](supported-protocols.md)
- [Adding Your First Position](../getting-started/first-position.md)
- [Hyperliquid Positions](hyperliquid-positions.md)
