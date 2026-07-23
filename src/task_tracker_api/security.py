from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from task_tracker_api.config import settings 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str: 
    """Menghasilkan hash bcrypt dari plain text password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    """Memverifikasi plain text password terhadap hash yang tersimpan di database."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Membuat JWT access token dengan payload data dan menyertakan waktu kadaluarsa (exp)."""
    # Menggunakan copy agar fungsi bersifat murni (pure function) dan tidak memutasi parameter asli
    to_encode = data.copy()

    # Menentukan waktu kadaluarsa token berbasis UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Meng-encode token menggunakan secret_key dari settings (config.py)
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    return encoded_jwt