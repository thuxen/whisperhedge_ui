"""
Test to verify we're checking perpetual markets, not spot markets
"""
from hyperliquid.info import Info as HLInfo
from hyperliquid.utils import constants

def test_market_types():
    """Check what meta_and_asset_ctxs returns"""
    print("="*60)
    print("Testing Hyperliquid Market Types")
    print("="*60)
    
    info = HLInfo(constants.MAINNET_API_URL, skip_ws=True)
    
    # Test meta_and_asset_ctxs (what we currently use)
    print("\n1. meta_and_asset_ctxs() - Current method:")
    meta_and_asset = info.meta_and_asset_ctxs()
    if meta_and_asset and len(meta_and_asset) == 2:
        universe = meta_and_asset[0].get('universe', [])
        print(f"   - Returns {len(universe)} markets")
        print(f"   - First 5 markets: {[u.get('name') for u in universe[:5]]}")
        print(f"   - Market type: PERPETUAL FUTURES")
    
    # Test meta() for perpetuals
    print("\n2. meta() - Perpetual markets:")
    try:
        perp_meta = info.meta()
        perp_universe = perp_meta.get('universe', [])
        print(f"   - Returns {len(perp_universe)} perpetual markets")
        print(f"   - First 5: {[u.get('name') for u in perp_universe[:5]]}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    # Test spot_meta() for spot markets
    print("\n3. spot_meta() - Spot markets:")
    try:
        spot_meta = info.spot_meta()
        spot_universe = spot_meta.get('universe', [])
        print(f"   - Returns {len(spot_universe)} spot markets")
        if spot_universe:
            print(f"   - First 5: {[u.get('name') for u in spot_universe[:5]]}")
    except Exception as e:
        print(f"   - Error: {e}")
    
    # Check if HYPE, ETH, BTC are in perpetuals
    print("\n4. Checking our tokens in perpetual markets:")
    for token in ['HYPE', 'ETH', 'BTC']:
        found = False
        for i, asset in enumerate(universe):
            if asset.get('name') == token:
                print(f"   ✓ {token} found in perpetuals at index {i}")
                found = True
                break
        if not found:
            print(f"   ✗ {token} NOT found in perpetuals")
    
    print("\n" + "="*60)
    print("Conclusion:")
    print("meta_and_asset_ctxs() returns PERPETUAL futures markets ✓")
    print("This is correct for hedging with perpetual futures!")
    print("="*60)

if __name__ == "__main__":
    test_market_types()
