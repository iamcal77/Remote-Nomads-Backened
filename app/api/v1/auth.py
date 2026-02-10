from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole
from app.core.security import create_password_reset_token, decode_access_token, hash_password, verify_password, create_access_token
from app.schemas.auth import ForgotPasswordRequest, RegisterRequest, LoginRequest, ResetPasswordRequest  # import the models

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        role_enum = UserRole(request.role.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        email=request.email,
        password=hash_password(request.password),
        role=role_enum,
        full_name=request.full_name 
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered"}



@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,       
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
         "role": user.role,
    }

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest, 
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        return {"message": "If the email exists, a reset token was generated"}

    reset_token = create_password_reset_token(user.id)

    return {
        "reset_token": reset_token,
        "expires_in": "15 minutes"
    }

@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    payload_token = payload.token
    new_password = payload.new_password

    decoded = decode_access_token(payload_token)

    if decoded.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid reset token")

    user = db.query(User).filter(User.id == decoded["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    db.commit()

    return {"message": "Password reset successful"}
