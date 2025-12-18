from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    industry = Column(String)
    timezone = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    salary_expectation = Column(String, nullable=True)
    cv_path = Column(String, nullable=True)
    user = relationship("User")

    applications = relationship(
        "Application",
        back_populates="candidate_profile"
    )
