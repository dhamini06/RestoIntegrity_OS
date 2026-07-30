import os
import hashlib
import secrets
import bcrypt
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def generate_otp(length: int = 6) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(length))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode("utf-8")).hexdigest()

def verify_otp(otp: str, otp_hash: str) -> bool:
    return hash_otp(otp) == otp_hash

def generate_session_token() -> str:
    return secrets.token_urlsafe(48)

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

def get_otp_expiry(minutes: int = 5) -> str:
    return (datetime.now() + timedelta(minutes=minutes)).isoformat()

def is_expired(expiry_iso: str) -> bool:
    return datetime.now() > datetime.fromisoformat(expiry_iso)

def sanitize_email(email: str) -> str:
    return email.strip().lower()
