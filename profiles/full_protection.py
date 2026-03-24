"""
Full Protection Profile - Maximum Capital Preservation

Very high hedge ratios (0.95-1.00) with tightest rebalancing and shortest cooldowns.
Pure capital preservation mode for market meltdowns - no upside capture focus.
Uses 7-day log-return correlation as primary indicator for hedge ratio,
with minimal adjustments to maintain maximum protection regardless of conditions.

Best for: Market crash scenarios, risk-off mode, pure capital preservation.
"""

# Profile metadata
PROFILE_NAME = 'full_protection'
PROFILE_DESCRIPTION = 'Maximum protection hedging for capital preservation in market meltdowns'

# ═══════════════════════════════════════════════════════════════════
# HEDGE RATIO CALCULATION
# ═══════════════════════════════════════════════════════════════════

# Correlation tiers - all tiers maintain near-perfect hedge
# Format: (min_correlation, hedge_ratio)
CORRELATION_TIERS = [
    (0.95, 1.00),  # Ultra-high correlation → 100% hedge
    (0.88, 1.00),  # Very high correlation → 100% hedge
    (0.78, 1.00),  # High correlation → 100% hedge
    (0.68, 0.98),  # Medium correlation → 98% hedge
    (0.55, 0.97),  # Low-medium correlation → 97% hedge
    (0.00, 0.95),  # Low correlation → 95% hedge (FLOOR)
]

# Hedge ratio constraints
HEDGE_RATIO_FLOOR = 0.95  # Never go below 95% hedge
HEDGE_RATIO_CAP = 1.00    # Cap at 100% (no over-hedging)

# MRHL trending adjustment (DISABLED for full protection)
MRHL_HEDGE_ADJUSTMENT = {
    'threshold': 999999,  # Effectively disabled - never reduce hedge
    'reduction': 0.00,    # No reduction
    'min_ratio': 0.95,    # Floor at 95%
}

# ARV-based rebalancing adjustments (minimal - protection is priority)
ARV_REBALANCING = {
    'high_threshold': 60,  # ARV >= 60% = high volatility
    'low_threshold': 25,   # ARV <= 25% = low volatility
    'high_arv': {
        'drift_multiplier': 1.1,    # Minimal widening
        'cooldown_multiplier': 1.2,  # Minimal lengthening
    },
    'low_arv': {
        'drift_multiplier': 0.90,   # Minimal tightening
        'cooldown_multiplier': 0.85, # Minimal shortening
    }
}

# ═══════════════════════════════════════════════════════════════════
# REBALANCING SETTINGS (DYNAMIC)
# ═══════════════════════════════════════════════════════════════════

# Funding-based rebalancing regimes (all tight for protection)
REBALANCING_REGIMES = {
    'aggressive': {  # Strong positive funding (≥ 0.12% daily)
        'delta_drift_threshold_pct': 0.20,  # Tightest
        'rebalance_cooldown_hours': 2.0,    # Shortest
        'funding_multiplier': 1.00,         # No boost needed - already at max
    },
    'mild_positive': {  # Mild positive funding (0.01% to 0.12% daily)
        'delta_drift_threshold_pct': 0.22,
        'rebalance_cooldown_hours': 3.0,
        'funding_multiplier': 1.00,
    },
    'normal': {  # Neutral funding (-0.04% to 0.01% daily)
        'delta_drift_threshold_pct': 0.25,
        'rebalance_cooldown_hours': 4.0,
        'funding_multiplier': 1.00,
    },
    'lazy': {  # Negative funding (< -0.04% daily)
        # Use correlation-based formulas (but keep tight)
        'use_correlation_formula': True,
        'drift_formula': lambda corr: max(0.20, 0.40 - 0.30 * corr),  # Tight range
        'cooldown_formula': lambda corr: max(2.0, 8.0 - 8.0 * corr),  # Short range
        'funding_multiplier': 1.00,  # No reduction - maintain protection
    }
}

# Funding thresholds for regime selection (daily %)
FUNDING_THRESHOLDS = {
    'aggressive': 0.12,      # >= 0.12% daily = strong positive
    'mild_positive': 0.01,   # >= 0.01% daily = mild positive
    'lazy': -0.04,           # < -0.04% daily = negative
}

# Pullback filter formulas (very tight - catch any downside)
PULLBACK_FORMULAS = {
    'down_threshold': lambda corr: -0.030,  # Fixed tight threshold
    'bounce_threshold': lambda corr: -0.015,  # Fixed tight threshold
    'lookback_hours': lambda corr: 4,  # Short lookback
}

# MRHL rebalancing overrides (minimal - maintain tight settings)
MRHL_REBALANCING_OVERRIDES = {
    'ultra_fast': {  # MRHL ≤ 2.0h
        'threshold': 2.0,
        'comparison': '<=',
        'overrides': {
            'delta_drift_threshold_pct': 0.18,  # Tightest
            'rebalance_cooldown_hours': 1.5,    # Shortest
            'down_threshold': -0.025,
            'bounce_threshold': -0.012,
            'lookback_hours': 3,
        }
    },
    'slow_trend': {  # MRHL ≥ 14.0h
        'threshold': 14.0,
        'comparison': '>=',
        'multipliers': {
            'delta_drift_threshold_pct': 1.3,  # Minimal widening
            'rebalance_cooldown_hours': 1.3,   # Minimal lengthening
        },
        'minimums': {
            'delta_drift_threshold_pct': 0.30,  # Tight floor
            'rebalance_cooldown_hours': 6.0,    # Short cap
        },
        'overrides': {
            'down_threshold': -0.035,
            'bounce_threshold': -0.020,
            'lookback_hours': 8,
        }
    }
}

# Safety parameters (tightest settings)
SAFETY_FORMULAS = {
    'max_hedge_drift_pct': lambda corr: 0.30,  # Fixed tight limit
    'drift_min_pct_of_capital': lambda corr: 0.05,  # Fixed sensitive threshold
}

# ARV-based drift cap (very tight)
ARV_DRIFT_CAP = {
    'threshold': 25.0,  # ARV <= 25% = very low volatility
    'max_drift': 0.35,  # Tightest cap
}

# Volume/TVL-based drift minimum (thin pool protection)
VOLUME_TVL_DRIFT_FLOOR = {
    'threshold': 3.0,   # volume_tvl_ratio < 3.0 = thin pool
    'min_drift': 0.08,  # Tight floor
}

# ═══════════════════════════════════════════════════════════════════
# CALCULATION FUNCTION
# ═══════════════════════════════════════════════════════════════════

def calculate(corr_7d: float, arv_7d: float, mrhl_hours: float, funding_rate_daily: float) -> dict:
    """
    Calculate hedge configuration for full protection profile.
    
    Args:
        corr_7d: 7-day log-return correlation
        arv_7d: 7-day annualized realized volatility (%)
        mrhl_hours: Mean reversion half-life (hours)
        funding_rate_daily: Daily funding rate (% per day)
        
    Returns:
        Dict with complete hedge configuration
    """
    # ═══════════════════════════════════════════════════════════════════
    # STEP 1: Get base ratio from correlation tier ONLY
    # ═══════════════════════════════════════════════════════════════════
    
    ratio = 0.95  # Default for very low correlation (FLOOR)
    for threshold, tier_ratio in CORRELATION_TIERS:
        if corr_7d >= threshold:
            ratio = tier_ratio
            break
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: NO MRHL trending adjustment (maintain maximum protection)
    # ═══════════════════════════════════════════════════════════════════
    
    # MRHL adjustment disabled for full protection - always maintain high hedge
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 3: Final cap at 1.00 (no over-hedging)
    # ═══════════════════════════════════════════════════════════════════
    
    ratio = min(1.00, ratio)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 4: Calculate rebalancing settings (minimal adjustments)
    # ═══════════════════════════════════════════════════════════════════
    
    # Determine funding regime
    if funding_rate_daily >= FUNDING_THRESHOLDS['aggressive']:
        regime = 'aggressive'
    elif funding_rate_daily >= FUNDING_THRESHOLDS['mild_positive']:
        regime = 'mild_positive'
    elif funding_rate_daily >= FUNDING_THRESHOLDS['lazy']:
        regime = 'normal'
    else:
        regime = 'lazy'
    
    # Get base rebalancing settings for regime
    regime_config = REBALANCING_REGIMES[regime]
    
    # NO funding multiplier adjustment - maintain 95-100% range
    funding_multiplier = regime_config.get('funding_multiplier', 1.0)
    ratio = ratio * funding_multiplier
    
    # Apply floor and cap to hedge ratio
    ratio = max(HEDGE_RATIO_FLOOR, min(HEDGE_RATIO_CAP, ratio))
    
    # Get rebalancing settings from regime
    if regime_config.get('use_correlation_formula'):
        delta_drift_threshold_pct = regime_config['drift_formula'](corr_7d)
        rebalance_cooldown_hours = regime_config['cooldown_formula'](corr_7d)
    else:
        delta_drift_threshold_pct = regime_config['delta_drift_threshold_pct']
        rebalance_cooldown_hours = regime_config['rebalance_cooldown_hours']
    
    # Apply minimal ARV adjustments
    if arv_7d >= ARV_REBALANCING['high_threshold']:
        # High volatility - minimal widening
        delta_drift_threshold_pct *= ARV_REBALANCING['high_arv']['drift_multiplier']
        rebalance_cooldown_hours *= ARV_REBALANCING['high_arv']['cooldown_multiplier']
    elif arv_7d <= ARV_REBALANCING['low_threshold']:
        # Low volatility - minimal tightening
        delta_drift_threshold_pct *= ARV_REBALANCING['low_arv']['drift_multiplier']
        rebalance_cooldown_hours *= ARV_REBALANCING['low_arv']['cooldown_multiplier']
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 5: Calculate pullback filter (very tight)
    # ═══════════════════════════════════════════════════════════════════
    
    down_threshold = PULLBACK_FORMULAS['down_threshold'](corr_7d)
    bounce_threshold = PULLBACK_FORMULAS['bounce_threshold'](corr_7d)
    lookback_hours = PULLBACK_FORMULAS['lookback_hours'](corr_7d)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 6: Apply MRHL rebalancing overrides (if applicable)
    # ═══════════════════════════════════════════════════════════════════
    
    mrhl_regime = None
    
    for regime_name, override_config in MRHL_REBALANCING_OVERRIDES.items():
        threshold = override_config['threshold']
        comparison = override_config['comparison']
        
        # Check if MRHL matches this override
        if comparison == '<=' and mrhl_hours <= threshold:
            mrhl_regime = regime_name
            # Apply overrides
            if 'overrides' in override_config:
                for key, value in override_config['overrides'].items():
                    if key == 'delta_drift_threshold_pct':
                        delta_drift_threshold_pct = value
                    elif key == 'rebalance_cooldown_hours':
                        rebalance_cooldown_hours = value
                    elif key == 'down_threshold':
                        down_threshold = value
                    elif key == 'bounce_threshold':
                        bounce_threshold = value
                    elif key == 'lookback_hours':
                        lookback_hours = value
            break
        
        elif comparison == '>=' and mrhl_hours >= threshold:
            mrhl_regime = regime_name
            # Apply multipliers
            if 'multipliers' in override_config:
                mult = override_config['multipliers']
                mins = override_config.get('minimums', {})
                
                if 'delta_drift_threshold_pct' in mult:
                    delta_drift_threshold_pct = max(
                        mins.get('delta_drift_threshold_pct', 0),
                        delta_drift_threshold_pct * mult['delta_drift_threshold_pct']
                    )
                
                if 'rebalance_cooldown_hours' in mult:
                    rebalance_cooldown_hours = max(
                        mins.get('rebalance_cooldown_hours', 0),
                        rebalance_cooldown_hours * mult['rebalance_cooldown_hours']
                    )
            
            # Apply overrides
            if 'overrides' in override_config:
                for key, value in override_config['overrides'].items():
                    if key == 'down_threshold':
                        down_threshold = value
                    elif key == 'bounce_threshold':
                        bounce_threshold = value
                    elif key == 'lookback_hours':
                        lookback_hours = value
            break
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 6.5: Apply ARV-based drift cap (very tight)
    # ═══════════════════════════════════════════════════════════════════
    
    if arv_7d <= ARV_DRIFT_CAP['threshold']:
        # Very low volatility - cap drift threshold (tightest)
        delta_drift_threshold_pct = min(delta_drift_threshold_pct, ARV_DRIFT_CAP['max_drift'])
    
    # Hard cap on drift threshold - always tight for protection
    delta_drift_threshold_pct = min(delta_drift_threshold_pct, 0.40)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 6.6: Apply hard cooldown cap (full protection profile)
    # ═══════════════════════════════════════════════════════════════════
    
    # Hard cap at 6h for full protection - shortest across all profiles
    rebalance_cooldown_hours = min(rebalance_cooldown_hours, 6.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 7: Calculate safety parameters (tightest settings)
    # ═══════════════════════════════════════════════════════════════════
    
    max_hedge_drift_pct = SAFETY_FORMULAS['max_hedge_drift_pct'](corr_7d)
    drift_min_pct_of_capital = SAFETY_FORMULAS['drift_min_pct_of_capital'](corr_7d)
    
    # ═══════════════════════════════════════════════════════════════════
    # FINAL CONFIG ASSEMBLY
    # ═══════════════════════════════════════════════════════════════════
    
    return {
        # Core hedge behavior - ALWAYS NEAR 100%
        'target_hedge_ratio': round(ratio, 3),
        
        # Rebalancing settings - TIGHTEST ACROSS ALL PROFILES
        'delta_drift_threshold_pct': round(delta_drift_threshold_pct, 3),
        'rebalance_cooldown_hours': round(rebalance_cooldown_hours, 1),
        
        # Pullback filter (very tight)
        'down_threshold': round(down_threshold, 4),
        'bounce_threshold': round(bounce_threshold, 4),
        'lookback_hours': int(lookback_hours),
        
        # Safety parameters (tightest)
        'max_hedge_drift_pct': round(max_hedge_drift_pct, 3),
        'drift_min_pct_of_capital': round(drift_min_pct_of_capital, 3),
        
        # Metadata
        'profile': PROFILE_NAME,
        'profile_description': PROFILE_DESCRIPTION,
        'funding_regime': regime,
        'mrhl_regime': mrhl_regime,
        'corr_7d': round(corr_7d, 3),
        'arv_7d': round(arv_7d, 2),
        'mrhl_hours': round(mrhl_hours, 1) if mrhl_hours else None,
        'funding_rate_daily': round(funding_rate_daily, 4),
    }
