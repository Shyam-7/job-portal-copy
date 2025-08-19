from sqlalchemy import Column, String, Text, Integer, Boolean, JSON
from app.db.base import BaseModel

class SiteContent(BaseModel):
    __tablename__ = 'content'
    title = Column(String(255), nullable=False)
    content = Column(Text)
    content_type = Column(String(100))
    status = Column(String(50))
    tags = Column(JSON)
    view_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
