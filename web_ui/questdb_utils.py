"""
QuestDB utility functions for querying hedge state and position data
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import List, Dict, Optional


def get_questdb_connection():
    """Create and return a QuestDB connection"""
    questdb_host = os.getenv('QUESTDB_HOST', 'localhost')
    questdb_port = os.getenv('QUESTDB_PORT', '8812')
    questdb_user = os.getenv('QUESTDB_USER', 'admin')
    questdb_password = os.getenv('QUESTDB_PASSWORD', 'quest')
    questdb_database = os.getenv('QUESTDB_DATABASE', 'qdb')
    
    conn = psycopg2.connect(
        host=questdb_host,
        port=int(questdb_port),
        user=questdb_user,
        password=questdb_password,
        database=questdb_database,
        connect_timeout=5
    )
    return conn


def get_position_value_history(position_id: str, hours: int = 24) -> List[Dict]:
    """
    Get historical LP value and hedge account value for a position
    
    Args:
        position_id: The position ID to query
        hours: Number of hours of history to fetch (default 24)
    
    Returns:
        List of dicts with timestamp, lp_value_usd, hl_account_value, total_value
    """
    try:
        print(f"\n=== QuestDB Query Debug ===")
        print(f"Position ID: {position_id}")
        print(f"Hours: {hours}")
        
        conn = get_questdb_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Calculate timestamp for X hours ago
        time_ago = datetime.utcnow() - timedelta(hours=hours)
        print(f"Querying data from: {time_ago} to now")
        
        # Query hedge_state table for position history
        query = """
            SELECT 
                time as timestamp,
                lp_value_usd,
                hl_account_value,
                (lp_value_usd + hl_account_value) as total_value
            FROM hedge_state
            WHERE position_id = %s
            AND time >= %s
            ORDER BY time ASC
        """
        
        print(f"Executing query with position_id='{position_id}'")
        cursor.execute(query, (position_id, time_ago))
        results = cursor.fetchall()
        
        print(f"Query returned {len(results)} rows")
        
        cursor.close()
        conn.close()
        
        # Convert to list of dicts with formatted data
        history = []
        for i, row in enumerate(results):
            # Format timestamp as dd-mm HH:MM for chart display
            if row['timestamp']:
                dt = row['timestamp']
                timestamp_display = f"{dt.day:02d}-{dt.month:02d} {dt.hour:02d}:{dt.minute:02d}"
            else:
                timestamp_display = ""
            
            history.append({
                'timestamp': timestamp_display,
                'lp_value_usd': round(float(row['lp_value_usd']), 2) if row['lp_value_usd'] else 0.0,
                'hl_account_value': round(float(row['hl_account_value']), 2) if row['hl_account_value'] else 0.0,
                'total_value': round(float(row['total_value']), 2) if row['total_value'] else 0.0,
            })
            if i < 3:  # Print first 3 rows for debugging
                print(f"Row {i+1}: {history[-1]}")
        
        print(f"Returning {len(history)} data points")
        print("=========================\n")
        
        return history
        
    except Exception as e:
        print(f"❌ Error fetching position value history: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_latest_position_values(position_id: str) -> Optional[Dict]:
    """
    Get the most recent LP value and hedge account value for a position
    
    Args:
        position_id: The position ID to query
    
    Returns:
        Dict with lp_value_usd, hl_account_value, total_value, timestamp
    """
    try:
        conn = get_questdb_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT 
                time as timestamp,
                lp_value_usd,
                hl_account_value,
                (lp_value_usd + hl_account_value) as total_value,
                lp_il_usd,
                lp_il_pct,
                lp_utilization_pct,
                lp_distance_to_lower_pct,
                lp_distance_to_upper_pct
            FROM hedge_state
            WHERE position_id = %s
            ORDER BY time DESC
            LIMIT 1
        """
        
        cursor.execute(query, (position_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {
                'timestamp': result['timestamp'].isoformat() if result['timestamp'] else None,
                'lp_value_usd': float(result['lp_value_usd']) if result['lp_value_usd'] else 0.0,
                'hl_account_value': float(result['hl_account_value']) if result['hl_account_value'] else 0.0,
                'total_value': float(result['total_value']) if result['total_value'] else 0.0,
                'lp_il_usd': float(result['lp_il_usd']) if result['lp_il_usd'] is not None else None,
                'lp_il_pct': float(result['lp_il_pct']) if result['lp_il_pct'] is not None else None,
                'lp_utilization_pct': float(result['lp_utilization_pct']) if result['lp_utilization_pct'] is not None else None,
                'lp_distance_to_lower_pct': float(result['lp_distance_to_lower_pct']) if result['lp_distance_to_lower_pct'] is not None else None,
                'lp_distance_to_upper_pct': float(result['lp_distance_to_upper_pct']) if result['lp_distance_to_upper_pct'] is not None else None,
            }
        
        return None
        
    except Exception as e:
        print(f"Error fetching latest position values: {e}")
        return None


def get_first_position_values(position_id: str) -> Optional[dict]:
    """
    Get the first hedge_state entry for a position (baseline for PnL calculation).
    
    Args:
        position_id: The position ID to query
    
    Returns:
        dict with first_lp_value, first_hedge_value, first_total_value, or None if no data
    """
    try:
        conn = get_questdb_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT 
                time as timestamp,
                lp_value_usd,
                hl_account_value,
                (lp_value_usd + hl_account_value) as total_value
            FROM hedge_state
            WHERE position_id = %s
            ORDER BY time ASC
            LIMIT 1
        """
        
        cursor.execute(query, (position_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {
                'timestamp': result['timestamp'].isoformat() if result['timestamp'] else None,
                'lp_value_usd': float(result['lp_value_usd']) if result['lp_value_usd'] else 0.0,
                'hl_account_value': float(result['hl_account_value']) if result['hl_account_value'] else 0.0,
                'total_value': float(result['total_value']) if result['total_value'] else 0.0,
            }
        
        return None
        
    except Exception as e:
        print(f"Error fetching first position values: {e}")
        return None


def get_last_hedge_execution(position_id: str) -> Optional[datetime]:
    """
    Get the timestamp of the last hedge execution for a position.
    Returns the most recent entry from hedge_state table.
    
    Args:
        position_id: The position ID to query
    
    Returns:
        datetime of last hedge execution, or None if no hedge data exists
    """
    try:
        conn = get_questdb_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT time as timestamp
            FROM hedge_state
            WHERE position_id = %s
            ORDER BY time DESC
            LIMIT 1
        """
        
        cursor.execute(query, (position_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result and result['timestamp']:
            return result['timestamp']
        
        return None
        
    except Exception as e:
        print(f"Error fetching last hedge execution: {e}")
        return None


def format_time_ago(dt: Optional[datetime]) -> str:
    """
    Format a datetime as a human-readable 'time ago' string.
    
    Args:
        dt: datetime to format
    
    Returns:
        String like "5 seconds ago", "2 hours ago", "Never"
    """
    if dt is None:
        return "Never"
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        secs = int(seconds)
        return f"{secs} second{'s' if secs != 1 else ''} ago"
    elif seconds < 3600:  # Less than 1 hour
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:  # Less than 1 day
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:  # 1 day or more
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


def get_latest_regime_tracking(position_id: str) -> dict | None:
    """
    Get the most recent regime tracking entry for a position.
    Returns the latest applied config values, regime classification, and indicators.
    
    Args:
        position_id: The position ID to query
    
    Returns:
        Dict with regime tracking data or None if no data found
    """
    query = """
        SELECT 
            time,
            funding_regime,
            profile_name,
            target_hedge_ratio,
            delta_drift_threshold_pct,
            rebalance_cooldown_hours,
            down_threshold,
            bounce_threshold,
            lookback_hours,
            corr_returns_7d,
            std_token0_7d,
            std_token1_7d,
            vol_ratio,
            funding_rate_daily,
            mrhl_hours,
            arv_7d_pct,
            atr_7d_pct,
            pool_tvl_usd,
            pool_volume_24h_usd,
            pool_volume_tvl_ratio,
            hl_open_interest_token0,
            hl_open_interest_token1,
            mvhr_beta_raw,
            mvhr_base_ratio,
            dynamic_config_enabled,
            dynamic_config_applied,
            fallback_reason,
            regime_changed,
            config_changed
        FROM regime_tracking
        WHERE position_id = %s
        ORDER BY time DESC
        LIMIT 1
    """
    
    try:
        conn = get_questdb_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(query, (position_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {
                'timestamp': result['time'].isoformat() if result.get('time') else '',
                'funding_regime': result.get('funding_regime') or '',
                'profile_name': result.get('profile_name') or '',
                'target_hedge_ratio': float(result['target_hedge_ratio']) if result.get('target_hedge_ratio') is not None else 0.0,
                'delta_drift_threshold_pct': float(result['delta_drift_threshold_pct']) if result.get('delta_drift_threshold_pct') is not None else 0.0,
                'rebalance_cooldown_hours': float(result['rebalance_cooldown_hours']) if result.get('rebalance_cooldown_hours') is not None else 0.0,
                'down_threshold': float(result['down_threshold']) if result.get('down_threshold') is not None else 0.0,
                'bounce_threshold': float(result['bounce_threshold']) if result.get('bounce_threshold') is not None else 0.0,
                'lookback_hours': int(result['lookback_hours']) if result.get('lookback_hours') is not None else 0,
                'corr_returns_7d': float(result['corr_returns_7d']) if result.get('corr_returns_7d') is not None else 0.0,
                'std_token0_7d': float(result['std_token0_7d']) if result.get('std_token0_7d') is not None else 0.0,
                'std_token1_7d': float(result['std_token1_7d']) if result.get('std_token1_7d') is not None else 0.0,
                'vol_ratio': float(result['vol_ratio']) if result.get('vol_ratio') is not None else 0.0,
                'funding_rate_daily': float(result['funding_rate_daily']) if result.get('funding_rate_daily') is not None else 0.0,
                'mrhl_hours': float(result['mrhl_hours']) if result.get('mrhl_hours') is not None else 0.0,
                'arv_7d_pct': float(result['arv_7d_pct']) if result.get('arv_7d_pct') is not None else 0.0,
                'atr_7d_pct': float(result['atr_7d_pct']) if result.get('atr_7d_pct') is not None else 0.0,
                'pool_tvl_usd': float(result['pool_tvl_usd']) if result.get('pool_tvl_usd') is not None else 0.0,
                'pool_volume_24h_usd': float(result['pool_volume_24h_usd']) if result.get('pool_volume_24h_usd') is not None else 0.0,
                'pool_volume_tvl_ratio': float(result['pool_volume_tvl_ratio']) if result.get('pool_volume_tvl_ratio') is not None else 0.0,
                'hl_open_interest_token0': float(result['hl_open_interest_token0']) if result.get('hl_open_interest_token0') is not None else 0.0,
                'hl_open_interest_token1': float(result['hl_open_interest_token1']) if result.get('hl_open_interest_token1') is not None else 0.0,
                'mvhr_beta_raw': float(result['mvhr_beta_raw']) if result.get('mvhr_beta_raw') is not None else 0.0,
                'mvhr_base_ratio': float(result['mvhr_base_ratio']) if result.get('mvhr_base_ratio') is not None else 0.0,
                'dynamic_config_enabled': bool(result.get('dynamic_config_enabled', False)),
                'dynamic_config_applied': bool(result.get('dynamic_config_applied', False)),
                'fallback_reason': result.get('fallback_reason') or '',
                'regime_changed': bool(result.get('regime_changed', False)),
                'config_changed': bool(result.get('config_changed', False)),
            }
        return None
    except Exception as e:
        print(f"Error fetching regime tracking data: {e}")
        return None
