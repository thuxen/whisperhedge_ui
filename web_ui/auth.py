import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase_client(access_token: str = "") -> Client:
    print(f"[SUPABASE] Creating Supabase client", flush=True)
    sys.stdout.flush()
    print(f"[SUPABASE]   - URL configured: {bool(SUPABASE_URL)}", flush=True)
    sys.stdout.flush()
    print(f"[SUPABASE]   - Key configured: {bool(SUPABASE_KEY)}", flush=True)
    sys.stdout.flush()
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("[SUPABASE ERROR] Missing credentials!", flush=True)
        sys.stdout.flush()
        raise ValueError("Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[SUPABASE] ✓ Client created successfully", flush=True)
        sys.stdout.flush()
        
        # Set the session token for RLS to work
        if access_token:
            print("[SUPABASE] Setting session token for RLS", flush=True)
            sys.stdout.flush()
            client.auth.set_session(access_token, "")
        
        return client
    except Exception as e:
        print(f"[SUPABASE ERROR] Failed to create client: {e}", flush=True)
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        raise
