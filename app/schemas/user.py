from pydantic import BaseModel
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole
