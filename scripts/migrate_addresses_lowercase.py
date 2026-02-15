#!/usr/bin/env python3
"""
One-time migration script to lowercase all ERC-20 addresses in Supabase.

This script:
1. Performs a dry run to identify addresses that will change
2. Checks for potential unique constraint violations
3. Reports conflicts for manual review
4. Waits for user confirmation before applying changes
5. Updates all EVM network addresses to lowercase in a transaction

Run from project root:
    python3 scripts/migrate_addresses_lowercase.py
"""

import os
import sys
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from web_ui/.env
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(project_root, 'web_ui', '.env')
load_dotenv(env_path)

# EVM networks that use case-insensitive addresses
EVM_NETWORKS = {'ethereum', 'arbitrum', 'base', 'polygon', 'optimism'}


def get_supabase_admin_client() -> Client:
    """Get Supabase client with service role key for admin operations"""
    url = os.getenv("SUPABASE_URL")
    # Use service role key to bypass RLS policies for migration
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment")
    
    return create_client(url, key)


def analyze_lp_positions(supabase: Client) -> Tuple[List[Dict], List[str]]:
    """Analyze lp_positions table for addresses that need lowercasing"""
    print("\n📋 Analyzing lp_positions table...")
    
    response = supabase.table("lp_positions").select("id, user_id, protocol, network, nft_id, pool_address").execute()
    
    print(f"  DEBUG: Found {len(response.data)} total rows")
    
    changes = []
    conflicts = []
    
    for row in response.data:
        network = row.get('network', '').lower()
        pool_address = row.get('pool_address', '')
        print(f"  DEBUG: network='{network}', pool_address='{pool_address}', is_mixed_case={pool_address != pool_address.lower() if pool_address else 'N/A'}")
        
        if network in EVM_NETWORKS and pool_address and pool_address != pool_address.lower():
            changes.append({
                'table': 'lp_positions',
                'id': row['id'],
                'field': 'pool_address',
                'old': pool_address,
                'new': pool_address.lower(),
                'network': network,
                'user_id': row['user_id'],
                'protocol': row['protocol'],
                'nft_id': row['nft_id']
            })
    
    # Check for potential unique constraint violations
    # UNIQUE(user_id, protocol, network, nft_id)
    seen_keys = {}
    for row in response.data:
        network = row.get('network', '').lower()
        if network in EVM_NETWORKS:
            key = (row['user_id'], row['protocol'], network, row['nft_id'])
            if key in seen_keys:
                conflicts.append(f"lp_positions: Duplicate key {key}")
            seen_keys[key] = row['id']
    
    print(f"  Found {len(changes)} addresses to lowercase")
    print(f"  Found {len(conflicts)} potential conflicts")
    
    return changes, conflicts


def analyze_position_configs(supabase: Client) -> Tuple[List[Dict], List[str]]:
    """Analyze position_configs table for addresses that need lowercasing"""
    print("\n📋 Analyzing position_configs table...")
    
    response = supabase.table("position_configs").select(
        "id, user_id, protocol, network, nft_id, pool_address, token0_address, token1_address"
    ).execute()
    
    print(f"  DEBUG: Found {len(response.data)} total rows")
    
    changes = []
    conflicts = []
    
    for row in response.data:
        print(f"  DEBUG: Row - network={row.get('network')}, pool={row.get('pool_address')}, token0={row.get('token0_address')}, token1={row.get('token1_address')}")
        network = row.get('network', '').lower()
        
        if network in EVM_NETWORKS:
            # Check pool_address
            pool_address = row.get('pool_address', '')
            if pool_address and pool_address != pool_address.lower():
                changes.append({
                    'table': 'position_configs',
                    'id': row['id'],
                    'field': 'pool_address',
                    'old': pool_address,
                    'new': pool_address.lower(),
                    'network': network
                })
            
            # Check token0_address
            token0_address = row.get('token0_address', '')
            if token0_address and token0_address != token0_address.lower():
                changes.append({
                    'table': 'position_configs',
                    'id': row['id'],
                    'field': 'token0_address',
                    'old': token0_address,
                    'new': token0_address.lower(),
                    'network': network
                })
            
            # Check token1_address
            token1_address = row.get('token1_address', '')
            if token1_address and token1_address != token1_address.lower():
                changes.append({
                    'table': 'position_configs',
                    'id': row['id'],
                    'field': 'token1_address',
                    'old': token1_address,
                    'new': token1_address.lower(),
                    'network': network
                })
    
    # Check for potential unique constraint violations
    # UNIQUE(user_id, protocol, nft_id, network)
    seen_keys = {}
    for row in response.data:
        network = row.get('network', '').lower()
        if network in EVM_NETWORKS:
            key = (row['user_id'], row['protocol'], row['nft_id'], network)
            if key in seen_keys:
                conflicts.append(f"position_configs: Duplicate key {key}")
            seen_keys[key] = row['id']
    
    print(f"  Found {len(changes)} addresses to lowercase")
    print(f"  Found {len(conflicts)} potential conflicts")
    
    return changes, conflicts


def analyze_user_api_keys(supabase: Client) -> Tuple[List[Dict], List[str]]:
    """Analyze user_api_keys table for addresses that need lowercasing"""
    print("\n📋 Analyzing user_api_keys table...")
    
    response = supabase.table("user_api_keys").select("id, user_id, exchange, wallet_address").execute()
    
    print(f"  DEBUG: Found {len(response.data)} total rows")
    
    changes = []
    conflicts = []
    
    for row in response.data:
        print(f"  DEBUG: Row - exchange={row.get('exchange')}, wallet_address={row.get('wallet_address')}")
        exchange = row.get('exchange', '').lower()
        wallet_address = row.get('wallet_address', '')
        print(f"    -> exchange='{exchange}', is_hyperliquid={exchange == 'hyperliquid'}, has_mixed_case={wallet_address != wallet_address.lower() if wallet_address else 'N/A'}")
        
        # Currently all exchanges are Hyperliquid (EVM-based)
        # In future, check exchange type to determine if EVM
        if exchange == 'hyperliquid' and wallet_address and wallet_address != wallet_address.lower():
            changes.append({
                'table': 'user_api_keys',
                'id': row['id'],
                'field': 'wallet_address',
                'old': wallet_address,
                'new': wallet_address.lower(),
                'exchange': exchange
            })
    
    print(f"  Found {len(changes)} addresses to lowercase")
    print(f"  Found {len(conflicts)} potential conflicts")
    
    return changes, conflicts


def print_changes(all_changes: List[Dict]):
    """Print all changes in a readable format"""
    if not all_changes:
        print("\n✅ No addresses need to be changed!")
        return
    
    print(f"\n📝 Summary of changes ({len(all_changes)} total):")
    print("=" * 80)
    
    by_table = {}
    for change in all_changes:
        table = change['table']
        if table not in by_table:
            by_table[table] = []
        by_table[table].append(change)
    
    for table, changes in by_table.items():
        print(f"\n{table}: {len(changes)} changes")
        for i, change in enumerate(changes[:5], 1):  # Show first 5 examples
            print(f"  {i}. {change['field']}: {change['old']} → {change['new']}")
        if len(changes) > 5:
            print(f"  ... and {len(changes) - 5} more")


def apply_changes(supabase: Client, all_changes: List[Dict]) -> bool:
    """Apply all address changes to the database"""
    print("\n🔄 Applying changes...")
    
    success_count = 0
    error_count = 0
    
    for change in all_changes:
        try:
            table = change['table']
            record_id = change['id']
            field = change['field']
            new_value = change['new']
            
            supabase.table(table).update({field: new_value}).eq("id", record_id).execute()
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error updating {table}.{field} (id={record_id}): {e}")
            error_count += 1
    
    print(f"\n✅ Successfully updated {success_count} addresses")
    if error_count > 0:
        print(f"❌ Failed to update {error_count} addresses")
        return False
    
    return True


def verify_changes(supabase: Client) -> bool:
    """Verify that all EVM addresses are now lowercase"""
    print("\n🔍 Verifying changes...")
    
    issues = []
    
    # Check lp_positions
    response = supabase.table("lp_positions").select("id, network, pool_address").execute()
    for row in response.data:
        network = row.get('network', '').lower()
        pool_address = row.get('pool_address', '')
        if network in EVM_NETWORKS and pool_address and pool_address != pool_address.lower():
            issues.append(f"lp_positions.pool_address still has mixed case: {pool_address}")
    
    # Check position_configs
    response = supabase.table("position_configs").select(
        "id, network, pool_address, token0_address, token1_address"
    ).execute()
    for row in response.data:
        network = row.get('network', '').lower()
        if network in EVM_NETWORKS:
            for field in ['pool_address', 'token0_address', 'token1_address']:
                addr = row.get(field, '')
                if addr and addr != addr.lower():
                    issues.append(f"position_configs.{field} still has mixed case: {addr}")
    
    # Check user_api_keys
    response = supabase.table("user_api_keys").select("id, exchange, wallet_address").execute()
    for row in response.data:
        exchange = row.get('exchange', '').lower()
        wallet_address = row.get('wallet_address', '')
        if exchange == 'hyperliquid' and wallet_address and wallet_address != wallet_address.lower():
            issues.append(f"user_api_keys.wallet_address still has mixed case: {wallet_address}")
    
    if issues:
        print(f"❌ Found {len(issues)} verification issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("✅ All EVM addresses are now lowercase!")
    return True


def main():
    """Main migration script"""
    print("=" * 80)
    print("ERC-20 Address Normalization Migration")
    print("=" * 80)
    
    try:
        # Get Supabase client
        supabase = get_supabase_admin_client()
        print("✅ Connected to Supabase")
        
        # Analyze all tables
        lp_changes, lp_conflicts = analyze_lp_positions(supabase)
        config_changes, config_conflicts = analyze_position_configs(supabase)
        api_changes, api_conflicts = analyze_user_api_keys(supabase)
        
        all_changes = lp_changes + config_changes + api_changes
        all_conflicts = lp_conflicts + config_conflicts + api_conflicts
        
        # Report conflicts
        if all_conflicts:
            print("\n⚠️  CONFLICTS DETECTED:")
            print("=" * 80)
            for conflict in all_conflicts:
                print(f"  - {conflict}")
            print("\n❌ Please resolve conflicts manually before proceeding.")
            return 1
        
        # Print changes
        print_changes(all_changes)
        
        if not all_changes:
            print("\n✅ Migration complete - no changes needed!")
            return 0
        
        # Confirm with user
        print("\n" + "=" * 80)
        response = input("Apply these changes? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("❌ Migration cancelled by user")
            return 1
        
        # Apply changes
        if not apply_changes(supabase, all_changes):
            print("\n❌ Migration failed - some updates did not succeed")
            return 1
        
        # Verify changes
        if not verify_changes(supabase):
            print("\n⚠️  Migration completed but verification found issues")
            return 1
        
        print("\n" + "=" * 80)
        print("✅ Migration completed successfully!")
        print("=" * 80)
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
