from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # ✅ THIS COLUMN WAS MISSING
    candidate_profile_id = Column(
        Integer,
        ForeignKey("candidate_profiles.id"),
        nullable=False
    )

    status = Column(String, default="applied")

    # ✅ RELATIONSHIP
    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="applications"
    )
