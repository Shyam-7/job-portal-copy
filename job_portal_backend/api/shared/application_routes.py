from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from db_utils import get_db_connection

router = APIRouter(prefix="/api/applications", tags=["Applications"])

# Schemas
class ApplicationCreate(BaseModel):
    job_id: str
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None

class Application(BaseModel):
    id: str
    job_id: str
    user_id: str
    cover_letter: Optional[str]
    resume_url: Optional[str]
    status: str
    applied_at: datetime
    updated_at: datetime
    # Optional fields from joins
    job_title: Optional[str] = None
    job_company: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    cover_letter: Optional[str] = None

@router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate):
    """Apply for a job"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # In a real app, get user_id from JWT token
        # For now, using a real user from database for testing
        user_id = "a0a1c6b8-d735-4367-b901-6039115a1d16"  # Test User
        
        # Check if user already applied for this job
        cursor.execute("""
            SELECT id FROM applications 
            WHERE user_id = %s AND job_id = %s
        """, (user_id, application.job_id))
        
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied for this job"
            )
        
        # Create application
        cursor.execute("""
            INSERT INTO applications (job_id, user_id, cover_letter, resume_url, status)
            VALUES (%s, %s, %s, %s, 'applied')
            RETURNING id
        """, (
            application.job_id, user_id, 
            application.cover_letter, application.resume_url
        ))
        
        app_id = cursor.fetchone()['id']
        connection.commit()
        
        # Fetch created application
        cursor.execute("""
            SELECT id, job_id, user_id, cover_letter, resume_url, 
                   status, applied_at, updated_at
            FROM applications 
            WHERE id = %s
        """, (app_id,))
        app = cursor.fetchone()
        cursor.close()
        
        if app:
            return Application(**dict(app))
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    finally:
        connection.close()

@router.get("/user", response_model=List[Application])
def get_current_user_applications():
    """Get current user's applications - matches frontend expectation"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # In a real app, get user_id from JWT token
        user_id = "a0a1c6b8-d735-4367-b901-6039115a1d16"  # Test User
        
        cursor.execute("""
            SELECT a.id, a.job_id, a.user_id, a.cover_letter, a.resume_url, 
                   a.status, a.applied_at, a.updated_at,
                   j.title as job_title, j.company_name as job_company
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.user_id = %s
            ORDER BY a.applied_at DESC
        """, (user_id,))
        
        applications = cursor.fetchall()
        cursor.close()
        
        return [Application(**dict(app)) for app in applications]
    finally:
        connection.close()

@router.get("/me", response_model=List[Application])
def get_my_applications():
    """Get current user's applications - legacy endpoint"""
    return get_current_user_applications()

@router.get("/user/{user_id}", response_model=List[Application])
def get_user_applications(user_id: str):
    """Get applications for specific user - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT a.id, a.job_id, a.user_id, a.cover_letter, a.resume_url, 
                   a.status, a.applied_at, a.updated_at,
                   j.title as job_title, j.company_name as job_company,
                   u.name as user_name, u.email as user_email
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.user_id = u.id
            WHERE a.user_id = %s
            ORDER BY a.applied_at DESC
        """, (user_id,))
        
        applications = cursor.fetchall()
        cursor.close()
        
        return [Application(**dict(app)) for app in applications]
    finally:
        connection.close()

@router.put("/{application_id}", response_model=Application)
def update_application(application_id: str, application_update: ApplicationUpdate):
    """Update application status"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if application exists
        cursor.execute("SELECT id FROM applications WHERE id = %s", (application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Build update query
        update_fields = []
        params = []
        
        update_data = application_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            update_fields.append(f"{field} = %s")
            params.append(value)
        
        if update_fields:
            params.append(application_id)
            cursor.execute(f"""
                UPDATE applications 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, params)
            connection.commit()
        
        # Fetch updated application
        cursor.execute("""
            SELECT id, job_id, user_id, cover_letter, resume_url, status, applied_at, updated_at
            FROM applications 
            WHERE id = %s
        """, (application_id,))
        app = cursor.fetchone()
        cursor.close()
        
        if app:
            return Application(**dict(app))
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    finally:
        connection.close()

@router.delete("/{application_id}")
def withdraw_application(application_id: str):
    """Withdraw application"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if application exists
        cursor.execute("SELECT id FROM applications WHERE id = %s", (application_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Update status to withdrawn
        cursor.execute("""
            UPDATE applications 
            SET status = 'withdrawn', updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (application_id,))
        connection.commit()
        cursor.close()
        
        return {"message": "Application withdrawn successfully"}
    finally:
        connection.close()
