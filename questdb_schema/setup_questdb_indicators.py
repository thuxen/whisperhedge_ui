#!/usr/bin/env python3
"""
QuestDB Indicator Tables Setup Script

Creates all indicator tables in QuestDB with proper schema and partitioning.
Run this after setup_questdb_schema.py to create indicator tables.

Indicators:
- ATR (Average True Range): Price volatility measurement
- CORR (Correlation): Price pattern correlation
- ARV (Annualized Realized Volatility): Volatility measurement
- MRHL (Mean Reversion Half-Life): Mean reversion speed
"""

import requests

# Use the same host from config
QUESTDB_HOST = '84.247.147.36'
QUESTDB_PORT = 9000

def execute_query(query: str) -> bool:
    """Execute a SQL query on QuestDB via REST API."""
    try:
        response = requests.get(
            f"http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec",
            params={'query': query}
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                print(f"❌ Query error: {result['error']}")
                return False
            return True
        else:
            print(f"❌ HTTP error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def drop_indicator_tables():
    """Drop existing indicator tables (if schema needs to change)."""
    print("🗑️  Dropping existing indicator tables...")
    
    tables = ['indicator_atr', 'indicator_corr', 'indicator_arv', 'indicator_mrhl']
    for table in tables:
        query = f"DROP TABLE IF EXISTS {table};"
        if execute_query(query):
            print(f"   ✅ Dropped {table}")
        else:
            print(f"   ⚠️  Could not drop {table} (may not exist)")
    print()


def create_indicator_tables():
    """Create all indicator tables in QuestDB."""
    
    print("=" * 80)
    print("QuestDB Indicator Tables Setup")
    print("=" * 80)
    print(f"Host: {QUESTDB_HOST}")
    print(f"REST Port: {QUESTDB_PORT}")
    print()
    
    # Drop existing tables first (schema changed)
    drop_indicator_tables()
    
    # =============================================================================
    # ATR INDICATOR (Average True Range)
    # =============================================================================
    print("📊 Dropping and recreating indicator_atr table...")
    
    # Drop existing table
    drop_atr = "DROP TABLE IF EXISTS indicator_atr;"
    execute_query(drop_atr)
    
    # Recreate with DEDUP
    atr_query = """
    CREATE TABLE indicator_atr (
        time TIMESTAMP,
        pool_address SYMBOL INDEX,
        period INT,
        atr_value DOUBLE,
        atr_pct DOUBLE,
        current_price DOUBLE,
        data_points INT
    ) TIMESTAMP(time) PARTITION BY DAY
    DEDUP UPSERT KEYS(time, pool_address, period);
    """
    
    if execute_query(atr_query):
        print("   ✅ indicator_atr table created with DEDUP")
    else:
        print("   ❌ Failed to create indicator_atr table")
        return False
    
    # =============================================================================
    # CORR INDICATOR (Correlation)
    # =============================================================================
    print("📊 Dropping and recreating indicator_corr table...")
    
    # Drop existing table
    drop_corr = "DROP TABLE IF EXISTS indicator_corr;"
    execute_query(drop_corr)
    
    # Recreate with DEDUP (now includes 'type' for log_return vs price_level)
    corr_query = """
    CREATE TABLE indicator_corr (
        time TIMESTAMP,
        pool_address SYMBOL INDEX,
        period INT,
        type SYMBOL INDEX,
        corr_value DOUBLE,
        corr_period_days INT,
        current_price DOUBLE,
        data_points INT
    ) TIMESTAMP(time) PARTITION BY DAY
    DEDUP UPSERT KEYS(time, pool_address, period, type);
    """
    
    if execute_query(corr_query):
        print("   ✅ indicator_corr table created with DEDUP")
    else:
        print("   ❌ Failed to create indicator_corr table")
        return False
    
    # =============================================================================
    # ARV INDICATOR (Annualized Realized Volatility)
    # =============================================================================
    print("📊 Dropping and recreating indicator_arv table...")
    
    # Drop existing table
    drop_arv = "DROP TABLE IF EXISTS indicator_arv;"
    execute_query(drop_arv)
    
    # Recreate with DEDUP
    arv_query = """
    CREATE TABLE indicator_arv (
        time TIMESTAMP,
        pool_address SYMBOL INDEX,
        period INT,
        arv_value DOUBLE,
        arv_pct DOUBLE,
        current_price DOUBLE,
        data_points INT
    ) TIMESTAMP(time) PARTITION BY DAY
    DEDUP UPSERT KEYS(time, pool_address, period);
    """
    
    if execute_query(arv_query):
        print("   ✅ indicator_arv table created with DEDUP")
    else:
        print("   ❌ Failed to create indicator_arv table")
        return False
    
    # =============================================================================
    # MRHL INDICATOR (Mean Reversion Half-Life)
    # =============================================================================
    print("📊 Dropping and recreating indicator_mrhl table...")
    
    # Drop existing table
    drop_mrhl = "DROP TABLE IF EXISTS indicator_mrhl;"
    execute_query(drop_mrhl)
    
    # Recreate with DEDUP
    mrhl_query = """
    CREATE TABLE indicator_mrhl (
        time TIMESTAMP,
        pool_address SYMBOL INDEX,
        period INT,
        half_life_hours DOUBLE,
        kappa DOUBLE,
        r_squared DOUBLE,
        current_price DOUBLE,
        data_points INT
    ) TIMESTAMP(time) PARTITION BY DAY
    DEDUP UPSERT KEYS(time, pool_address, period);
    """
    
    if execute_query(mrhl_query):
        print("   ✅ indicator_mrhl table created with DEDUP")
    else:
        print("   ❌ Failed to create indicator_mrhl table")
        return False
    
    return True


def verify_tables():
    """Verify all indicator tables exist."""
    print("\n📋 Verifying indicator tables...")
    
    query = "SHOW TABLES;"
    response = requests.get(
        f"http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec",
        params={'query': query}
    )
    
    if response.status_code == 200:
        result = response.json()
        if 'dataset' in result:
            tables = [row[0] for row in result['dataset']]
            
            expected_tables = [
                'indicator_atr',
                'indicator_corr',
                'indicator_arv',
                'indicator_mrhl'
            ]
            
            found_tables = [t for t in expected_tables if t in tables]
            
            print(f"\n✅ Found {len(found_tables)}/{len(expected_tables)} indicator tables:")
            for table in found_tables:
                print(f"   - {table}")
            
            if len(found_tables) == len(expected_tables):
                print("\n🎉 All indicator tables created successfully!")
                return True
            else:
                missing = set(expected_tables) - set(found_tables)
                print(f"\n⚠️  Missing tables: {missing}")
                return False
    
    print("❌ Failed to verify tables")
    return False


def main():
    """Main setup function."""
    try:
        if create_indicator_tables():
            if verify_tables():
                print("\n" + "=" * 80)
                print("✅ QuestDB indicator tables setup complete!")
                print("=" * 80)
                return
        
        print("\n" + "=" * 80)
        print("❌ QuestDB indicator tables setup failed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Setup failed with exception: {e}")


if __name__ == "__main__":
    main()
