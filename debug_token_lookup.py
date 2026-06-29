"""
Debug script to see what's happening with token lookups
"""
import sys
import os
import importlib.util

# Import hl_utils directly
spec = importlib.util.spec_from_file_location("hl_utils", "web_ui/hl_utils.py")
hl_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hl_utils)

def debug_token_lookup(token_symbol):
    """Debug a single token lookup"""
    print(f"\n{'='*60}")
    print(f"Debugging: {token_symbol}")
    print('='*60)
    
    # Step 1: Load mapping
    print("\n1. Loading token mapping...")
    token_mapping = hl_utils._load_token_mapping()
    mapped_symbol = token_mapping.get(token_symbol.upper(), token_symbol.upper())
    print(f"   {token_symbol} → {mapped_symbol}")
    
    # Step 2: Try to get metadata
    print("\n2. Fetching Hyperliquid metadata...")
    try:
        from hyperliquid.info import Info as HLInfo
        from hyperliquid.utils import constants
        
        info = HLInfo(constants.MAINNET_API_URL, skip_ws=True)
        meta_and_asset_ctxs = info.meta_and_asset_ctxs()
        
        if not meta_and_asset_ctxs:
            print("   ✗ No data returned from Hyperliquid API")
            return
        
        if len(meta_and_asset_ctxs) != 2:
            print(f"   ✗ Unexpected response length: {len(meta_and_asset_ctxs)}")
            return
        
        universe = meta_and_asset_ctxs[0].get('universe', [])
        asset_ctxs = meta_and_asset_ctxs[1]
        
        print(f"   ✓ Got {len(universe)} markets from Hyperliquid")
        
        # Step 3: Search for the token
        print(f"\n3. Searching for '{mapped_symbol}' in Hyperliquid markets...")
        found = False
        for i, asset in enumerate(universe):
            if asset.get('name') == mapped_symbol:
                print(f"   ✓ Found {mapped_symbol} at index {i}")
                print(f"   - szDecimals: {asset.get('szDecimals')}")
                if i < len(asset_ctxs):
                    mark_px = asset_ctxs[i].get('markPx')
                    print(f"   - Price: ${mark_px}")
                found = True
                break
        
        if not found:
            print(f"   ✗ {mapped_symbol} not found in Hyperliquid markets")
            print(f"\n   Available markets (first 20):")
            for i, asset in enumerate(universe[:20]):
                print(f"     - {asset.get('name')}")
            if len(universe) > 20:
                print(f"     ... and {len(universe) - 20} more")
    
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    tokens = ["WHYPE", "UETH", "UBTC", "WETH", "WBTC"]
    
    for token in tokens:
        debug_token_lookup(token)
    
    print("\n" + "="*60)
    print("Debug complete")
    print("="*60)
