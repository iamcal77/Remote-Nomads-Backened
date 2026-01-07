from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.roles import require_role
from app.models.application import Application
from app.models.candidate_profile import CandidateProfile
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.application import ApplicationResponse
from app.schemas.candidate_profile import CandidateProfileCreate, CandidateProfileResponse
from app.utils.file_upload import save_file
from fastapi import UploadFile, File

router = APIRouter()

@router.post("/profile")
def create_or_update_profile(
    industry: str = Form(...),
    full_name: str = Form(...),
    timezone: str | None = Form(None),
    skills: str | None = Form(None),
    salary_expectation: str | None = Form(None),
    cv: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 🔹 Update user's full name
    user = db.query(User).filter(User.id == user_id).first()
    user.full_name = full_name

    # 🔹 Get or create profile
    profile = db.query(CandidateProfile).filter_by(user_id=user_id).first()

    if not profile:
        profile = CandidateProfile(user_id=user_id)
        db.add(profile)

    profile.industry = industry
    profile.timezone = timezone
    profile.skills = skills
    profile.salary_expectation = salary_expectation

    # 🔹 Handle CV upload
    if cv:
        path = save_file(cv, folder="cvs")
        profile.cv_path = path

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile created/updated successfully",
        "profile_id": profile.id
    }

@router.get("/profile", response_model=CandidateProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("candidate"))
):
    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.user_id == current_user["user_id"])
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    user = db.query(User).filter(User.id == current_user["user_id"]).first()

    return {
        "id": profile.id,
        "industry": profile.industry,
        "timezone": profile.timezone,
        "skills": profile.skills,
        "salary_expectation": profile.salary_expectation,
        "cv_path": profile.cv_path,
        "full_name": user.full_name,
        "email": user.email
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
