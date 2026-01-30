#!/usr/bin/env python3
"""
Test script to verify domain-based branding
"""
import os
import sys

def test_branding():
    print("=" * 60)
    print("DOMAIN-BASED BRANDING TEST")
    print("=" * 60)
    
    # Test 1: No REFLEX_DOMAIN set (default - whitelabel)
    print("\n1. Testing with NO REFLEX_DOMAIN set (localhost/default):")
    print("-" * 60)
    os.environ.pop('REFLEX_DOMAIN', None)
    os.environ.pop('HOST', None)
    os.environ.pop('VERCEL_URL', None)
    
    # Import after clearing env
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'web_ui'))
    from branding.config import BrandConfig
    print(f"APP_NAME: {BrandConfig.APP_NAME}")
    print(f"COMPANY_NAME: {BrandConfig.COMPANY_NAME}")
    print(f"TAGLINE: {BrandConfig.TAGLINE}")
    print(f"SUPPORT_EMAIL: {BrandConfig.SUPPORT_EMAIL}")
    
    # Test 2: REFLEX_DOMAIN set to whisperhedge.com
    print("\n2. Testing with REFLEX_DOMAIN=whisperhedge.com:")
    print("-" * 60)
    os.environ['REFLEX_DOMAIN'] = 'whisperhedge.com'
    
    # Reload the module
    if 'branding.config' in sys.modules:
        del sys.modules['branding.config']
    
    from branding.config import BrandConfig
    print(f"APP_NAME: {BrandConfig.APP_NAME}")
    print(f"COMPANY_NAME: {BrandConfig.COMPANY_NAME}")
    print(f"TAGLINE: {BrandConfig.TAGLINE}")
    print(f"SUPPORT_EMAIL: {BrandConfig.SUPPORT_EMAIL}")
    
    # Test 3: REFLEX_DOMAIN set to custom domain
    print("\n3. Testing with REFLEX_DOMAIN=metrix.finance:")
    print("-" * 60)
    os.environ['REFLEX_DOMAIN'] = 'metrix.finance'
    
    # Reload the module
    if 'branding.config' in sys.modules:
        del sys.modules['branding.config']
    
    from branding.config import BrandConfig
    print(f"APP_NAME: {BrandConfig.APP_NAME}")
    print(f"COMPANY_NAME: {BrandConfig.COMPANY_NAME}")
    print(f"TAGLINE: {BrandConfig.TAGLINE}")
    print(f"SUPPORT_EMAIL: {BrandConfig.SUPPORT_EMAIL}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nSummary:")
    print("- Local (no REFLEX_DOMAIN): Shows 'White Label'")
    print("- VPS (REFLEX_DOMAIN=whisperhedge.com): Shows 'WhisperHedge'")
    print("- Partners (other domains): Shows 'White Label'")

if __name__ == "__main__":
    test_branding()
