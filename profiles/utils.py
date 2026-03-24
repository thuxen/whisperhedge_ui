"""
Profile System - Validation Utilities

Strict validation for indicators and calculated configs.
Fails hard on any validation error to prevent trading with bad data.
NO fallbacks for live money - better to skip a run than use wrong settings.
"""

def validate_indicators(
    corr_7d: float,
    arv_7d: float,
    mrhl_hours: float,
    funding_rate_daily: float
) -> None:
    """
    Validate all indicators are present and in reasonable ranges.
    
    Args:
        corr_7d: 7-day log-return correlation
        arv_7d: 7-day annualized realized volatility (%)
        mrhl_hours: Mean reversion half-life (hours)
        funding_rate_daily: Daily funding rate (% per day)
        
    Raises:
        ValueError: If any indicator is missing or out of range
    """
    # Check for None/missing values
    if corr_7d is None:
        raise ValueError("Missing correlation (corr_7d) - cannot calculate hedge config")
    if arv_7d is None:
        raise ValueError("Missing ARV (arv_7d) - cannot calculate hedge config")
    if mrhl_hours is None:
        raise ValueError("Missing MRHL (mrhl_hours) - cannot calculate hedge config")
    if funding_rate_daily is None:
        raise ValueError("Missing funding rate (funding_rate_daily) - cannot calculate hedge config")
    
    # Check ranges
    if not (-1.0 <= corr_7d <= 1.0):
        raise ValueError(
            f"Invalid correlation: {corr_7d:.4f} (must be [-1.0, 1.0]). "
            f"Check indicator calculation or data source."
        )
    
    if not (0 <= arv_7d <= 500):
        raise ValueError(
            f"Invalid ARV: {arv_7d:.2f}% (must be [0, 500]). "
            f"Check indicator calculation or data source."
        )
    
    if not (0 <= mrhl_hours <= 1000):
        raise ValueError(
            f"Invalid MRHL: {mrhl_hours:.1f}h (must be [0, 1000]). "
            f"Check indicator calculation or data source."
        )
    
    if not (-1.0 <= funding_rate_daily <= 1.0):
        raise ValueError(
            f"Invalid funding rate: {funding_rate_daily:+.4f}% (must be [-1.0, 1.0]). "
            f"Check funding rate calculation or data source."
        )

def validate_config(config: dict) -> None:
    """
    Validate calculated config has all required fields and reasonable values.
    
    Args:
        config: Calculated hedge configuration dict
        
    Raises:
        ValueError: If any required field is missing or has invalid value
    """
    # Required fields
    required_fields = [
        'target_hedge_ratio',
        'delta_drift_threshold_pct',
        'rebalance_cooldown_hours',
        'down_threshold',
        'bounce_threshold',
        'lookback_hours',
        'max_hedge_drift_pct',
        'drift_min_pct_of_capital',
        'profile',
    ]
    
    # Check all required fields exist
    for field in required_fields:
        if field not in config:
            raise ValueError(
                f"Missing required field in config: '{field}'. "
                f"Profile calculation failed to produce complete config."
            )
        if config[field] is None:
            raise ValueError(
                f"Field '{field}' is None. "
                f"Profile calculation failed to produce valid value."
            )
    
    # Validate ranges for critical trading parameters
    ratio = config['target_hedge_ratio']
    if not (0.0 <= ratio <= 1.0):
        raise ValueError(
            f"Invalid hedge ratio: {ratio:.3f} (must be [0.0, 1.0]). "
            f"NEVER hedge more than 100% of LP capital. "
            f"Profile calculation produced unsafe value."
        )
    
    drift = config['delta_drift_threshold_pct']
    if not (0.05 <= drift <= 5.0):
        raise ValueError(
            f"Invalid drift threshold: {drift:.3f} (must be [0.05, 5.0]). "
            f"Profile calculation produced unsafe value."
        )
    
    cooldown = config['rebalance_cooldown_hours']
    if not (0.0 <= cooldown <= 168.0):  # Max 1 week
        raise ValueError(
            f"Invalid cooldown: {cooldown:.1f}h (must be [0.0, 168.0]). "
            f"Profile calculation produced unsafe value."
        )
    
    down = config['down_threshold']
    if not (-1.0 <= down <= 0.0):
        raise ValueError(
            f"Invalid down threshold: {down:.4f} (must be [-1.0, 0.0]). "
            f"Profile calculation produced unsafe value."
        )
    
    bounce = config['bounce_threshold']
    if not (-1.0 <= bounce <= 0.0):
        raise ValueError(
            f"Invalid bounce threshold: {bounce:.4f} (must be [-1.0, 0.0]). "
            f"Profile calculation produced unsafe value."
        )
    
    lookback = config['lookback_hours']
    if not (1 <= lookback <= 168):  # Max 1 week
        raise ValueError(
            f"Invalid lookback hours: {lookback} (must be [1, 168]). "
            f"Profile calculation produced unsafe value."
        )

def get_correlation_tier(corr_7d: float, tiers: list) -> float:
    """
    Get hedge ratio from correlation tiers.
    
    Args:
        corr_7d: 7-day log-return correlation
        tiers: List of (threshold, ratio) tuples
        
    Returns:
        Hedge ratio for the correlation tier
    """
    for threshold, ratio in tiers:
        if corr_7d >= threshold:
            return ratio
    # Return lowest tier as default
    return tiers[-1][1]

def apply_bounds(value: float, min_val: float, max_val: float) -> float:
    """
    Apply min/max bounds to value.
    
    Args:
        value: Value to bound
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        
    Returns:
        Bounded value
    """
    return max(min_val, min(max_val, value))
