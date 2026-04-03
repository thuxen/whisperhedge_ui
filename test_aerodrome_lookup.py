"""
Standalone test script for Aerodrome Slipstream position lookup
Tests fetching position data from Aerodrome on Base network
"""
from web3 import Web3
from typing import Dict, Optional
import os
import math
import asyncio

# Test Configuration
TEST_NFT_ID = "63301904"
TEST_NETWORK = "base"
TEST_PROTOCOL = "aerodrome_slipstream"

# Network RPC - using paid drpc endpoint for testing
BASE_RPC = "https://lb.drpc.live/base/AgabH9LLzU5spjPklruwaz9Ek6W6rmgR8LnvQrxF2MGT"

# Aerodrome Slipstream Contract Addresses (Base)
AERODROME_POSITION_MANAGER = "0x827922686190790b37229fd06084350E74485b72"
AERODROME_FACTORY = "0x5e7BB104d84c7CB9B682AaC2F3d509f5F406809A"

# Minimal ABI for Position Manager (same as Uniswap V3)
POSITION_MANAGER_ABI = [
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "positions",
        "outputs": [
            {"internalType": "uint96", "name": "nonce", "type": "uint96"},
            {"internalType": "address", "name": "operator", "type": "address"},
            {"internalType": "address", "name": "token0", "type": "address"},
            {"internalType": "address", "name": "token1", "type": "address"},
            {"internalType": "uint24", "name": "fee", "type": "uint24"},
            {"internalType": "int24", "name": "tickLower", "type": "int24"},
            {"internalType": "int24", "name": "tickUpper", "type": "int24"},
            {"internalType": "uint128", "name": "liquidity", "type": "uint128"},
            {"internalType": "uint256", "name": "feeGrowthInside0LastX128", "type": "uint256"},
            {"internalType": "uint256", "name": "feeGrowthInside1LastX128", "type": "uint256"},
            {"internalType": "uint128", "name": "tokensOwed0", "type": "uint128"},
            {"internalType": "uint128", "name": "tokensOwed1", "type": "uint128"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

# ERC20 ABI for token info
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

# Aerodrome Factory ABI - uses tickSpacing instead of fee
AERODROME_FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
            {"internalType": "int24", "name": "tickSpacing", "type": "int24"},
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

# Fee tier to tick spacing mapping for Aerodrome
FEE_TO_TICK_SPACING = {
    100: 1,      # 0.01% -> tickSpacing 1
    500: 10,     # 0.05% -> tickSpacing 10
    3000: 60,    # 0.3% -> tickSpacing 60
    10000: 200,  # 1% -> tickSpacing 200
}

# Aerodrome Pool slot0 ABI - DIFFERENT from Uniswap V3 (no feeProtocol field)
# Source: https://github.com/aerodrome-finance/slipstream/blob/main/contracts/core/CLPool.sol
POOL_SLOT0_ABI = [{
    "inputs": [],
    "name": "slot0",
    "outputs": [
        {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
        {"internalType": "int24", "name": "tick", "type": "int24"},
        {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
        {"internalType": "bool", "name": "unlocked", "type": "bool"}
    ],
    "stateMutability": "view",
    "type": "function"
}]


# Helper Functions (copied from blockchain_utils.py)

def get_web3() -> Optional[Web3]:
    """Get Web3 instance for Base network"""
    try:
        w3 = Web3(Web3.HTTPProvider(BASE_RPC))
        if not w3.is_connected():
            print(f"❌ Failed to connect to Base RPC")
            return None
        return w3
    except Exception as e:
        print(f"❌ Error connecting to Base: {e}")
        return None


def get_token_symbol(w3: Web3, token_address: str) -> str:
    """Get token symbol from contract"""
    try:
        token_contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )
        symbol = token_contract.functions.symbol().call()
        return symbol
    except Exception as e:
        print(f"⚠️  Error getting token symbol for {token_address}: {e}")
        return token_address[:8]


def get_token_decimals(w3: Web3, token_address: str) -> int:
    """Get token decimals from contract"""
    try:
        token_contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=ERC20_ABI
        )
        decimals = token_contract.functions.decimals().call()
        return decimals
    except Exception as e:
        print(f"⚠️  Error getting token decimals for {token_address}: {e}")
        return 18


def tick_to_price(tick: int) -> float:
    """Convert Uniswap V3 tick to price"""
    return 1.0001 ** tick


def tick_to_sqrt_price_x96(tick: int) -> int:
    """Convert tick to sqrtPriceX96"""
    return int((1.0001 ** (tick / 2)) * (2 ** 96))


def calculate_amount0_from_liquidity(liquidity: int, sqrt_price_a_x96: int, sqrt_price_b_x96: int) -> int:
    """Calculate amount0 from liquidity"""
    if sqrt_price_a_x96 > sqrt_price_b_x96:
        sqrt_price_a_x96, sqrt_price_b_x96 = sqrt_price_b_x96, sqrt_price_a_x96
    numerator = (liquidity << 96) * (sqrt_price_b_x96 - sqrt_price_a_x96)
    denominator = sqrt_price_b_x96 * sqrt_price_a_x96
    return numerator // denominator


def calculate_amount1_from_liquidity(liquidity: int, sqrt_price_a_x96: int, sqrt_price_b_x96: int) -> int:
    """Calculate amount1 from liquidity"""
    if sqrt_price_a_x96 > sqrt_price_b_x96:
        sqrt_price_a_x96, sqrt_price_b_x96 = sqrt_price_b_x96, sqrt_price_a_x96
    return (liquidity * (sqrt_price_b_x96 - sqrt_price_a_x96)) >> 96


def compute_lp_amounts_from_raw_liquidity(
    raw_liquidity: int,
    current_tick: int,
    tick_lower: int,
    tick_upper: int,
    sqrt_price_x96: int,
    token0_decimals: int,
    token1_decimals: int
) -> tuple:
    """Calculate actual token amounts from raw liquidity"""
    sqrt_price_lower_x96 = tick_to_sqrt_price_x96(tick_lower)
    sqrt_price_upper_x96 = tick_to_sqrt_price_x96(tick_upper)
    sqrt_price_current_x96 = sqrt_price_x96
    
    token0_amount_raw = 0
    token1_amount_raw = 0
    
    if current_tick < tick_lower:
        # Position is entirely in token0
        token0_amount_raw = calculate_amount0_from_liquidity(raw_liquidity, sqrt_price_lower_x96, sqrt_price_upper_x96)
    elif current_tick > tick_upper:
        # Position is entirely in token1
        token1_amount_raw = calculate_amount1_from_liquidity(raw_liquidity, sqrt_price_lower_x96, sqrt_price_upper_x96)
    else:
        # Position is in range
        token0_amount_raw = calculate_amount0_from_liquidity(raw_liquidity, sqrt_price_current_x96, sqrt_price_upper_x96)
        token1_amount_raw = calculate_amount1_from_liquidity(raw_liquidity, sqrt_price_lower_x96, sqrt_price_current_x96)
    
    # Convert to human-readable amounts
    token0_amount = token0_amount_raw / (10 ** token0_decimals)
    token1_amount = token1_amount_raw / (10 ** token1_decimals)
    
    return token0_amount, token1_amount


def fetch_aerodrome_position(nft_id: str) -> Dict:
    """
    Fetch Aerodrome Slipstream position data from Base blockchain
    """
    print(f"\n{'='*60}")
    print(f"🔍 Aerodrome Position Lookup Test")
    print(f"{'='*60}")
    print(f"NFT ID: {nft_id}")
    print(f"Network: Base")
    print(f"Protocol: Aerodrome Slipstream")
    print(f"{'='*60}\n")
    
    # Get Web3 instance
    print("📡 Connecting to Base network...")
    w3 = get_web3()
    if not w3:
        raise Exception("Could not connect to Base network")
    print("✅ Connected to Base\n")
    
    # Get position manager contract
    print("📋 Loading Aerodrome Position Manager contract...")
    position_manager = w3.eth.contract(
        address=Web3.to_checksum_address(AERODROME_POSITION_MANAGER),
        abi=POSITION_MANAGER_ABI
    )
    print(f"✅ Contract loaded: {AERODROME_POSITION_MANAGER}\n")
    
    # Fetch position data
    print(f"🔎 Fetching position #{nft_id}...")
    try:
        position_data = position_manager.functions.positions(int(nft_id)).call()
    except Exception as e:
        raise Exception(f"Failed to fetch position: {e}")
    
    # Parse position data
    (nonce, operator, token0, token1, fee, tick_lower, tick_upper, 
     liquidity, fee_growth_0, fee_growth_1, tokens_owed_0, tokens_owed_1) = position_data
    
    print("✅ Position data fetched\n")
    
    # Get token info
    print("🪙 Fetching token information...")
    token0_symbol = get_token_symbol(w3, token0)
    token1_symbol = get_token_symbol(w3, token1)
    token0_decimals = get_token_decimals(w3, token0)
    token1_decimals = get_token_decimals(w3, token1)
    print(f"  Token0: {token0_symbol} (decimals: {token0_decimals})")
    print(f"  Token1: {token1_symbol} (decimals: {token1_decimals})\n")
    
    # Get pool address - Aerodrome uses tickSpacing instead of fee
    print("🏊 Fetching pool address...")
    
    # Convert fee to tickSpacing
    tick_spacing = FEE_TO_TICK_SPACING.get(fee)
    if not tick_spacing:
        raise Exception(f"Unknown fee tier {fee} - cannot determine tickSpacing")
    
    print(f"  Fee tier: {fee} ({fee/10000:.2f}%) -> tickSpacing: {tick_spacing}")
    
    factory = w3.eth.contract(
        address=Web3.to_checksum_address(AERODROME_FACTORY),
        abi=AERODROME_FACTORY_ABI
    )
    pool_address = factory.functions.getPool(
        Web3.to_checksum_address(token0),
        Web3.to_checksum_address(token1),
        tick_spacing
    ).call()
    print(f"✅ Pool: {pool_address}\n")
    
    # Get current price from pool
    print("💹 Fetching current pool price...")
    pool_contract = w3.eth.contract(
        address=Web3.to_checksum_address(pool_address),
        abi=POOL_SLOT0_ABI
    )
    slot0 = pool_contract.functions.slot0().call()
    sqrt_price_x96 = slot0[0]
    current_tick = slot0[1]
    current_price_raw = (sqrt_price_x96 / (2**96)) ** 2
    
    # Adjust for token decimals
    decimal_adjustment = 10 ** (token1_decimals - token0_decimals)
    current_price = current_price_raw / decimal_adjustment
    
    print(f"✅ Current tick: {current_tick}")
    print(f"✅ Current price: {current_price:.6f} {token1_symbol}/{token0_symbol}\n")
    
    # Calculate price bounds
    pa_raw = tick_to_price(tick_lower)
    pb_raw = tick_to_price(tick_upper)
    pa = pa_raw / decimal_adjustment
    pb = pb_raw / decimal_adjustment
    
    # Calculate token amounts
    print("🧮 Calculating token amounts...")
    token0_amount, token1_amount = compute_lp_amounts_from_raw_liquidity(
        raw_liquidity=liquidity,
        current_tick=current_tick,
        tick_lower=tick_lower,
        tick_upper=tick_upper,
        sqrt_price_x96=sqrt_price_x96,
        token0_decimals=token0_decimals,
        token1_decimals=token1_decimals
    )
    print(f"✅ Token amounts calculated\n")
    
    # Check if in range
    in_range = current_tick >= tick_lower and current_tick <= tick_upper
    
    # Get USD values and hedge_tokens from Hyperliquid
    token0_price_usd = None
    token1_price_usd = None
    position_value_usd = None
    hedge_tokens = None
    
    try:
        import sys
        sys.path.insert(0, '/home/deltree/projects/whisperhedge_ui')
        from web_ui.hl_utils import get_hl_token_metadata, is_stablecoin
        
        print("💵 Fetching USD prices and HL metadata from Hyperliquid...")
        
        # Get token metadata (this uses the token mapping)
        token0_meta = None
        token1_meta = None
        
        if is_stablecoin(token0_symbol):
            token0_price_usd = 1.0
            print(f"  {token0_symbol}: $1.00 (stablecoin)")
        else:
            token0_meta = get_hl_token_metadata(token0_symbol)
            if token0_meta:
                token0_price_usd = token0_meta['price']
                print(f"  {token0_symbol} → {token0_meta['hl_symbol']}: ${token0_price_usd:.4f}")
            else:
                print(f"  {token0_symbol}: Not available on Hyperliquid")
        
        if is_stablecoin(token1_symbol):
            token1_price_usd = 1.0
            print(f"  {token1_symbol}: $1.00 (stablecoin)")
        else:
            token1_meta = get_hl_token_metadata(token1_symbol)
            if token1_meta:
                token1_price_usd = token1_meta['price']
                print(f"  {token1_symbol} → {token1_meta['hl_symbol']}: ${token1_price_usd:.4f}")
            else:
                print(f"  {token1_symbol}: Not available on Hyperliquid")
        
        # Build hedge_tokens JSONB structure (required for backend hedging)
        hedge_tokens = {
            "token0": {
                "hl_symbol": token0_meta.get('hl_symbol', '') if token0_meta else '',
                "pool_symbol": token0_symbol,
                "sz_decimals": token0_meta.get('sz_decimals', 8) if token0_meta else 8,
                "price_decimals": token0_meta.get('price_decimals', 5) if token0_meta else 5
            },
            "token1": {
                "hl_symbol": token1_meta.get('hl_symbol', '') if token1_meta else '',
                "pool_symbol": token1_symbol,
                "sz_decimals": token1_meta.get('sz_decimals', 8) if token1_meta else 8,
                "price_decimals": token1_meta.get('price_decimals', 5) if token1_meta else 5
            }
        }
        print(f"✅ hedge_tokens JSONB built\n")
        
        # Calculate USD values
        if token0_price_usd and token1_price_usd:
            token0_value_usd = token0_amount * token0_price_usd
            token1_value_usd = token1_amount * token1_price_usd
            position_value_usd = token0_value_usd + token1_value_usd
            print(f"✅ USD values calculated: ${position_value_usd:,.2f}\n")
        else:
            print(f"⚠️  Cannot calculate USD values - missing prices\n")
    except Exception as e:
        print(f"⚠️  Could not fetch Hyperliquid prices: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Return structured data
    return {
        "nft_id": nft_id,
        "network": "base",
        "protocol": "aerodrome_slipstream",
        "pool_address": pool_address,
        "token0_address": token0,
        "token1_address": token1,
        "token0_symbol": token0_symbol,
        "token1_symbol": token1_symbol,
        "token0_decimals": token0_decimals,
        "token1_decimals": token1_decimals,
        "fee_tier": fee,
        "tick_lower": tick_lower,
        "tick_upper": tick_upper,
        "current_tick": current_tick,
        "liquidity": liquidity,
        "current_price": current_price,
        "price_lower": pa,
        "price_upper": pb,
        "token0_amount": token0_amount,
        "token1_amount": token1_amount,
        "in_range": in_range,
        "token0_price_usd": token0_price_usd,
        "token1_price_usd": token1_price_usd,
        "position_value_usd": position_value_usd,
        "hedge_tokens": hedge_tokens,  # JSONB structure for backend hedging
    }


def print_results(data: Dict):
    """Print formatted results"""
    print(f"\n{'='*60}")
    print(f"📊 POSITION SUMMARY")
    print(f"{'='*60}\n")
    
    print(f"🆔 Position Details:")
    print(f"  NFT ID: {data['nft_id']}")
    print(f"  Network: {data['network'].title()}")
    print(f"  Protocol: {data['protocol'].replace('_', ' ').title()}")
    print(f"  Pool: {data['pool_address']}")
    print(f"  Fee Tier: {data['fee_tier']} ({data['fee_tier']/10000:.2f}%)\n")
    
    print(f"🪙 Tokens:")
    print(f"  Token0: {data['token0_symbol']} ({data['token0_address']})")
    print(f"  Token1: {data['token1_symbol']} ({data['token1_address']})\n")
    
    print(f"📈 Liquidity & Range:")
    print(f"  Liquidity: {data['liquidity']:,}")
    print(f"  Tick Lower: {data['tick_lower']}")
    print(f"  Tick Upper: {data['tick_upper']}")
    print(f"  Current Tick: {data['current_tick']}")
    print(f"  In Range: {'✅ Yes' if data['in_range'] else '❌ No'}\n")
    
    print(f"💰 Token Amounts:")
    print(f"  {data['token0_symbol']}: {data['token0_amount']:.6f}")
    print(f"  {data['token1_symbol']}: {data['token1_amount']:.6f}\n")
    
    print(f"💹 Prices ({data['token1_symbol']}/{data['token0_symbol']}):")
    print(f"  Current: {data['current_price']:.6f}")
    print(f"  Lower Bound: {data['price_lower']:.6f}")
    print(f"  Upper Bound: {data['price_upper']:.6f}\n")
    
    if data['position_value_usd']:
        print(f"💵 USD Values:")
        print(f"  {data['token0_symbol']} Price: ${data['token0_price_usd']:.4f}")
        print(f"  {data['token1_symbol']} Price: ${data['token1_price_usd']:.4f}")
        print(f"  {data['token0_symbol']} Value: ${data['token0_amount'] * data['token0_price_usd']:,.2f}")
        print(f"  {data['token1_symbol']} Value: ${data['token1_amount'] * data['token1_price_usd']:,.2f}")
        print(f"  Total Position: ${data['position_value_usd']:,.2f}\n")
    else:
        print(f"💵 USD Values: Not available\n")
    
    if data.get('hedge_tokens'):
        print(f"🔗 Hedge Token Mapping (for backend):")
        ht = data['hedge_tokens']
        print(f"  Token0: {ht['token0']['pool_symbol']} → HL:{ht['token0']['hl_symbol']} (sz_dec:{ht['token0']['sz_decimals']})")
        print(f"  Token1: {ht['token1']['pool_symbol']} → HL:{ht['token1']['hl_symbol']} (sz_dec:{ht['token1']['sz_decimals']})\n")
    
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        # Fetch position data
        position_data = fetch_aerodrome_position(TEST_NFT_ID)
        
        # Print results
        print_results(position_data)
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
