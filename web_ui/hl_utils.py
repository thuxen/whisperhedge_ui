"""
Hyperliquid utility functions for the web UI
Copied from modulesv5/hyperliquid.py and core_hedger_v5.py
"""
from hyperliquid.info import Info as HLInfo
from hyperliquid.utils import constants
from typing import Optional, Dict
import requests
import json
import os


# Load token mapping from JSON config file
def _load_token_mapping() -> Dict[str, str]:
    """Load token symbol mapping from JSON config file"""
    config_path = os.path.join(os.path.dirname(__file__), 'token_mapping.json')
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get('mappings', {})
    except Exception as e:
        print(f"Warning: Could not load token_mapping.json: {e}")
        # Fallback to basic mappings
        return {
            'ETH': 'ETH', 'WETH': 'ETH',
            'BTC': 'BTC', 'WBTC': 'BTC',
            'LINK': 'LINK', 'ENA': 'ENA',
        }


TOKEN_TO_HL_SYMBOL = _load_token_mapping()


def get_hl_account_balance(wallet_address: str) -> Optional[Dict]:
    """
    Fetch Hyperliquid account balance to verify API key works
    Uses the same method as core_hedger_v5.py hl_get_user_state()
    
    Args:
        wallet_address: Wallet address to query
        
    Returns:
        Dict with balance info or None if error
    """
    try:
        # Initialize Info client (same as core_hedger)
        info = HLInfo(constants.MAINNET_API_URL, skip_ws=True)
        
        # Get user state (same as hl_get_user_state in modulesv5/hyperliquid.py)
        addr = wallet_address.lower()
        user_state = info.user_state(addr)
        
        if not user_state:
            return None
        
        # Extract balance info (same as core_hedger_v5.py lines 3948-3960)
        if 'marginSummary' not in user_state:
            return None
            
        margin = user_state['marginSummary']
        account_value = float(margin.get('accountValue', 0))
        margin_used = float(margin.get('totalMarginUsed', 0))
        notional_pos = float(margin.get('totalNtlPos', 0))
        
        try:
            available = account_value - margin_used
        except (ValueError, TypeError):
            available = 0.0
        
        return {
            'account_value': account_value,
            'margin_used': margin_used,
            'notional_pos': notional_pos,
            'available': available,
        }
        
    except Exception as e:
        # Handle different types of errors gracefully
        error_msg = str(e)
        if "422" in error_msg or "Failed to deserialize" in error_msg:
            # Invalid API key or wallet address - common with test data
            print(f"Invalid API key or wallet address - balance check failed")
        elif "JSONDecodeError" in error_msg:
            # API response parsing error
            print(f"API response error - unable to fetch balance")
        else:
            # Other unexpected errors
            print(f"Error fetching HL balance: {e}")
        return None


def get_hl_token_metadata(token_symbol: str) -> Optional[Dict]:
    """
    Get token metadata from Hyperliquid including price and decimals
    
    Args:
        token_symbol: Token symbol (e.g., 'WETH', 'WBTC', 'LINK')
        
    Returns:
        Dict with price, sz_decimals, hl_symbol or None if not found
    """
    try:
        # Map token symbol to Hyperliquid market symbol
        hl_symbol = TOKEN_TO_HL_SYMBOL.get(token_symbol.upper(), token_symbol.upper())
        
        info = HLInfo(constants.MAINNET_API_URL, skip_ws=True)
        
        # Get all market data
        meta_and_asset_ctxs = info.meta_and_asset_ctxs()
        if not meta_and_asset_ctxs or len(meta_and_asset_ctxs) != 2:
            return None
        
        universe = meta_and_asset_ctxs[0].get('universe', [])
        asset_ctxs = meta_and_asset_ctxs[1]
        
        # Find the token in the universe using mapped symbol
        for i, asset in enumerate(universe):
            if asset.get('name') == hl_symbol:
                metadata = {
                    'hl_symbol': hl_symbol,
                    'pool_symbol': token_symbol.upper(),
                    'sz_decimals': asset.get('szDecimals', 8),  # Default to 8 if not found
                    'price_decimals': 5,  # Hyperliquid uses 5 for most tokens
                    'price': None
                }
                
                # Get price if available
                if i < len(asset_ctxs):
                    mark_px = asset_ctxs[i].get('markPx')
                    if mark_px:
                        metadata['price'] = float(mark_px)
                
                return metadata
        
        return None
        
    except Exception as e:
        print(f"Error fetching HL metadata for {token_symbol} (mapped to {hl_symbol}): {e}")
        return None


def get_hl_token_price(token_symbol: str) -> Optional[float]:
    """
    Get token price from Hyperliquid
    
    Args:
        token_symbol: Token symbol (e.g., 'WETH', 'WBTC', 'LINK')
        
    Returns:
        Token price in USD or None if not found
    """
    metadata = get_hl_token_metadata(token_symbol)
    return metadata['price'] if metadata else None
