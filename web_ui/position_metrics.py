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
    
    # Performance metrics (placeholders for future)
    entry_value: Optional[float] = None
    current_pnl: Optional[float] = None
    pnl_percentage: Optional[float] = None
    
    # Price metrics (placeholders for future)
    entry_price: Optional[float] = None
    current_price: Optional[float] = None
    price_change_pct: Optional[float] = None
    
    # Time metrics
    last_update: str = "Never"
    position_age_days: Optional[int] = None
