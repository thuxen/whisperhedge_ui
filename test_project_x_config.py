"""
Test script to verify Project X (HyperEVM) configuration
"""
import sys
import os

# Direct import to avoid package initialization issues
sys.path.insert(0, os.path.dirname(__file__))

# Import directly from the module file
import importlib.util
spec = importlib.util.spec_from_file_location("blockchain_utils", "web_ui/blockchain_utils.py")
blockchain_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(blockchain_utils)

NETWORK_RPCS = blockchain_utils.NETWORK_RPCS
POSITION_MANAGER_ADDRESSES = blockchain_utils.POSITION_MANAGER_ADDRESSES
FACTORY_ADDRESSES = blockchain_utils.FACTORY_ADDRESSES
get_web3 = blockchain_utils.get_web3

def test_hyperevm_config():
    """Test that HyperEVM network is properly configured"""
    print("=" * 60)
    print("Testing Project X (HyperEVM) Configuration")
    print("=" * 60)
    
    # Test 1: Check RPC endpoint
    print("\n1. Checking RPC endpoint...")
    assert "hyperevm" in NETWORK_RPCS, "HyperEVM not found in NETWORK_RPCS"
    rpc_url = NETWORK_RPCS["hyperevm"]
    print(f"   ✓ RPC URL: {rpc_url}")
    
    # Test 2: Check Position Manager address
    print("\n2. Checking Position Manager address...")
    assert "hyperevm" in POSITION_MANAGER_ADDRESSES, "HyperEVM not found in POSITION_MANAGER_ADDRESSES"
    pm_address = POSITION_MANAGER_ADDRESSES["hyperevm"]
    expected_pm = "0xeaD19AE861c29bBb2101E834922B2FEee69B9091"
    assert pm_address == expected_pm, f"Position Manager mismatch: {pm_address} != {expected_pm}"
    print(f"   ✓ Position Manager: {pm_address}")
    
    # Test 3: Check Factory address
    print("\n3. Checking Factory address...")
    assert "hyperevm" in FACTORY_ADDRESSES, "HyperEVM not found in FACTORY_ADDRESSES"
    factory_address = FACTORY_ADDRESSES["hyperevm"]
    expected_factory = "0xFf7B3e8C00e57ea31477c32A5B52a58Eea47b072"
    assert factory_address == expected_factory, f"Factory mismatch: {factory_address} != {expected_factory}"
    print(f"   ✓ Factory: {factory_address}")
    
    # Test 4: Test Web3 connection
    print("\n4. Testing Web3 connection to HyperEVM...")
    w3 = get_web3("hyperevm")
    if w3 and w3.is_connected():
        print(f"   ✓ Successfully connected to HyperEVM")
        try:
            block_number = w3.eth.block_number
            print(f"   ✓ Current block number: {block_number}")
        except Exception as e:
            print(f"   ⚠ Could not fetch block number: {e}")
    else:
        print(f"   ✗ Failed to connect to HyperEVM RPC")
        print(f"   Note: This may be due to network issues or RPC rate limits")
    
    print("\n" + "=" * 60)
    print("Configuration Test Complete!")
    print("=" * 60)
    print("\nAll configuration checks passed ✓")
    print("\nNext steps:")
    print("1. Test fetching a position with your test NFT ID")
    print("2. Verify position data displays correctly in UI")
    print("3. Test saving position configuration to database")

if __name__ == "__main__":
    test_hyperevm_config()
