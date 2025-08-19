from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.db.schemas.common.base_schema import BaseSchema

class JobBase(BaseModel):
    title: Optional[str] = Field(None, example="Software Engineer")
    company_name: Optional[str] = Field(None, example="Tech Corp")
    location: Optional[str] = Field(None, example="San Francisco, CA")
    employment_type: Optional[str] = Field(None, example="Full-time")
    description: Optional[str] = Field(None, example="We are looking for a talented Software Engineer...")
    requirements: Optional[str] = Field(None, example="- 3+ years of experience...")
    salary_min: Optional[Decimal] = Field(None, example=100000.00)
    salary_max: Optional[Decimal] = Field(None, example=150000.00)
    experience_level: Optional[str] = Field(None, example="Mid-level")
    skills_required: Optional[str] = Field(None, example="Python, FastAPI, Docker")
    benefits: Optional[str] = Field(None, example="Health insurance, 401k, PTO")
    is_remote: Optional[bool] = Field(False, example=True)
    application_deadline: Optional[datetime] = Field(None, example="2025-12-31T23:59:59Z")
    status: Optional[str] = Field('active', example="active")

class JobCreate(JobBase):
    title: str = Field(..., example="Software Engineer")
    company_name: str = Field(..., example="Tech Corp")
    description: str = Field(..., example="We are looking for a talented Software Engineer...")

class JobUpdate(JobBase):
    pass

class Job(JobBase, BaseSchema):
    posted_by: Optional[str] = Field(None, example="user_id_123")

    class Config:
        from_attributes = True
