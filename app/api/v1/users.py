from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.core.security import hash_password

router = APIRouter()

# -------------------- CREATE USER --------------------
@router.post("/", response_model=dict)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        full_name=user.full_name,     # ✅ FIX
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
        status=user.status or "active"  # ✅ FIX (safe default)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role,
        "full_name": new_user.full_name,
        "status": new_user.status
    }


# -------------------- GET ALL USERS --------------------
@router.get("/", response_model=List[dict])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "role": u.role, "full_name":u.full_name, "status":u.status} for u in users]

# -------------------- GET USER BY ID --------------------
@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("admin", "manager"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email, "role": user.role}

# -------------------- UPDATE USER --------------------
@router.put("/{user_id}", response_model=dict)
def update_user(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = updated_user.email
    user.role = updated_user.role
    user.full_name = updated_user.full_name
    user.status = updated_user.status
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "role": user.role}

# -------------------- DELETE USER --------------------
@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("admin"))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted"}
