from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.dependencies.roles import require_role

router = APIRouter()

# Create a new job (Admin only)
@router.post("/", response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# Update job status (Admin only)
@router.put("/{job_id}/jobs")
def update_job_status(
    job_id: int,
    status_update: JobUpdate,  # JSON body
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.status = status_update.status
    db_job.title = status_update.title or db_job.title
    db_job.description = status_update.description or db_job.description
    db_job.client_name = status_update.client_name or db_job.client_name
    db_job.industry = status_update.industry or db_job.industry
    db_job.skills = status_update.skills or db_job.skills
    db_job.salary_range = status_update.salary_range or db_job.salary_range
    db_job.timezone = status_update.timezone or db_job.timezone
    db_job.expiry_date = status_update.expiry_date or db_job.expiry_date
    db_job.location = status_update.location or db_job.location
    db.commit()
    db.refresh(db_job)
    
    return db_job

# List all jobs (any authenticated user)
@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin","recruiter","manager","candidate"))):
    return db.query(Job).all()

# Get a job by ID (any authenticated user)
@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin", "recruiter", "manager", "candidate"))
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
