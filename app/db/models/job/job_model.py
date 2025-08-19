from sqlalchemy import Column, String, Text, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Job(BaseModel):
    __tablename__ = 'jobs'
    title = Column(String(255))
    company_name = Column(String(255))
    location = Column(String(255))
    employment_type = Column(String(100))
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Numeric(10, 2))
    salary_max = Column(Numeric(10, 2))
    experience_level = Column(String(100))
    skills_required = Column(Text)
    benefits = Column(Text)
    is_remote = Column(Boolean, default=False)
    application_deadline = Column(DateTime)
    posted_by = Column(String(36), ForeignKey('users.id'))
    status = Column(String(50), default='active')

    poster = relationship("User")
