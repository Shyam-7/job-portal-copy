from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from db_utils import get_db_connection

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

# Schemas
class Job(BaseModel):
    id: str
    title: str
    company_name: str
    description: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    employment_type: str
    status: str = "active"
    created_at: datetime
    updated_at: datetime

class JobCreate(BaseModel):
    title: str
    company_name: str
    description: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    employment_type: str = "full-time"

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    employment_type: Optional[str] = None
    status: Optional[str] = None

@router.get("/", response_model=List[Job])
def get_all_jobs():
    """Get all active jobs"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, company_name, description, location, salary_min, salary_max, 
                   employment_type, status, created_at, updated_at 
            FROM jobs 
            WHERE status = 'active' 
            ORDER BY created_at DESC
        """)
        jobs = cursor.fetchall()
        cursor.close()
        return [Job(**job) for job in jobs]
    finally:
        connection.close()

@router.get("/search")
def search_jobs(q: Optional[str] = None, location: Optional[str] = None, job_type: Optional[str] = None):
    """Search jobs with filters"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        where_conditions = ["status = 'active'"]
        params = []
        
        if q:
            where_conditions.append("(title LIKE %s OR description LIKE %s OR company_name LIKE %s)")
            search_term = f"%{q}%"
            params.extend([search_term, search_term, search_term])
        
        if location:
            where_conditions.append("location LIKE %s")
            params.append(f"%{location}%")
        
        if job_type:
            where_conditions.append("employment_type = %s")
            params.append(job_type)
        
        query = f"""
            SELECT id, title, company_name, description, location, salary_min, salary_max, 
                   employment_type, status, created_at, updated_at 
            FROM jobs 
            WHERE {' AND '.join(where_conditions)}
            ORDER BY created_at DESC
        """
        
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        cursor.close()
        return [Job(**job) for job in jobs]
    finally:
        connection.close()

@router.get("/{job_id}", response_model=Job)
def get_job_by_id(job_id: str):
    """Get job by ID"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, company_name, description, location, salary_min, salary_max, 
                   employment_type, status, created_at, updated_at 
            FROM jobs 
            WHERE id = %s
        """, (job_id,))
        job = cursor.fetchone()
        cursor.close()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return Job(**job)
    finally:
        connection.close()

@router.post("/", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(job_data: JobCreate):
    """Create new job - Admin/Employer only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Insert new job
        cursor.execute("""
            INSERT INTO jobs (title, company_name, description, location, salary_min, salary_max, 
                            employment_type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'active')
            RETURNING id, title, company_name, description, location, salary_min, salary_max, 
                     employment_type, status, created_at, updated_at
        """, (
            job_data.title, job_data.company_name, job_data.description,
            job_data.location, job_data.salary_min, job_data.salary_max, 
            job_data.employment_type
        ))
        
        job = cursor.fetchone()
        connection.commit()
        cursor.close()
        
        return Job(**job)
    finally:
        connection.close()

@router.put("/{job_id}", response_model=Job)
def update_job(job_id: str, job_update: JobUpdate):
    """Update job - Admin/Employer only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if job exists
        cursor.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Build update query
        update_fields = []
        params = []
        
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            update_fields.append(f"{field} = %s")
            params.append(value)
        
        if update_fields:
            params.append(job_id)
            cursor.execute(f"""
                UPDATE jobs 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, params)
            connection.commit()
        
        # Fetch updated job
        cursor.execute("""
            SELECT id, title, company_name, description, location, salary_min, salary_max, 
                   employment_type, status, created_at, updated_at 
            FROM jobs 
            WHERE id = %s
        """, (job_id,))
        job = cursor.fetchone()
        cursor.close()
        
        return Job(**job)
    finally:
        connection.close()

@router.delete("/{job_id}")
def delete_job(job_id: str):
    """Delete job - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if job exists
        cursor.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Soft delete by setting status to 'deleted'
        cursor.execute("""
            UPDATE jobs 
            SET status = 'deleted', updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (job_id,))
        connection.commit()
        cursor.close()
        
        return {"message": "Job deleted successfully"}
    finally:
        connection.close()
