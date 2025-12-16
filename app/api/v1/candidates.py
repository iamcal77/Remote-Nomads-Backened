from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.roles import require_role
from app.models.application import Application
from app.models.candidate_profile import CandidateProfile
from app.dependencies.auth import get_current_user
from app.schemas.application import ApplicationResponse
from app.schemas.candidate_profile import CandidateProfileCreate, CandidateProfileResponse
from app.utils.file_upload import save_file
from fastapi import UploadFile, File

router = APIRouter()

@router.post("/profile")
def create_or_update_profile(
    payload: CandidateProfileCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    profile = db.query(CandidateProfile).filter_by(user_id=user_id).first()

    if profile:
        # Update existing
        profile.industry = payload.industry
        profile.timezone = payload.timezone
        profile.skills = payload.skills
        profile.salary_expectation = payload.salary_expectation
    else:
        # Create new
        profile = CandidateProfile(
            user_id=user_id,
            industry=payload.industry,
            timezone=payload.timezone,
            skills=payload.skills,
            salary_expectation=payload.salary_expectation
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile created/updated successfully",
        "id": profile.id
    }

#get my applications
@router.get("/my-applications", response_model=list[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    return (
        db.query(Application)
        .filter(Application.user_id == current_user["user_id"])
        .all()
    )


# cv uoload endpoint
@router.post("/profile/upload-cv")
def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    profile = db.query(CandidateProfile).filter_by(
        user_id=current_user["user_id"]
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    path = save_file(file, folder="cvs")
    profile.cv_path = path

    db.commit()

    return {"cv_path": path}
