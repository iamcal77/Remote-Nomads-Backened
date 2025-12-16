from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse, JobStatusUpdate
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
@router.patch("/{job_id}/status")
def update_job_status(
    job_id: int,
    status_update: JobStatusUpdate,  # JSON body
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db_job.status = status_update.status  # get status from JSON
    db.commit()
    db.refresh(db_job)
    
    return db_job

# List all jobs (any authenticated user)
@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin","recruiter","manager","candidate"))):
    return db.query(Job).all()
