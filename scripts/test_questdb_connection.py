#!/usr/bin/env python3
"""
Test script to verify QuestDB read-only connection
"""
import os
import sys
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("❌ psycopg2 not installed. Installing...")
    os.system("pip install psycopg2-binary")
    import psycopg2
    from psycopg2.extras import RealDictCursor

def load_env():
    """Load environment variables from web_ui/.env"""
    env_file = os.path.join(os.path.dirname(__file__), '..', 'web_ui', '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print(f"✓ Loaded environment from {env_file}")
    else:
        print(f"⚠ No .env file found at {env_file}")

def test_questdb_connection():
    """Test QuestDB connection with read-only credentials"""
    
    # Load environment variables
    load_env()
    
    # Get QuestDB credentials from environment
    questdb_host = os.getenv('QUESTDB_HOST', 'localhost')
    questdb_port = os.getenv('QUESTDB_PORT', '8812')
    questdb_user = os.getenv('QUESTDB_USER', 'admin')
    questdb_password = os.getenv('QUESTDB_PASSWORD', 'quest')
    questdb_database = os.getenv('QUESTDB_DATABASE', 'qdb')
    
    print("\n" + "="*60)
    print("QuestDB Connection Test")
    print("="*60)
    print(f"Host: {questdb_host}")
    print(f"Port: {questdb_port}")
    print(f"User: {questdb_user}")
    print(f"Database: {questdb_database}")
    print("="*60 + "\n")
    
    try:
        # Attempt connection
        print("🔌 Attempting to connect to QuestDB...")
        conn = psycopg2.connect(
            host=questdb_host,
            port=int(questdb_port),
            user=questdb_user,
            password=questdb_password,
            database=questdb_database,
            connect_timeout=5
        )
        print("✅ Connection successful!\n")
        
        # Test read access
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # List all tables
        print("📋 Listing available tables:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  (No tables found)")
        
        print()
        
        # Try to read from a common table (adjust table name as needed)
        print("🔍 Testing read access on tables:")
        for table in tables:
            table_name = table['table_name']
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
                result = cursor.fetchone()
                print(f"  ✓ {table_name}: {result['count']} rows")
                
                # Show sample data from first table with data
                if result['count'] > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    sample_rows = cursor.fetchall()
                    print(f"\n    Sample data from {table_name}:")
                    for i, row in enumerate(sample_rows, 1):
                        print(f"    Row {i}: {dict(row)}")
                    break
                    
            except Exception as e:
                print(f"  ✗ {table_name}: {str(e)}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ QuestDB connection test PASSED")
        print("="*60)
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check that QuestDB is running")
        print("2. Verify credentials in .env.production are correct")
        print("3. Ensure read-only user has proper permissions")
        print("4. Check firewall/network settings")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_questdb_connection()
    sys.exit(0 if success else 1)
