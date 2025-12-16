
from sqlalchemy import Column, Integer, ForeignKey, String
from app.core.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    status = Column(String, default="applied")

    candidate_profile = Column(JSONB, nullable=True)  # <-- store candidate profile here
