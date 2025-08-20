from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.job.saved_job_schema import SavedJob
from app.services import saved_job_service
from app.core.auth import get_current_user
from app.db.models.user.user_model import User
from app.api.deps import get_db

router = APIRouter(prefix="/api/saved-jobs", tags=["Saved Jobs"])

@router.get("/", response_model=List[SavedJob])
def read_saved_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return saved_job_service.get_saved_jobs(db, user_id=current_user.id)

@router.post("/{job_id}", response_model=SavedJob)
def save_job_for_user(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return saved_job_service.save_job(db, user_id=current_user.id, job_id=job_id)

@router.delete("/{job_id}")
def unsave_job_for_user(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return saved_job_service.unsave_job(db, user_id=current_user.id, job_id=job_id)
