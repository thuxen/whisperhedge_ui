"""
Simple test to verify token mappings are loaded correctly
"""
import json

def test_mappings():
    """Test that HyperEVM token mappings exist in the config"""
    print("=" * 60)
    print("Testing Token Mapping Configuration")
    print("=" * 60)
    
    with open('web_ui/token_mapping.json', 'r') as f:
        config = json.load(f)
    
    mappings = config.get('mappings', {})
    
    test_cases = [
        ("WHYPE", "HYPE"),
        ("UETH", "ETH"),
        ("UBTC", "BTC"),
    ]
    
    print("\nHyperEVM Token Mappings:")
    all_passed = True
    
    for pool_symbol, expected_hl_symbol in test_cases:
        actual = mappings.get(pool_symbol)
        if actual == expected_hl_symbol:
            print(f"  ✓ {pool_symbol} → {actual}")
        else:
            print(f"  ✗ {pool_symbol} → {actual} (expected {expected_hl_symbol})")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("All mappings configured correctly! ✓")
        print("\nThe system will now:")
        print("  1. Accept WHYPE/UETH positions from Project X")
        print("  2. Map WHYPE → HYPE for Hyperliquid hedging")
        print("  3. Map UETH → ETH for Hyperliquid hedging")
        print("  4. Map UBTC → BTC for Hyperliquid hedging")
    else:
        print("Some mappings are missing or incorrect!")
    print("=" * 60)

if __name__ == "__main__":
    test_mappings()
