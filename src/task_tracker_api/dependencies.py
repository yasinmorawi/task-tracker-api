from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlmodel import Session, select

from task_tracker_api.database import get_db
from task_tracker_api.models import User
from task_tracker_api.config import settings


ALGORITHM = "HS256"
# # OAuth2PasswordBearer mendefinisikan tokenUrl untuk dokumentasi Swagger UI (/docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db),
) -> User: 
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        # 1. DEcode token menggunakan secret_key dan algoritma yang aktif 
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])

        # 2. Ambil niali 'sub' (email) dari payload token 
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError: 
        # Jika token invalid, rusak, atau expired
        raise credentials_exception

    # 3. Cari user di database berdasarkan email dari token
    stmt = select(User).where(User.email == email)
    user = db.scalars(stmt).first()

    if user is None: 
        raise credentials_exception

    # 4. Return objek user yang valid untuk digunakan di endpoint terproteksi 
    return user