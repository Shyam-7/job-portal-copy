from pydantic import BaseModel
from typing import Optional, Any
from app.db.schemas.common.base_schema import BaseSchema
from .user_schema import User

class UserProfileBase(BaseModel):
    headline: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    about: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    job_preferences: Optional[Any] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase, BaseSchema):
    user_id: str
    user: User

    class Config:
        from_attributes = True
