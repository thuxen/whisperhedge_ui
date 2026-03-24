"""
Balanced Profile - Base Hedge Configuration

Default tiered correlation approach with dynamic rebalancing settings.
Uses 7-day log-return correlation as primary indicator for hedge ratio,
with adjustments based on volatility (ARV), mean reversion (MRHL), and funding rates.

All rebalancing settings (drift thresholds, cooldowns, pullback filters) are
calculated dynamically based on market conditions to work across all position types.
"""

# Profile metadata
PROFILE_NAME = 'balanced'
PROFILE_DESCRIPTION = 'Balanced hedging with standard correlation tiers and dynamic rebalancing'

# ═══════════════════════════════════════════════════════════════════
# HEDGE RATIO CALCULATION
# ═══════════════════════════════════════════════════════════════════

# Correlation tiers - base hedge ratio
# Format: (min_correlation, hedge_ratio)
CORRELATION_TIERS = [
    (0.95, 0.98),  # Ultra-high correlation → 98% hedge
    (0.88, 0.95),  # Very high correlation → 95% hedge
    (0.78, 0.90),  # High correlation → 90% hedge
    (0.68, 0.72),  # Medium correlation → 72% hedge
    (0.55, 0.58),  # Low-medium correlation → 58% hedge
    (0.00, 0.45),  # Low correlation → 45% hedge (FLOOR)
]

# Hedge ratio constraints
HEDGE_RATIO_FLOOR = 0.45  # Never go below 45% hedge (max 55% long exposure)
HEDGE_RATIO_CAP = 1.00    # Never over-hedge

# MRHL trending adjustment (ONLY adjustment that affects hedge ratio)
MRHL_HEDGE_ADJUSTMENT = {
    'threshold': 120,  # MRHL > 120h = trending market
    'reduction': 0.12,  # Reduce by 12% (middle of 8-15% range)
    'min_ratio': 0.45,  # Never go below 45% (updated from 0.40)
}

# ARV-based rebalancing adjustments (affects rebalancing settings, NOT hedge ratio)
ARV_REBALANCING = {
    'high_threshold': 60,  # ARV >= 60% = high volatility
    'low_threshold': 25,   # ARV <= 25% = low volatility
    'high_arv': {
        'drift_multiplier': 1.3,    # Widen threshold by 30%
        'cooldown_multiplier': 1.5,  # Lengthen cooldown by 50%
    },
    'low_arv': {
        'drift_multiplier': 0.85,   # Tighten threshold by 15%
        'cooldown_multiplier': 0.75, # Shorten cooldown by 25%
    }
}

# ═══════════════════════════════════════════════════════════════════
# REBALANCING SETTINGS (DYNAMIC)
# ═══════════════════════════════════════════════════════════════════

# Funding-based rebalancing regimes
REBALANCING_REGIMES = {
    'aggressive': {  # Strong positive funding (≥ 0.12% daily)
        'delta_drift_threshold_pct': 0.30,
        'rebalance_cooldown_hours': 4.0,
        'funding_multiplier': 1.50,  # 50% boost to hedge ratio
    },
    'mild_positive': {  # Mild positive funding (0.01% to 0.12% daily) - NEW
        'delta_drift_threshold_pct': 0.38,
        'rebalance_cooldown_hours': 8.0,
        'funding_multiplier': 1.10,  # 10% boost to hedge ratio
    },
    'normal': {  # Neutral funding (-0.04% to 0.01% daily)
        'delta_drift_threshold_pct': 0.38,
        'rebalance_cooldown_hours': 8.0,
        'funding_multiplier': 1.00,  # No adjustment
    },
    'lazy': {  # Negative funding (< -0.04% daily)
        # Use correlation-based formulas
        'use_correlation_formula': True,
        'drift_formula': lambda corr: max(0.80, 1.8 - 2.0 * corr),
        'cooldown_formula': lambda corr: max(12.0, 32.0 - 32.0 * corr),
        'funding_multiplier': 0.50,  # 50% reduction to hedge ratio
    }
}

# Funding thresholds for regime selection (daily %)
FUNDING_THRESHOLDS = {
    'aggressive': 0.12,      # >= 0.12% daily = strong positive
    'mild_positive': 0.01,   # >= 0.01% daily = mild positive (NEW)
    'lazy': -0.04,           # < -0.04% daily = negative
}

# Pullback filter formulas (correlation-based)
PULLBACK_FORMULAS = {
    'down_threshold': lambda corr: min(-0.01, max(-0.25, -0.065 - 0.40 * (0.75 - corr))),
    'bounce_threshold': lambda corr: min(-0.005, max(-0.25, -0.038 - 0.25 * (0.75 - corr))),
    'lookback_hours': lambda corr: int(max(1, min(24, 7 + 40 * (0.75 - corr)))),
}

# MRHL rebalancing overrides (affects rebalancing settings, NOT hedge ratio)
MRHL_REBALANCING_OVERRIDES = {
    'ultra_fast': {  # MRHL ≤ 2.0h
        'threshold': 2.0,
        'comparison': '<=',
        'overrides': {
            'delta_drift_threshold_pct': 0.25,
            'rebalance_cooldown_hours': 2.0,
            'down_threshold': -0.040,
            'bounce_threshold': -0.025,
            'lookback_hours': 6,
        }
    },
    'slow_trend': {  # MRHL ≥ 14.0h
        'threshold': 14.0,
        'comparison': '>=',
        'multipliers': {
            'delta_drift_threshold_pct': 2.2,
            'rebalance_cooldown_hours': 1.8,
        },
        'minimums': {
            'delta_drift_threshold_pct': 2.0,
            'rebalance_cooldown_hours': 24.0,  # Cap at 24h (was 48h)
        },
        'overrides': {
            'down_threshold': -0.35,
            'bounce_threshold': -0.25,
            'lookback_hours': 48,
        }
    }
}

# Safety parameters (correlation-based formulas)
SAFETY_FORMULAS = {
    'max_hedge_drift_pct': lambda corr: max(0.45, min(0.70, 0.55 + 1.2 * (0.75 - corr))),  # Capped [0.45, 0.70]
    'drift_min_pct_of_capital': lambda corr: 0.07 * (corr / 0.75),
}

# ARV-based drift cap (low volatility override)
ARV_DRIFT_CAP = {
    'threshold': 25.0,  # ARV <= 25% = very low volatility
    'max_drift': 0.60,  # Cap drift threshold at 0.60% in calm markets
}

# Volume/TVL-based drift minimum (thin pool protection)
VOLUME_TVL_DRIFT_FLOOR = {
    'threshold': 3.0,   # volume_tvl_ratio < 3.0 = thin pool
    'min_drift': 0.10,  # Floor at 10% of capital
}

# ═══════════════════════════════════════════════════════════════════
# CALCULATION FUNCTION
# ═══════════════════════════════════════════════════════════════════

def calculate(corr_7d: float, arv_7d: float, mrhl_hours: float, funding_rate_daily: float) -> dict:
    """
    Calculate hedge configuration for balanced profile.
    
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
    
    ratio = 0.45  # Default for very low correlation
    for threshold, tier_ratio in CORRELATION_TIERS:
        if corr_7d >= threshold:
            ratio = tier_ratio
            break
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 2: Apply MRHL trending adjustment (ONLY adjustment to hedge ratio)
    # ═══════════════════════════════════════════════════════════════════
    
    if mrhl_hours > MRHL_HEDGE_ADJUSTMENT['threshold']:
        # Trending market - reduce hedge ratio by 12%
        ratio = max(
            MRHL_HEDGE_ADJUSTMENT['min_ratio'],
            ratio * (1 - MRHL_HEDGE_ADJUSTMENT['reduction'])
        )
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 3: Final cap at 1.0 (safety - should never be needed)
    # ═══════════════════════════════════════════════════════════════════
    
    ratio = min(1.00, ratio)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 4: Calculate rebalancing settings (ARV/MRHL/funding driven)
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
    
    # Apply funding multiplier to hedge ratio
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
    
    # Apply ARV adjustments to rebalancing settings
    if arv_7d >= ARV_REBALANCING['high_threshold']:
        # High volatility - widen thresholds, lengthen cooldown
        delta_drift_threshold_pct *= ARV_REBALANCING['high_arv']['drift_multiplier']
        rebalance_cooldown_hours *= ARV_REBALANCING['high_arv']['cooldown_multiplier']
    elif arv_7d <= ARV_REBALANCING['low_threshold']:
        # Low volatility - tighten thresholds, shorten cooldown
        delta_drift_threshold_pct *= ARV_REBALANCING['low_arv']['drift_multiplier']
        rebalance_cooldown_hours *= ARV_REBALANCING['low_arv']['cooldown_multiplier']
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 5: Calculate pullback filter (correlation-based)
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
    # STEP 6.5: Apply ARV-based drift cap (low volatility override)
    # ═══════════════════════════════════════════════════════════════════
    
    if arv_7d <= ARV_DRIFT_CAP['threshold']:
        # Very low volatility - cap drift threshold to prevent over-laziness
        delta_drift_threshold_pct = min(delta_drift_threshold_pct, ARV_DRIFT_CAP['max_drift'])
    
    # Hard cap on drift threshold for low-correlation scenarios
    if corr_7d < 0.55:
        delta_drift_threshold_pct = min(delta_drift_threshold_pct, 1.80)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 6.6: Apply hard cooldown cap (balanced profile safety)
    # ═══════════════════════════════════════════════════════════════════
    
    # Hard cap at 24h to prevent excessive laziness from ARV + MRHL stacking
    # Longer cooldowns belong in conservative profiles
    rebalance_cooldown_hours = min(rebalance_cooldown_hours, 24.0)
    
    # ═══════════════════════════════════════════════════════════════════
    # STEP 7: Calculate safety parameters (correlation-based)
    # ═══════════════════════════════════════════════════════════════════
    
    max_hedge_drift_pct = SAFETY_FORMULAS['max_hedge_drift_pct'](corr_7d)
    drift_min_pct_of_capital = SAFETY_FORMULAS['drift_min_pct_of_capital'](corr_7d)
    
    # ═══════════════════════════════════════════════════════════════════
    # FINAL CONFIG ASSEMBLY
    # ═══════════════════════════════════════════════════════════════════
    
    return {
        # Core hedge behavior - CORRELATION DRIVEN ONLY
        'target_hedge_ratio': round(ratio, 3),
        
        # Rebalancing settings - ARV/MRHL/FUNDING DRIVEN
        'delta_drift_threshold_pct': round(delta_drift_threshold_pct, 3),
        'rebalance_cooldown_hours': round(rebalance_cooldown_hours, 1),
        
        # Pullback filter (dynamic)
        'down_threshold': round(down_threshold, 4),
        'bounce_threshold': round(bounce_threshold, 4),
        'lookback_hours': int(lookback_hours),
        
        # Safety parameters (dynamic)
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
