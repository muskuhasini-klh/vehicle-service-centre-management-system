import hashlib
import os

SECRET_KEY = os.getenv("SECRET_KEY", "vehicle-service-centre-secret-key-2026")

def hash_password(password: str) -> str:
    """Generate SHA256 hash of password with salt."""
    return hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password matches either plain text (for initial seed/simple demo) or hash."""
    if plain_password == hashed_password:
        return True
    return hash_password(plain_password) == hashed_password

def generate_token(user_id: int, role: str) -> str:
    """Generate simple demo JWT/session token."""
    raw = f"{user_id}:{role}:{SECRET_KEY}"
    return hashlib.md5(raw.encode()).hexdigest()
