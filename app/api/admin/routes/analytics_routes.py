from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.admin.analytics_schema import (
    DashboardStats,
    RecentActivity,
    JobCategoryDistribution,
    ApplicationStatusDistribution
)
from app.api.admin.services.analytics_service import (
    get_dashboard_stats,
    get_recent_activity,
    get_job_categories,
    get_application_status,
    get_monthly_trends,
    get_conversion_data,
    get_top_jobs,
    get_user_activity,
    export_report,
    refresh_data
)
from app.core.permissions import get_admin_user
from app.db.models.user.user_model import User
from app.api.deps import get_db

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview", response_model=DashboardStats)
def read_analytics_overview(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_dashboard_stats(db)

@router.get("/recent-activity", response_model=List[RecentActivity])
def read_recent_activity(limit: int = 5, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_recent_activity(db, limit=limit)

@router.get("/job-categories", response_model=List[JobCategoryDistribution])
def read_job_categories(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_job_categories(db)

@router.get("/application-status", response_model=List[ApplicationStatusDistribution])
def read_application_status(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_application_status(db)

@router.get("/monthly-trends", response_model=List[dict])
def read_monthly_trends(months: int = 6, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_monthly_trends(db, months=months)

@router.get("/conversion", response_model=dict)
def read_conversion_data(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_conversion_data(db)

@router.get("/top-jobs", response_model=List[dict])
def read_top_jobs(limit: int = 10, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_top_jobs(db, limit=limit)

@router.get("/user-activity", response_model=List[dict])
def read_user_activity(days: int = 30, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return get_user_activity(db, days=days)

@router.get("/export/{type}")
def export_analytics_report(type: str, db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return export_report(db, type=type)

@router.post("/refresh")
def refresh_analytics_data(db: Session = Depends(get_db), admin_user: User = Depends(get_admin_user)):
    return refresh_data(db)
