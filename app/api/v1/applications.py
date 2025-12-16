from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application import Application
from app.models.candidate_profile import CandidateProfile
from app.schemas.application import ApplicationCreate, ApplicationResponse, CandidateProfileResponse
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role

router = APIRouter()

# Candidate applies for a job
@router.post("/", response_model=ApplicationResponse)
def apply_for_job(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    user_id = current_user["user_id"]

    profile = db.query(CandidateProfile).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Please create your candidate profile before applying"
        )

    application = Application(
        user_id=user_id,
        job_id=payload.job_id,
        candidate_profile_id=profile.id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


# Internal users view applications for a job
@router.get("/jobs/{job_id}", response_model=list[ApplicationResponse])
def get_applications_for_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    applications = (
        db.query(Application)
        .filter(Application.job_id == job_id)
        .all()
    )
    return applications



