from sqlalchemy import Column, String, DateTime
from app.db.base import BaseModel

class PasswordResetToken(BaseModel):
    __tablename__ = 'password_reset_tokens'
    email = Column(String(255), primary_key=True)
    token = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
