from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    recruiter = "recruiter"
    manager = "manager"
    candidate = "candidate"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    full_name = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(String, nullable=True)
    updated_at = Column(String, nullable=True)
