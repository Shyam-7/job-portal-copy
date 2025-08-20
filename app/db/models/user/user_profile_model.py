from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class UserProfile(BaseModel):
    __tablename__ = 'user_profiles'
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, unique=True)
    headline = Column(String(255))
    phone_number = Column(String(50))
    location = Column(String(255))
    about = Column(Text)
    experience = Column(Text)
    education = Column(Text)
    skills = Column(Text)
    cover_letter = Column(Text)
    resume_url = Column(String(255))
    job_preferences = Column(JSON)

    user = relationship("User")
