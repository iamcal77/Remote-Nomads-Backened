from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, UserRole
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest  # import the models

router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Ensure role is valid
    try:
        role_enum = UserRole(request.role.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        email=request.email,
        password=hash_password(request.password),
        role=role_enum
    )
    db.add(user)
    db.commit()
    return {"message": "User registered"}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": user.id,        # ✅ REQUIRED
        "email": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
