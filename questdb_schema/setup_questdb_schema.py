#!/usr/bin/env python3
"""
Create QuestDB tables for the data collector.
"""

import requests
import time

# Use the same host from config
QUESTDB_HOST = '100.82.114.51'
QUESTDB_PORT = 9000

def create_tables():
    """Create the required tables in QuestDB."""

    print("🔍 Creating QuestDB tables...")

    # QuestDB table schemas
    schemas = [
        # Pool metadata table
        # Drop existing table first
        """
        DROP TABLE IF EXISTS data_pools;
        """,
        
        # Recreate pool metadata table
        """
        CREATE TABLE data_pools (
            pool_address SYMBOL,
            network SYMBOL,
            strategy SYMBOL,
            tags SYMBOL,
            notes SYMBOL,
            enabled BOOLEAN,
            date_added TIMESTAMP,
            gt_name SYMBOL,
            gt_created_at TIMESTAMP,
            gt_reserve_usd DOUBLE,
            gt_fdv_usd DOUBLE,
            gt_volume_24h DOUBLE,
            gt_price_change_24h DOUBLE,
            gt_transactions_24h LONG,
            token0_address SYMBOL,
            token0_symbol SYMBOL,
            token0_decimals INT,
            token1_address SYMBOL,
            token1_symbol SYMBOL,
            token1_decimals INT,
            fee_tier INT,
            liquidity STRING,
            current_tick INT,
            sqrt_price_x96 STRING,
            raw_geckoterminal_data STRING,
            raw_web3_data STRING
        ) timestamp(date_added) PARTITION BY MONTH;
        """,

        # Price data table (time-series)
        # Drop existing table first
        """
        DROP TABLE IF EXISTS data_prices;
        """,
        
        # Recreate with DEDUP and is_synthetic flag
        """
        CREATE TABLE data_prices (
            time TIMESTAMP,
            pool_address SYMBOL INDEX,
            open_usd DOUBLE,
            high_usd DOUBLE,
            low_usd DOUBLE,
            close_usd DOUBLE,
            volume_usd DOUBLE,
            open_ratio DOUBLE,
            high_ratio DOUBLE,
            low_ratio DOUBLE,
            close_ratio DOUBLE,
            volume_ratio DOUBLE,
            is_synthetic BOOLEAN
        ) timestamp(time) PARTITION BY DAY
        DEDUP UPSERT KEYS(time, pool_address);
        """,
        
        # Pool metrics table (time-series, less frequent than prices)
        # Drop existing table first
        """
        DROP TABLE IF EXISTS data_pool_metrics;
        """,
        
        # Recreate pool metrics table
        """
        CREATE TABLE data_pool_metrics (
            time TIMESTAMP,
            pool_address SYMBOL,
            tvl_usd DOUBLE,
            volume_24h_usd DOUBLE,
            volume_tvl_ratio DOUBLE,
            price_change_24h_pct DOUBLE,
            transactions_24h INT,
            buys_24h INT,
            sells_24h INT,
            fdv_usd DOUBLE
        ) timestamp(time) PARTITION BY DAY;
        """
    ]

    success_count = 0

    for i, schema in enumerate(schemas, 1):
        print(f"Creating table {i}/{len(schemas)}...")

        try:
            # Use GET with query parameter for QuestDB
            response = requests.get(
                f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
                params={'query': schema.strip()},
                timeout=30
            )

            if response.status_code == 200:
                print(f"  ✅ Table {i} created successfully")
                success_count += 1
            else:
                print(f"  ❌ Table {i} creation failed: {response.status_code}")
                print(f"     Response: {response.text}")

        except Exception as e:
            print(f"  ❌ Table {i} creation error: {e}")

        # Small delay between table creations
        time.sleep(1)

    return success_count == len(schemas)

def verify_tables():
    """Verify that tables were created successfully."""

    print("\n🔍 Verifying tables...")

    try:
        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': 'SELECT table_name FROM tables();'},
            timeout=10
        )

        if response.status_code == 200:
            import json
            result = response.json()

            if 'dataset' in result and result['dataset']:
                tables = [row[0] for row in result['dataset']]
                print(f"Found tables: {tables}")

                required_tables = ['data_pools', 'data_prices']
                missing_tables = [t for t in required_tables if t not in tables]

                if not missing_tables:
                    print("✅ All required tables present!")
                    return True
                else:
                    print(f"❌ Missing tables: {missing_tables}")
                    return False
            else:
                print("❌ No tables found")
                return False
        else:
            print(f"❌ Query failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def test_basic_operations():
    """Test basic insert and select operations."""

    print("\n🔍 Testing basic operations...")

    try:
        # Test insert via REST API
        insert_query = """
        INSERT INTO data_prices (time, pool_address, close_usd)
        VALUES (now(), '0x1234567890123456789012345678901234567890', 100.0);
        """

        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': insert_query.strip()},
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Insert operation successful")
        else:
            print(f"❌ Insert failed: {response.status_code} - {response.text}")
            return False

        # Test select
        select_query = "SELECT * FROM data_prices LIMIT 5;"

        response = requests.get(
            f'http://{QUESTDB_HOST}:{QUESTDB_PORT}/exec',
            params={'query': select_query},
            timeout=10
        )

        if response.status_code == 200:
            print("✅ Select operation successful")
            return True
        else:
            print(f"❌ Select failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ Operation test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("QuestDB Schema Setup")
    print("=" * 60)

    # Create tables
    tables_created = create_tables()

    if tables_created:
        # Verify tables
        tables_verified = verify_tables()

        if tables_verified:
            # Test operations
            operations_ok = test_basic_operations()

            if operations_ok:
                print("\n🎉 QuestDB is ready for data collection!")
            else:
                print("\n⚠️ Tables created but operations failed")
        else:
            print("\n❌ Table verification failed")
    else:
        print("\n❌ Table creation failed")

    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. If successful: Run data_collector_v2.py")
    print("2. If failed: Check QuestDB logs and network configuration")
    print("=" * 60)
