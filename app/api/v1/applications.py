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
    application = Application(user_id=user_id, job_id=payload.job_id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return {
        "message": "Application submitted successfully",
        "application_id": application.id,
        "status": application.status
    }

# Internal users view applications for a job
@router.get("/jobs/{job_id}", response_model=list[ApplicationResponse])
def get_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    applications = db.query(Application).filter(Application.job_id == job_id).all()

    result = []
    for app in applications:
        candidate_profile_data = app.candidate_profile or {}
        candidate_profile = CandidateProfileResponse(
            id=app.id,  # or proper candidate_profile ID
            industry=candidate_profile_data.get("industry", ""),
            timezone=candidate_profile_data.get("timezone"),
            skills=candidate_profile_data.get("skills"),
            salary_expectation=candidate_profile_data.get("salary_expectation"),
            cv_path=candidate_profile_data.get("cv_path"),
        )
        result.append(ApplicationResponse(
            id=app.id,
            user_id=app.user_id,
            job_id=app.job_id,
            status=app.status,
            candidate_profile=candidate_profile
        ))

    return result


