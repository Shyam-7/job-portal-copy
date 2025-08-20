from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class Message(BaseModel):
    __tablename__ = 'messages'

    application_id = Column(String(36), ForeignKey('applications.id'), nullable=False)
    sender_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    recipient_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)

    application = relationship("Application")
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
