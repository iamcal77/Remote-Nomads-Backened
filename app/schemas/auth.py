from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str  # or UserRole if you want strict enum validation
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
