from datetime import date
from typing import Optional
from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    job_id: int

class CandidateProfileResponse(BaseModel):
    id: int
    industry: str
    timezone: str | None = None
    skills: str | None = None
    salary_expectation: str | None = None
    cv_path: str | None = None

    class Config:
        orm_mode = True  # allows SQLAlchemy model to Pydantic conversion

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    full_name: Optional[str] = None
    cv_path: Optional[str] = None
    applied_at: date
    
    

    class Config:
        orm_mode = True