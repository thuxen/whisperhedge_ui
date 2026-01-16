import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    """Central configuration for the application"""
    
    # Branding
    APP_NAME = os.getenv("APP_NAME", "WhisperHedge")
    COMPANY_NAME = os.getenv("COMPANY_NAME", "WhisperHedge")
    DOMAIN = os.getenv("DOMAIN", "whisperhedge.com")
    
    # Instance Details
    INSTANCE_ID = os.getenv("INSTANCE_ID", "default")
    
    # Supabase Configuration
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Feature Flags
    ENABLE_SIGNUP = os.getenv("ENABLE_SIGNUP", "True").lower() == "true"
