from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application import Application
from app.models.candidate_profile import CandidateProfile
from app.schemas.application import ApplicationCreate, ApplicationResponse, CandidateProfileResponse
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from sqlalchemy.orm import joinedload


router = APIRouter()

# Candidate applies for a job
@router.post("/", response_model=ApplicationResponse)
def apply_for_job(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    user_id = current_user["user_id"]

    # Get candidate profile
    profile = db.query(CandidateProfile).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="Please create your candidate profile before applying"
        )

    # Create application
    application = Application(
        user_id=user_id,
        job_id=payload.job_id,
        candidate_profile_id=profile.id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    # Map to response
    response = {
        "id": application.id,
        "user_id": application.user_id,
        "job_id": application.job_id,
        "status": application.status,
        "full_name": profile.user.full_name,   # get from user relationship
        "cv_path": profile.cv_path,
        "applied_at": application.created_at
    }

    return response



# Internal users view applications for a job
@router.get("/jobs/{job_id}/applications", response_model=list[ApplicationResponse])
def get_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate_profile).joinedload(CandidateProfile.user)
        )
        .filter(Application.job_id == job_id)
        .all()
    )

    result = []
    for app in applications:
        candidate = app.candidate_profile
        user = candidate.user if candidate else None

        # skip if missing data
        if not user or not candidate:
            continue

        result.append({
            "id": app.id,                        # use 'id' instead of 'application_id'
            "user_id": app.user_id,
            "job_id": app.job_id,
            "status": app.status,                # include status
            "full_name": user.full_name,
            "cv_path": candidate.cv_path,
            "applied_at": app.created_at
        })

    return result



