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
    candidate_profile: CandidateProfileResponse  # include nested profile

    class Config:
        orm_mode = True