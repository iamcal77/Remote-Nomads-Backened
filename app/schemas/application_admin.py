from pydantic import BaseModel
from datetime import datetime

class AdminApplicationResponse(BaseModel):
    application_id: int
    job_id: int
    status: str
    applied_at: datetime

    # Candidate info
    full_name: str
    email: str
    industry: str | None
    skills: str | None
    salary_expectation: str | None
    cv_path: str | None

    class Config:
        from_attributes = True
