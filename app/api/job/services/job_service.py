from sqlalchemy.orm import Session
from app.db.models.job.job_model import Job
from app.db.schemas.job.job_schema import JobCreate, JobUpdate
from fastapi import HTTPException

def get_all_active_jobs(db: Session, skip: int = 0, limit: int = 100, title: str = None, location: str = None, sort_by: str = None, experience_level: str = None, salary_min: int = None, salary_max: int = None, company_type: str = None, work_type: str = None):
    query = db.query(Job).filter(Job.status == 'active')

    if title:
        query = query.filter(Job.title.ilike(f"%{title}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if experience_level:
        query = query.filter(Job.experience_level == experience_level)
    if salary_min:
        query = query.filter(Job.salary_min >= salary_min)
    if salary_max:
        query = query.filter(Job.salary_max <= salary_max)
    if company_type:
        query = query.filter(Job.company_type == company_type)
    if work_type:
        if work_type == "remote":
            query = query.filter(Job.is_remote == True)
        else:
            query = query.filter(Job.work_type == work_type)

    if sort_by:
        if sort_by == "newest":
            query = query.order_by(Job.created_at.desc())
        elif sort_by == "oldest":
            query = query.order_by(Job.created_at.asc())
        elif sort_by == "salary":
            query = query.order_by(Job.salary_max.desc())
        elif sort_by == "company":
            query = query.order_by(Job.company_name.asc())
        elif sort_by == "title":
            query = query.order_by(Job.title.asc())

    return query.offset(skip).limit(limit).all()

def get_all_jobs_for_admin(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

def get_job_by_id(db: Session, job_id: str):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

def create_job(db: Session, job: JobCreate, user_id: str):
    db_job = Job(**job.dict(), posted_by=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, job_id: str, job_update: JobUpdate):
    db_job = get_job_by_id(db, job_id)
    update_data = job_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_job, key, value)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: str):
    db_job = get_job_by_id(db, job_id)
    db.delete(db_job)
    db.commit()
    return {"message": "Job deleted successfully"}
