"""
Position metrics calculation and formatting
"""
from pydantic import BaseModel
from typing import Optional


class PositionMetrics(BaseModel):
    """Calculated metrics for a position"""
    
    # Value metrics (raw values)
    lp_value: float = 0.0
    hedge_value: float = 0.0
    total_value: float = 0.0
    
    # Entry baseline values (for PnL calculation)
    entry_lp_value: Optional[float] = None
    entry_hedge_value: Optional[float] = None
    entry_total_value: Optional[float] = None
    
    # Performance metrics - Total Position
    entry_value: Optional[float] = None
    current_pnl: Optional[float] = None
    pnl_percentage: Optional[float] = None
    apr: Optional[float] = None
    
    # Performance metrics - LP Component
    lp_pnl_usd: Optional[float] = None
    lp_pnl_pct: Optional[float] = None
    
    # Performance metrics - Hedge Component
    hedge_pnl_usd: Optional[float] = None
    hedge_pnl_pct: Optional[float] = None
    
    # Impermanent Loss metrics
    il_usd: Optional[float] = None
    il_pct: Optional[float] = None
    
    # Range position metrics
    utilization_pct: Optional[float] = None
    distance_to_lower_pct: Optional[float] = None
    distance_to_upper_pct: Optional[float] = None
    
    # Price metrics (placeholders for future)
    entry_price: Optional[float] = None
    current_price: Optional[float] = None
    price_change_pct: Optional[float] = None
    
    # Time metrics
    last_update: str = "Never"
    position_age_days: Optional[int] = None
