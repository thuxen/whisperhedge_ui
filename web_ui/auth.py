import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase_client(access_token: str = "") -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env file")
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Set the session token for RLS to work
    if access_token:
        client.auth.set_session(access_token, "")
    
    return client
