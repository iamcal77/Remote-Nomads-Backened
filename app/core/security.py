# app/core/security.py

from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
import hashlib
import hmac

# ------------------ Password Hashing (Argon2) ------------------
# Install: pip install passlib[argon2] argon2-cffi
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a user password using Argon2 (no 72-byte limit)."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a user password against the Argon2 hash."""
    return pwd_context.verify(password, hashed)

# ------------------ JWT Handling ------------------
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes: int = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = data.copy()
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# ------------------ Secret / Token Hashing ------------------
def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()

def verify_secret(secret: str, hash_value: str) -> bool:
    return hmac.compare_digest(hash_secret(secret), hash_value)

def create_password_reset_token(user_id: int, expires_minutes: int = 15) -> str:
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload = {
        "user_id": user_id,
        "type": "password_reset",
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
