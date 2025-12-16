from pydantic import BaseModel

class CandidateProfileCreate(BaseModel):
    industry: str
    timezone: str | None = None
    skills: str | None = None
    salary_expectation: str | None = None

class CandidateProfileResponse(BaseModel):
    id: int
    industry: str
    timezone: str | None = None
    skills: str | None = None
    salary_expectation: str | None = None
    cv_path: str | None = None

    class Config:
        from_attributes = True  # <-- allows SQLAlchemy model to pydantic conversion
