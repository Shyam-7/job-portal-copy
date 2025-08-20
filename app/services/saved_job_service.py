from sqlalchemy.orm import Session
from app.db.models.job.saved_job_model import SavedJob
from app.db.schemas.job.saved_job_schema import SavedJobCreate
from fastapi import HTTPException

def get_saved_jobs(db: Session, user_id: str):
    return db.query(SavedJob).filter(SavedJob.user_id == user_id).all()

def save_job(db: Session, user_id: str, job_id: str):
    db_saved_job = db.query(SavedJob).filter(SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
    if db_saved_job:
        raise HTTPException(status_code=400, detail="Job already saved")

    db_saved_job = SavedJob(user_id=user_id, job_id=job_id)
    db.add(db_saved_job)
    db.commit()
    db.refresh(db_saved_job)
    return db_saved_job

def unsave_job(db: Session, user_id: str, job_id: str):
    db_saved_job = db.query(SavedJob).filter(SavedJob.user_id == user_id, SavedJob.job_id == job_id).first()
    if not db_saved_job:
        raise HTTPException(status_code=404, detail="Saved job not found")

    db.delete(db_saved_job)
    db.commit()
    return {"message": "Job unsaved successfully"}
