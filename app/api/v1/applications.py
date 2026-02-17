import mimetypes
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.application import Application
from app.models.candidate_profile import CandidateProfile
from app.schemas.application import ApplicationCreate, ApplicationResponse, CandidateProfileResponse, StatusUpdateRequest
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from sqlalchemy.orm import joinedload

from app.schemas.application_admin import AdminApplicationResponse
from app.schemas.candidate_profile import CandidateJobStatusResponse


router = APIRouter()
BASE_DIR = Path(__file__).resolve().parents[2]  # /app

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
        raise HTTPException(400, "Please create your candidate profile before applying")

    #  Prevent re-application
    existing_application = (
        db.query(Application)
        .filter(
            Application.user_id == user_id,
            Application.job_id == payload.job_id
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="You have already applied for this job"
        )

    application = Application(
        user_id=user_id,
        job_id=payload.job_id,
        candidate_profile_id=profile.id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "id": application.id,
        "user_id": application.user_id,
        "job_id": application.job_id,
        "status": application.status,
        "full_name": profile.user.full_name,
        "cv_path": profile.cv_path,
        "applied_at": application.created_at
    }




# Internal users view applications for a job
@router.get("/", response_model=list[AdminApplicationResponse])
def admin_view_all_applications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    # Fetch all applications with candidate profile, user, and job
    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate_profile)
            .joinedload(CandidateProfile.user),
            joinedload(Application.job)  # load job relationship
        )
        .all()
    )

    results = []
    for app in applications:
        print("Here is me",app.job_id,app.job)
        profile = app.candidate_profile
        user = profile.user if profile else None
        job = app.job

        if not profile or not user or not job:
            continue

        results.append({
            "application_id": app.id,
            "job_id": app.job_id,
            "job_title": job.title,  # include job name
            "status":app.status,
            "applied_at": app.created_at,
            "full_name": user.full_name,
            "email": user.email,
            "industry": profile.industry,
            "skills": profile.skills,
            "salary_expectation": profile.salary_expectation,
            "cv_path": profile.cv_path
        })

    return results

@router.get("/cv/{application_id}/download")
def download_cv(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    application = (
        db.query(Application)
        .options(joinedload(Application.candidate_profile))
        .filter(Application.id == application_id)
        .first()
    )

    if not application or not application.candidate_profile:
        raise HTTPException(status_code=404, detail="CV not found")

    path = application.candidate_profile.cv_path

    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="CV file missing")

    return FileResponse(path, filename=os.path.basename(path))

@router.get("/cv/{application_id}/view")
def view_cv(application_id: int, db: Session = Depends(get_db), current_user: dict = Depends(require_role("admin"))):
    application = (
        db.query(Application)
        .options(joinedload(Application.candidate_profile))
        .filter(Application.id == application_id)
        .first()
    )

    if not application or not application.candidate_profile:
        raise HTTPException(404, "CV not found")

    relative_path = application.candidate_profile.cv_path
    if not relative_path:
        raise HTTPException(404, "CV not found")

    absolute_path = BASE_DIR / relative_path

    if not absolute_path.exists():
        raise HTTPException(404, "CV file missing")

    media_type, _ = mimetypes.guess_type(str(absolute_path))

    return FileResponse(
        str(absolute_path),
        media_type=media_type or "application/pdf",
        headers={"Content-Disposition": "inline"}
    )

@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    payload: StatusUpdateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin", "recruiter"))
):
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    allowed_statuses = ["pending", "reviewed", "shortlisted", "accepted", "rejected"]
    if payload.status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    app.status = payload.status
    db.commit()
    db.refresh(app)

    return {"application_id": app.id, "status": app.status}


@router.get("/candidate/dashboard", response_model=list[CandidateJobStatusResponse])
def candidate_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    user_id = current_user["user_id"]

    applications = (
        db.query(Application)
        .options(joinedload(Application.job))
        .filter(Application.user_id == user_id)
        .order_by(Application.created_at.desc())
        .all()
    )

    return [
        {
            "application_id": app.id,
            "job_id": app.job_id,
            "job_title": app.job.title,
            "status": app.status,
            "applied_at": app.created_at
        }
        for app in applications
    ]