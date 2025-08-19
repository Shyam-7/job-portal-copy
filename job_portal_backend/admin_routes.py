from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from db_utils import get_db_connection

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# Schemas
class UserSummary(BaseModel):
    id: str
    email: str
    name: Optional[str]
    role: str
    status: str
    created_at: str

class JobSummary(BaseModel):
    id: str
    title: str
    company: str
    location: str
    status: str
    created_at: str

class ApplicationSummary(BaseModel):
    id: str
    job_title: str
    user_name: str
    user_email: str
    status: str
    created_at: str

class Analytics(BaseModel):
    total_users: int
    total_jobs: int
    total_applications: int
    active_jobs: int
    pending_applications: int

@router.get("/users", response_model=List[UserSummary])
def get_all_users():
    """Get all users - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()  # RealDictCursor configured in db_utils
        cursor.execute("""
            SELECT id, email, name, role, status, created_at
            FROM users 
            WHERE status != 'deleted'
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        return [UserSummary(**user) for user in users]
    finally:
        connection.close()

@router.get("/jobs", response_model=List[JobSummary])
def get_all_jobs():
    """Get all jobs - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()  # RealDictCursor configured in db_utils
        cursor.execute("""
            SELECT id, title, company, location, status, created_at
            FROM jobs 
            WHERE status != 'deleted'
            ORDER BY created_at DESC
        """)
        jobs = cursor.fetchall()
        cursor.close()
        return [JobSummary(**job) for job in jobs]
    finally:
        connection.close()

@router.get("/applications", response_model=List[ApplicationSummary])
def get_all_applications():
    """Get all applications - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()  # RealDictCursor configured in db_utils
        cursor.execute("""
            SELECT a.id, j.title as job_title, u.name as user_name, 
                   u.email as user_email, a.status, a.created_at
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.id
            ORDER BY a.created_at DESC
        """)
        applications = cursor.fetchall()
        cursor.close()
        return [ApplicationSummary(**app) for app in applications]
    finally:
        connection.close()

@router.get("/analytics", response_model=Analytics)
def get_analytics():
    """Get system analytics - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()  # RealDictCursor configured in db_utils
        
        # Get counts
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE status != 'deleted'")
        total_users = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM jobs WHERE status != 'deleted'")
        total_jobs = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM applications")
        total_applications = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM jobs WHERE status = 'active'")
        active_jobs = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM applications WHERE status = 'submitted'")
        pending_applications = cursor.fetchone()['count']
        
        cursor.close()
        
        return Analytics(
            total_users=total_users,
            total_jobs=total_jobs,
            total_applications=total_applications,
            active_jobs=active_jobs,
            pending_applications=pending_applications
        )
    finally:
        connection.close()
