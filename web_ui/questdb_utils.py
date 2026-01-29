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
                (lp_value_usd + hl_account_value) as total_value
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
            }
        
        return None
        
    except Exception as e:
        print(f"Error fetching latest position values: {e}")
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
