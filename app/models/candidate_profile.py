from sqlalchemy import Column, Integer, ForeignKey, String, Text
from app.core.database import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    industry = Column(String)
    timezone = Column(String)
    skills = Column(Text)
    salary_expectation = Column(String)
    cv_path = Column(String)
