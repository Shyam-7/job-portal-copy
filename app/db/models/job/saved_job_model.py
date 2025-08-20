from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class SavedJob(BaseModel):
    __tablename__ = 'saved_jobs'
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    job_id = Column(String(36), ForeignKey('jobs.id'), nullable=False)

    user = relationship("User")
    job = relationship("Job")
