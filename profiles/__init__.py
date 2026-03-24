"""
Profile System - Registry and Loader

Manages hedge configuration profiles with tiered correlation approach.
Each profile calculates hedge ratio and rebalancing settings dynamically
based on market indicators (correlation, volatility, mean reversion, funding).
"""

from typing import Dict, Callable

# Import profile calculation functions
from . import balanced, moderate_bullish, aggressive_bullish, moderate_bearish, full_protection

# Profile registry - maps profile names to calculation functions
PROFILES: Dict[str, Callable] = {
    'balanced': balanced.calculate,
    'moderate_bullish': moderate_bullish.calculate,
    'aggressive_bullish': aggressive_bullish.calculate,
    'moderate_bearish': moderate_bearish.calculate,
    'full_protection': full_protection.calculate,
}

# Explicit exports
__all__ = ['PROFILES', 'calculate_config', 'get_profile', 'list_profiles']

def get_profile(profile_name: str = 'balanced') -> Callable:
    """
    Get profile calculation function by name.
    
    Args:
        profile_name: Profile name (default: 'balanced')
        
    Returns:
        Profile calculation function
        
    Raises:
        ValueError: If profile name is unknown
    """
    if profile_name not in PROFILES:
        available = ', '.join(PROFILES.keys())
        raise ValueError(f"Unknown profile: '{profile_name}'. Available profiles: {available}")
    
    return PROFILES[profile_name]

def calculate_config(
    profile_name: str,
    corr_7d: float,
    arv_7d: float,
    mrhl_hours: float,
    funding_rate_daily: float
) -> dict:
    """
    Calculate hedge configuration for specified profile.
    
    Args:
        profile_name: Profile to use ('balanced', 'aggressive_bull', etc.)
        corr_7d: 7-day log-return correlation
        arv_7d: 7-day annualized realized volatility (%)
        mrhl_hours: Mean reversion half-life (hours)
        funding_rate_daily: Daily funding rate (% per day)
        
    Returns:
        Dict with complete hedge configuration including:
        - target_hedge_ratio
        - delta_drift_threshold_pct
        - rebalance_cooldown_hours
        - down_threshold, bounce_threshold, lookback_hours
        - max_hedge_drift_pct, drift_min_pct_of_capital
        - metadata (profile, regimes, input indicators)
        
    Raises:
        ValueError: If profile name is unknown or inputs are invalid
    """
    profile_func = get_profile(profile_name)
    return profile_func(corr_7d, arv_7d, mrhl_hours, funding_rate_daily)

def list_profiles() -> list:
    """
    Get list of available profile names.
    
    Returns:
        List of profile names
    """
    return list(PROFILES.keys())
