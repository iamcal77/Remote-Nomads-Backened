from pydantic import BaseModel
from typing import Optional
from datetime import date

class JobCreate(BaseModel):
    title: str
    description: Optional[str]
    client_name: Optional[str]
    industry: Optional[str]
    skills: Optional[str]
    salary_range: Optional[str]
    timezone: Optional[str]
    expiry_date: Optional[date]
    location: Optional[str]
    status: Optional[str]

# Output schema for API responses
class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    client_name: Optional[str] = None
    industry: str
    skills: str
    salary_range: Optional[str] = None
    timezone: Optional[str] = None
    expiry_date: date
    status: str
    location: Optional[str] = None
    created_at: date

    class Config:
        orm_mode = True 

class JobUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: str
    client_name: Optional[str]
    industry: Optional[str]
    skills: Optional[str]
    salary_range: Optional[str]
    timezone: Optional[str]
    expiry_date: Optional[date]
    location: Optional[str]
    