import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")

def get_encryption_key() -> bytes:
    if not ENCRYPTION_KEY:
        raise ValueError("ENCRYPTION_KEY not set in .env file. Generate one with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'")
    return ENCRYPTION_KEY.encode()

def encrypt_value(value: str) -> str:
    f = Fernet(get_encryption_key())
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value: str) -> str:
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_value.encode()).decode()
