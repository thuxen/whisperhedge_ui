"""
Test script to verify HyperEVM token mappings
"""
import sys
import os
import importlib.util

# Import hl_utils directly
spec = importlib.util.spec_from_file_location("hl_utils", "web_ui/hl_utils.py")
hl_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hl_utils)

def test_hyperevm_mappings():
    """Test that HyperEVM tokens map correctly to Hyperliquid symbols"""
    print("=" * 60)
    print("Testing HyperEVM Token Mappings")
    print("=" * 60)
    
    test_cases = [
        ("WHYPE", "HYPE"),
        ("UETH", "ETH"),
        ("UBTC", "BTC"),
    ]
    
    all_passed = True
    
    for pool_symbol, expected_hl_symbol in test_cases:
        print(f"\n{pool_symbol} → {expected_hl_symbol}")
        
        # Test metadata fetching
        metadata = hl_utils.get_hl_token_metadata(pool_symbol)
        
        if metadata:
            actual_hl_symbol = metadata.get('hl_symbol')
            if actual_hl_symbol == expected_hl_symbol:
                print(f"  ✓ Mapping correct: {pool_symbol} → {actual_hl_symbol}")
                print(f"  ✓ Price: ${metadata.get('price', 'N/A')}")
                print(f"  ✓ Decimals: {metadata.get('sz_decimals', 'N/A')}")
            else:
                print(f"  ✗ Mapping incorrect: expected {expected_hl_symbol}, got {actual_hl_symbol}")
                all_passed = False
        else:
            print(f"  ✗ Failed to fetch metadata for {pool_symbol}")
            print(f"  Note: This could mean {expected_hl_symbol} is not available on Hyperliquid")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All token mappings verified! ✓")
    else:
        print("Some mappings failed - check Hyperliquid availability")
    print("=" * 60)
    
    print("\nYou can now add Project X positions with these tokens:")
    print("  - WHYPE/UETH pools")
    print("  - WHYPE/UBTC pools")
    print("  - UETH/UBTC pools")
    print("  - Any combination with stablecoins (USDC, USDT, etc.)")

if __name__ == "__main__":
    test_hyperevm_mappings()
