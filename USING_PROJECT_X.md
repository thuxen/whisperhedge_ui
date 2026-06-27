# Using Project X (HyperEVM DEX) with WhisperHedge

## Quick Start Guide

### Adding a Project X Position

1. **Navigate to LP Positions**
   - Go to the LP Positions section in WhisperHedge

2. **Select Protocol**
   - Click "Add Position"
   - In the Protocol dropdown, select **"Project X"**

3. **Network Selection**
   - The network will automatically be set to **"hyperevm"**
   - This is the only supported network for Project X

4. **Enter NFT ID**
   - Enter your Project X LP position NFT ID
   - This is the token ID from your position on HyperEVM

5. **Fetch Position Data**
   - Click "Fetch Position Data"
   - The system will connect to HyperEVM and retrieve:
     - Token pair (e.g., USDC/WETH)
     - Fee tier
     - Liquidity amount
     - Price ranges (pa, pb)
     - Current position value

6. **Configure Hedging** (Optional)
   - Select which tokens to hedge (token0, token1, or both)
   - Choose hedging strategy (static or dynamic)
   - Set target hedge ratio
   - Configure rebalance parameters

7. **Save Position**
   - Review the position details
   - Click "Save Position"
   - Your Project X position is now tracked!

## Technical Details

### Network Information
- **Network Name**: HyperEVM
- **Network ID**: hyperevm
- **RPC Endpoint**: https://lb.drpc.live/hyperliquid/AgabH9LLzU5spjPklruwaz9Ek6W6rmgR8LnvQrxF2MGT

### Contract Compatibility
Project X uses **Uniswap V3 compatible contracts**, which means:
- Position data structure is identical to Uniswap V3
- Fee tiers work the same way (100, 500, 3000, 10000 basis points)
- Tick-based price ranges use the same formulas
- Liquidity calculations are identical

### Supported Features
- ✅ Position tracking
- ✅ Real-time price monitoring
- ✅ Liquidity amount calculations
- ✅ Token balance tracking
- ✅ USD value calculations (via Hyperliquid price feeds)
- ✅ Automated hedging (if tokens are available on Hyperliquid)
- ✅ Dynamic hedging strategies
- ✅ Position editing and updates

## Example: Adding a USDC/WETH Position

Let's say you have a USDC/WETH LP position on Project X with NFT ID `12345`:

1. Select **Protocol**: "Project X"
2. **Network**: "hyperevm" (auto-selected)
3. **NFT ID**: `12345`
4. Click **"Fetch Position Data"**

The system will display:
```
Position: HyperEVM USDC/WETH Position #12345
Pool: 0x... (pool address)
Fee Tier: 3000 (0.3%)
Token0: USDC (amount: 1000.00)
Token1: WETH (amount: 0.5)
Current Price: $2000 per WETH
Price Range: $1800 - $2200
Position Value: ~$2000 USD
```

5. Configure hedging (optional):
   - Hedge token0 (USDC): No (stablecoin)
   - Hedge token1 (WETH): Yes
   - Target ratio: 80%

6. Click **"Save Position"**

## Hedging Considerations

### Token Mapping
For hedging to work, tokens must be available on Hyperliquid:
- **USDC**: Available as stablecoin (always $1.00)
- **WETH**: Available as ETH on Hyperliquid
- **Other tokens**: Check Hyperliquid availability

### Stablecoins
The system automatically recognizes stablecoins:
- USDC, USDT, DAI, FRAX
- These are valued at $1.00 for hedging calculations
- No need to hedge stablecoins (already delta-neutral)

### Custom Token Mapping
If a token on HyperEVM has a different symbol than on Hyperliquid:
- The system will attempt automatic mapping
- You may need to manually configure the hedge_tokens mapping
- Contact support if you encounter mapping issues

## Troubleshooting

### "Failed to fetch position data"
- **Check NFT ID**: Ensure the NFT ID is correct
- **Check ownership**: Verify you own this position
- **RPC issues**: The RPC endpoint may be rate-limited
- **Network connectivity**: Check your internet connection

### "Token not available for hedging"
- The token may not be listed on Hyperliquid
- Check available tokens at Hyperliquid's trading interface
- You can still track the position without hedging

### "Position already exists"
- Each NFT ID can only be added once per user
- Edit the existing position instead of creating a new one
- Use the "Edit" button on the existing position

## Advanced Features

### Dynamic Hedging
Project X positions support dynamic hedging:
- **Balanced**: Moderate adjustments based on market conditions
- **Aggressive**: Frequent rebalancing for tight delta control
- **Conservative**: Minimal rebalancing, lower trading costs

### Rebalance Settings
- **Cooldown Period**: Minimum time between rebalances (default: 8 hours)
- **Delta Drift Threshold**: Trigger rebalance when delta drifts by X% (default: 0.38%)
- **Max Hedge Drift**: Maximum allowed hedge position drift (default: 0.50%)

### Position Monitoring
Once saved, your Project X position will:
- Update prices in real-time
- Calculate current position value
- Track hedge status
- Monitor delta drift
- Trigger rebalances automatically (if enabled)

## Support

For issues specific to Project X integration:
1. Check the `PROJECT_X_INTEGRATION_SUMMARY.md` file
2. Run the test script: `python test_project_x_config.py`
3. Review logs for detailed error messages
4. Verify contract addresses match Project X documentation

## Comparison with Other Protocols

| Feature | Uniswap V3 | Aerodrome | Project X |
|---------|-----------|-----------|-----------|
| Networks | 5+ chains | Base only | HyperEVM only |
| Contract Type | Uniswap V3 | Aerodrome CL | Uniswap V3 |
| Fee Tiers | Standard | tickSpacing | Standard |
| Hedging | ✅ | ✅ | ✅ |
| Dynamic Hedging | ✅ | ✅ | ✅ |

Project X uses the same battle-tested Uniswap V3 contracts, ensuring reliability and compatibility with existing tools.

---

**Last Updated**: 2026-06-27  
**Version**: 1.0  
**Status**: Production Ready
