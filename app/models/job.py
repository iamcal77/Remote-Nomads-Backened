from sqlalchemy import Column, Integer, String, Text, Enum, Date
from app.core.database import Base
import enum

class JobStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    on_hold = "on_hold"
    filled = "filled"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    client_name = Column(String)
    industry = Column(String)
    skills = Column(Text)
    salary_range = Column(String)
    timezone = Column(String)
    expiry_date = Column(Date)
    status = Column(Enum(JobStatus), default=JobStatus.draft)
