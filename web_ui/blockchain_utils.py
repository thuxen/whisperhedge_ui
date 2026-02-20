"""Utilities for fetching Uniswap V3 position data from blockchain"""
from web3 import Web3
from typing import Dict, Optional
import os
import math


# Network RPC endpoints
NETWORK_RPCS = {
    "ethereum": os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com"),
    "arbitrum": os.getenv("ARBITRUM_RPC", "https://arbitrum.llamarpc.com"),
    "base": os.getenv("BASE_RPC", "https://base.llamarpc.com"),
    "polygon": os.getenv("POLYGON_RPC", "https://polygon.llamarpc.com"),
    "optimism": os.getenv("OPTIMISM_RPC", "https://optimism.llamarpc.com"),
}

# Uniswap V3 NFT Position Manager addresses
POSITION_MANAGER_ADDRESSES = {
    "ethereum": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
    "arbitrum": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
    "base": "0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1",
    "polygon": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
    "optimism": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
}

# Minimal ABI for Uniswap V3 Position Manager
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

# Minimal ERC20 ABI for getting token symbols
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

# Uniswap V3 Pool ABI for getting pool address
POOL_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "token0", "type": "address"},
            {"internalType": "address", "name": "token1", "type": "address"},
            {"internalType": "uint24", "name": "fee", "type": "uint24"},
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]

# Uniswap V3 Factory addresses
FACTORY_ADDRESSES = {
    "ethereum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "arbitrum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "base": "0x33128a8fC17869897dcE68Ed026d694621f6FDfD",
    "polygon": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "optimism": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
}


def get_web3(network: str) -> Optional[Web3]:
    """Get Web3 instance for the specified network"""
    rpc_url = NETWORK_RPCS.get(network.lower())
    if not rpc_url:
        return None
    
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            print(f"Failed to connect to {network} RPC")
            return None
        return w3
    except Exception as e:
        print(f"Error connecting to {network}: {e}")
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
        print(f"Error getting token symbol for {token_address}: {e}")
        return token_address[:8]  # Return shortened address as fallback


def fee_to_percentage(fee: int) -> str:
    """Convert fee tier to integer basis points (not percentage string)"""
    # Return as string integer, not percentage
    return str(fee)


def tick_to_price(tick: int) -> float:
    """Convert Uniswap V3 tick to price"""
    return 1.0001 ** tick


def tick_to_sqrt_price_x96(tick: int) -> int:
    """Convert tick to sqrtPriceX96 using Uniswap V3 formula"""
    return int((1.0001 ** (tick / 2)) * (2 ** 96))


def calculate_amount0_from_liquidity(liquidity: int, sqrt_price_a_x96: int, sqrt_price_b_x96: int) -> int:
    """Calculate amount0 (token0) from liquidity using Uniswap V3 formula"""
    if sqrt_price_a_x96 > sqrt_price_b_x96:
        sqrt_price_a_x96, sqrt_price_b_x96 = sqrt_price_b_x96, sqrt_price_a_x96
    numerator = (liquidity << 96) * (sqrt_price_b_x96 - sqrt_price_a_x96)
    denominator = sqrt_price_b_x96 * sqrt_price_a_x96
    return numerator // denominator


def calculate_amount1_from_liquidity(liquidity: int, sqrt_price_a_x96: int, sqrt_price_b_x96: int) -> int:
    """Calculate amount1 (token1) from liquidity using Uniswap V3 formula"""
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
    """
    Calculate actual token amounts from raw Uniswap V3 liquidity.
    Uses proper Uniswap V3 formulas - this is the accurate method.
    Copied from modulesv5/lp_calculations.py
    
    Returns: (amount0, amount1) in human-readable units
    """
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


def compute_lp_state(p: float, L: float, pa: float, pb: float) -> tuple:
    """
    Compute LP position state (token amounts, value, delta) at a given price.
    Copied from modulesv5/lp_calculations.py
    
    Returns: (x, y, v, delta) where:
        - x: token0 amount
        - y: token1 amount
        - v: total value
        - delta: position delta
    """
    if p <= 0:
        return 0.0, 0.0, 0.0, 0.0

    sqrt_pa = math.sqrt(pa)
    sqrt_pb = math.sqrt(pb)
    sqrt_p = math.sqrt(p)

    if p < pa:
        y_full = L * (sqrt_pb - sqrt_pa)
        v = y_full
        return 0.0, y_full, v, 0.0
    elif p > pb:
        x_full = L * (1 / sqrt_pa - 1 / sqrt_pb)
        v = x_full * p
        return x_full, 0.0, v, x_full
    else:
        x = L * (1 / sqrt_p - 1 / sqrt_pb)
        y = L * (sqrt_p - sqrt_pa)
        v = x * p + y
        delta = x
        return x, y, v, delta


# Pool slot0 ABI for getting current price
POOL_SLOT0_ABI = [{
    "inputs": [],
    "name": "slot0",
    "outputs": [
        {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
        {"internalType": "int24", "name": "tick", "type": "int24"},
        {"internalType": "uint16", "name": "observationIndex", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinality", "type": "uint16"},
        {"internalType": "uint16", "name": "observationCardinalityNext", "type": "uint16"},
        {"internalType": "uint8", "name": "feeProtocol", "type": "uint8"},
        {"internalType": "bool", "name": "unlocked", "type": "bool"}
    ],
    "stateMutability": "view",
    "type": "function"
}]


async def fetch_uniswap_position(network: str, nft_id: str) -> Dict[str, str]:
    """
    Fetch Uniswap V3 position data from blockchain
    
    Args:
        network: Network name (ethereum, arbitrum, base, polygon, optimism)
        nft_id: NFT token ID
        
    Returns:
        Dictionary with position data
    """
    try:
        # Get Web3 instance
        w3 = get_web3(network)
        if not w3:
            raise Exception(f"Could not connect to {network} network")
        
        # Get position manager contract
        manager_address = POSITION_MANAGER_ADDRESSES.get(network.lower())
        if not manager_address:
            raise Exception(f"Position manager not found for {network}")
        
        position_manager = w3.eth.contract(
            address=Web3.to_checksum_address(manager_address),
            abi=POSITION_MANAGER_ABI
        )
        
        # Fetch position data
        position_data = position_manager.functions.positions(int(nft_id)).call()
        
        # Parse position data
        (nonce, operator, token0, token1, fee, tick_lower, tick_upper, 
         liquidity, fee_growth_0, fee_growth_1, tokens_owed_0, tokens_owed_1) = position_data
        
        # Get token info (symbol and decimals)
        token0_symbol = get_token_symbol(w3, token0)
        token1_symbol = get_token_symbol(w3, token1)
        
        # Get token decimals
        try:
            token0_contract = w3.eth.contract(address=Web3.to_checksum_address(token0), abi=ERC20_ABI)
            token0_decimals = token0_contract.functions.decimals().call()
        except:
            token0_decimals = 18
        
        try:
            token1_contract = w3.eth.contract(address=Web3.to_checksum_address(token1), abi=ERC20_ABI)
            token1_decimals = token1_contract.functions.decimals().call()
        except:
            token1_decimals = 18
        
        # Get pool address from factory
        factory_address = FACTORY_ADDRESSES.get(network.lower())
        if factory_address:
            factory = w3.eth.contract(
                address=Web3.to_checksum_address(factory_address),
                abi=POOL_ABI
            )
            pool_address = factory.functions.getPool(
                Web3.to_checksum_address(token0),
                Web3.to_checksum_address(token1),
                fee
            ).call()
        else:
            pool_address = "Unknown"
        
        # Format fee tier
        fee_tier = fee_to_percentage(fee)
        
        # Get pool's current price from slot0
        current_price = 0.0
        current_tick = 0
        sqrt_price_x96 = 0
        current_price_raw = 0
        try:
            pool_contract = w3.eth.contract(
                address=Web3.to_checksum_address(pool_address),
                abi=POOL_SLOT0_ABI
            )
            slot0 = pool_contract.functions.slot0().call()
            sqrt_price_x96 = slot0[0]
            current_tick = slot0[1]
            current_price_raw = (sqrt_price_x96 / (2**96)) ** 2
        except Exception as e:
            print(f"Error fetching pool price: {e}")
        
        # Adjust for token decimals - applies to current_price, pa, and pb
        decimal_adjustment = 10 ** (token1_decimals - token0_decimals)
        current_price = current_price_raw / decimal_adjustment
        
        # Calculate price bounds from ticks (adjusted for decimals)
        pa_raw = tick_to_price(tick_lower)
        pb_raw = tick_to_price(tick_upper)
        pa = pa_raw / decimal_adjustment
        pb = pb_raw / decimal_adjustment
        
        # Calculate actual token amounts using Uniswap V3 formulas
        token0_amount_actual = 0.0
        token1_amount_actual = 0.0
        if sqrt_price_x96 > 0:
            try:
                token0_amount_actual, token1_amount_actual = compute_lp_amounts_from_raw_liquidity(
                    raw_liquidity=liquidity,
                    current_tick=current_tick,
                    tick_lower=tick_lower,
                    tick_upper=tick_upper,
                    sqrt_price_x96=sqrt_price_x96,
                    token0_decimals=token0_decimals,
                    token1_decimals=token1_decimals
                )
            except Exception as e:
                print(f"Error calculating token amounts: {e}")
        
        base_result = {
            "network": network,
            "nft_id": nft_id,
            "pool_address": pool_address,
            "token0_symbol": token0_symbol,
            "token1_symbol": token1_symbol,
            "token0_decimals": token0_decimals,
            "token1_decimals": token1_decimals,
            "fee_tier": fee_tier,
            "position_name": f"{network.title()} {token0_symbol}/{token1_symbol} Position #{nft_id}",
            "liquidity": str(liquidity),
            "tick_lower": tick_lower,
            "tick_upper": tick_upper,
            "current_tick": current_tick,
            "current_price": current_price,
            "pa": pa,
            "pb": pb,
            "token0_amount": token0_amount_actual,
            "token1_amount": token1_amount_actual,
        }
        
        # Try to get USD values and metadata from Hyperliquid
        try:
            from .hl_utils import get_hl_token_metadata, is_stablecoin
            
            # Get token metadata from Hyperliquid (or use $1.00 for stablecoins)
            token0_metadata = get_hl_token_metadata(token0_symbol)
            token1_metadata = get_hl_token_metadata(token1_symbol)
            
            # Use $1.00 for stablecoins, HL price for volatile tokens
            if is_stablecoin(token0_symbol):
                token0_price_usd = 1.0
            else:
                token0_price_usd = token0_metadata['price'] if token0_metadata else None
            
            if is_stablecoin(token1_symbol):
                token1_price_usd = 1.0
            else:
                token1_price_usd = token1_metadata['price'] if token1_metadata else None
            
            # Convert pool price (token ratio) to USD
            current_price_usd = 0.0
            pa_usd = 0.0
            pb_usd = 0.0
            
            if token0_price_usd and token1_price_usd:
                # For pools like ENA/WETH, current_price is WETH per ENA (token1/token0)
                # To get USD price of ENA: current_price * WETH_price
                # To get USD price of WETH: just WETH_price
                current_price_usd = round(current_price * token1_price_usd, 4)  # Pool price in USD, rounded to 4 decimals
                pa_usd = round(pa * token1_price_usd, 2)  # Lower bound in USD
                pb_usd = round(pb * token1_price_usd, 2)  # Upper bound in USD
                
                # Round token amounts to Hyperliquid sz_decimals for cleaner display
                token0_sz_decimals = token0_metadata.get('sz_decimals', 8) if token0_metadata else 8
                token1_sz_decimals = token1_metadata.get('sz_decimals', 8) if token1_metadata else 8
                
                token0_amount_rounded = round(token0_amount_actual, token0_sz_decimals)
                token1_amount_rounded = round(token1_amount_actual, token1_sz_decimals)
                
                # Calculate USD values using ACTUAL Hyperliquid token prices (not pool ratios)
                token0_amount_usd = round(token0_amount_rounded * token0_price_usd, 2)
                token1_amount_usd = round(token1_amount_rounded * token1_price_usd, 2)
                position_value_usd = round(token0_amount_usd + token1_amount_usd, 2)
                
                # Calculate percentage allocation (rounded to 1 decimal place)
                token0_pct = round((token0_amount_usd / position_value_usd * 100), 1) if position_value_usd > 0 else 0.0
                token1_pct = round((token1_amount_usd / position_value_usd * 100), 1) if position_value_usd > 0 else 0.0
                
                # Calculate delta (for hedging) - this is just token0 amount for in-range positions
                delta = token0_amount_rounded if current_tick >= tick_lower and current_tick <= tick_upper else 0.0
                
                # Prepare hedge_tokens JSONB data
                hedge_tokens = {
                    "token0": {
                        "hl_symbol": token0_metadata.get('hl_symbol', '') if token0_metadata else '',
                        "pool_symbol": token0_symbol,
                        "sz_decimals": token0_sz_decimals,
                        "price_decimals": token0_metadata.get('price_decimals', 5) if token0_metadata else 5
                    },
                    "token1": {
                        "hl_symbol": token1_metadata.get('hl_symbol', '') if token1_metadata else '',
                        "pool_symbol": token1_symbol,
                        "sz_decimals": token1_sz_decimals,
                        "price_decimals": token1_metadata.get('price_decimals', 5) if token1_metadata else 5
                    }
                }
                
                base_result.update({
                    "token0_amount": token0_amount_rounded,  # Rounded to HL decimals
                    "token1_amount": token1_amount_rounded,  # Rounded to HL decimals
                    "token0_price_usd": token0_price_usd,
                    "token1_price_usd": token1_price_usd,
                    "current_price_usd": current_price_usd,
                    "pa_usd": pa_usd,
                    "pb_usd": pb_usd,
                    "token0_amount_usd": token0_amount_usd,
                    "token1_amount_usd": token1_amount_usd,
                    "token0_pct": token0_pct,  # Rounded to 1 decimal
                    "token1_pct": token1_pct,  # Rounded to 1 decimal
                    "position_value_usd": position_value_usd,
                    "delta": delta,
                    "hl_price_available": True,
                    "hedge_tokens": hedge_tokens,  # JSONB data for database
                    "in_range": current_tick >= tick_lower and current_tick <= tick_upper,
                })
            else:
                # Missing prices for non-stablecoin tokens
                # This should be rare since validation blocks unavailable tokens
                missing_tokens = []
                if not token0_price_usd and not is_stablecoin(token0_symbol):
                    missing_tokens.append(token0_symbol)
                if not token1_price_usd and not is_stablecoin(token1_symbol):
                    missing_tokens.append(token1_symbol)
                
                base_result.update({
                    "hl_price_available": False,
                    "hl_price_error": f"Price unavailable for: {', '.join(missing_tokens)}" if missing_tokens else "Price data unavailable",
                })
        except Exception as e:
            print(f"Error fetching HL prices: {e}")
            base_result.update({
                "hl_price_available": False,
                "hl_price_error": f"Error: {str(e)}",
            })
        
        return base_result
        
    except Exception as e:
        raise Exception(f"Error fetching position data: {str(e)}")
