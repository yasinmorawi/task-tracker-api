from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError  # Opsional untuk menangani race condition

from task_tracker_api.database import get_db
from task_tracker_api.models import User
from task_tracker_api.schemas import UserCreate, UserRead
from task_tracker_api.security import (
    hash_password, 
    verify_password, 
    create_access_token,
)

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post(
        "/register", 
        response_model=UserRead, 
        status_code=status.HTTP_201_CREATED,
)

def register(
    user_in: UserCreate, 
    db: Session = Depends(get_db),
):
    
    # 1. Cek apakah email sudah terdaftar di database
    stmt = select(User).where(User.email == user_in.email)
    existing_user = db.scalars(stmt).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )


    # 2. Jika belum ada, hash password-nya 
    hashed_password = hash_password(user_in.password)

    # 3. Buat instance User baru
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password
    )

    # 4. Simpan ke database dengan proteksi IntegrityError (menangani race condition)
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    # 5. Return user yang baru dibuat
    return new_user


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db),
):
    
    # 1. Query user berdasarkan email (di OAuth2PasswordRequestForm, input email ditampung di field .username)
    stmt = select(User).where(User.email == form_data.username)
    user = db.scalars(stmt).first()


    # 2. Validasi keberadaan user dan kecocokan password
    # Pesan error disamakan untuk mencegah user enumeration attack
    if not user or not verify_password(
        form_data.password, 
        user.hashed_password,
    ):
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


    # 3. Jika valid, buat access token JWT dengan payload 'sub' berisi email user
    access_token = create_access_token(
        data={"sub": user.email}
    )


    # 4. Return token beserta tipe tokennya
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }