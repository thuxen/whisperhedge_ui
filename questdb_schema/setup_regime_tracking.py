#!/usr/bin/env python3
"""
Create regime_tracking table in QuestDB.

This script creates the regime_tracking table for tracking dynamic config
regime changes and decisions over time.

Usage:
    python schema/setup_regime_tracking.py
"""

import requests
import sys

# QuestDB connection (matches config)
QUESTDB_HOST = '84.247.147.36'
QUESTDB_PORT = 9000

def create_regime_tracking_table():
    """Create the regime_tracking table in QuestDB."""
    
    print("=" * 80)
    print("Creating regime_tracking table in QuestDB")
    print("=" * 80)
    
    schema = """
    CREATE TABLE IF NOT EXISTS regime_tracking (
        time TIMESTAMP,
        position_id SYMBOL INDEX,
        
        -- Regime Classification
        funding_regime SYMBOL,
        rebalance_aggression SYMBOL,
        mrhl_regime SYMBOL,
        
        -- Applied Config Values
        target_hedge_ratio DOUBLE,
        delta_drift_threshold_pct DOUBLE,
        rebalance_cooldown_hours DOUBLE,
        down_threshold DOUBLE,
        bounce_threshold DOUBLE,
        lookback_hours INT,
        
        -- Input Indicators (Core)
        corr_returns_7d DOUBLE,
        std_token_7d DOUBLE,
        std_eth_7d DOUBLE,
        vol_ratio DOUBLE,
        funding_rate_daily DOUBLE,
        mrhl_hours DOUBLE,
        
        -- MVHR Calculation Details
        mvhr_beta_raw DOUBLE,
        mvhr_base_ratio DOUBLE,
        
        -- Regime Change Detection
        regime_changed BOOLEAN,
        config_changed BOOLEAN,
        previous_funding_regime SYMBOL,
        previous_rebalance_aggression SYMBOL,
        previous_mrhl_regime SYMBOL,
        
        -- Metadata
        dynamic_config_enabled BOOLEAN,
        dynamic_config_applied BOOLEAN,
        fallback_reason SYMBOL,
        
        -- Extensible Indicators (JSON)
        indicators_json STRING
        
    ) timestamp(time) PARTITION BY DAY;
    """
    
    try:
        print("\n📍 Sending CREATE TABLE request to QuestDB...")
        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': schema.strip()},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Table created successfully!")
            return True
        else:
            print(f"❌ Table creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

def verify_table():
    """Verify that the table was created successfully."""
    
    print("\n" + "=" * 80)
    print("Verifying regime_tracking table")
    print("=" * 80)
    
    try:
        # Check if table exists
        print("\n📍 Checking if table exists...")
        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': 'SELECT table_name FROM tables();'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'dataset' in result and result['dataset']:
                tables = [row[0] for row in result['dataset']]
                
                if 'regime_tracking' in tables:
                    print("✅ Table exists in database")
                else:
                    print("❌ Table not found in database")
                    return False
            else:
                print("❌ Could not retrieve table list")
                return False
        else:
            print(f"❌ Query failed: {response.status_code}")
            return False
        
        # Check table schema
        print("\n📍 Checking table schema...")
        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': 'SELECT * FROM regime_tracking LIMIT 0;'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'columns' in result:
                columns = [col['name'] for col in result['columns']]
                print(f"✅ Table has {len(columns)} columns:")
                
                # Print key columns
                key_columns = [
                    'time', 'position_id', 'funding_regime', 'rebalance_aggression',
                    'target_hedge_ratio', 'delta_drift_threshold_pct', 'corr_returns_7d',
                    'regime_changed', 'indicators_json'
                ]
                
                for col in key_columns:
                    if col in columns:
                        print(f"   ✓ {col}")
                    else:
                        print(f"   ✗ {col} (MISSING)")
                
                return True
            else:
                print("❌ Could not retrieve column information")
                return False
        else:
            print(f"❌ Schema query failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def print_usage_examples():
    """Print example queries for the new table."""
    
    print("\n" + "=" * 80)
    print("Example Queries")
    print("=" * 80)
    
    examples = [
        ("Find regime changes in last 7 days", """
SELECT time, position_id, funding_regime, previous_funding_regime,
       target_hedge_ratio, delta_drift_threshold_pct
FROM regime_tracking
WHERE regime_changed = true 
  AND time > dateadd('d', -7, now())
ORDER BY time DESC;
        """),
        
        ("Regime change frequency by position", """
SELECT position_id, 
       COUNT(*) as total_changes,
       COUNT(*) FILTER (WHERE funding_regime != previous_funding_regime) as funding_changes
FROM regime_tracking
WHERE time > dateadd('d', -30, now())
  AND regime_changed = true
GROUP BY position_id;
        """),
        
        ("Current regime for all positions", """
SELECT DISTINCT ON (position_id) 
       position_id,
       time,
       funding_regime,
       target_hedge_ratio,
       corr_returns_7d
FROM regime_tracking
ORDER BY position_id, time DESC;
        """),
    ]
    
    for title, query in examples:
        print(f"\n📊 {title}:")
        print(query.strip())

if __name__ == "__main__":
    print("\n🚀 QuestDB Regime Tracking Table Setup\n")
    
    # Create table
    success = create_regime_tracking_table()
    
    if not success:
        print("\n❌ Setup failed - table creation error")
        sys.exit(1)
    
    # Verify table
    verified = verify_table()
    
    if not verified:
        print("\n⚠️  Table created but verification failed")
        sys.exit(1)
    
    # Print usage examples
    print_usage_examples()
    
    print("\n" + "=" * 80)
    print("✅ Setup Complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run core_hedger_v5.py with dynamic config enabled")
    print("2. Regime data will be logged to regime_tracking table")
    print("3. Use example queries above to analyze regime changes")
    print("4. Monitor for regime oscillation patterns")
    print("=" * 80 + "\n")
