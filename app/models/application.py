from sqlalchemy import Column, Date, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    created_at = Column(Date, server_default="now()")
    updated_at = Column(Date, server_default="now()", onupdate="now()")
    job = relationship("Job", back_populates="applications")
    candidate_profile_id = Column(
        Integer,
        ForeignKey("candidate_profiles.id"),
        nullable=False
    )
    status = Column(String, default="applied")
    candidate_profile = relationship(
        "CandidateProfile",
        back_populates="applications"
    )
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job_application"),
    )

