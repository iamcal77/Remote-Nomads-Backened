from pydantic import BaseModel
from typing import Optional

class CandidateProfileCreate(BaseModel):
    industry: Optional[str]
    timezone: Optional[str]
    skills: Optional[str]
    salary_expectation: Optional[str]
