from pydantic import BaseModel
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole
    full_name: str | None = None
    status: str | None = "active"
    created_at: str | None = None
    updated_at: str | None = None

class UserUpdate(BaseModel):
    email: str | None = None
    role: UserRole | None = None
    full_name: str | None = None
    status: str | None = None