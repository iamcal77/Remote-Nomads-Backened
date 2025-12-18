from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    created_at = Column(Date, server_default="now()")
    updated_at = Column(Date, server_default="now()", onupdate="now()")

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
