from sqlalchemy.orm import Session
from app.db.models.user.user_model import User
from app.db.models.user.user_profile_model import UserProfile
from app.db.schemas.user.user_schema import UserCreate, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException
from app.db.models.user.password_reset_token_model import PasswordResetToken
import uuid
from datetime import datetime, timedelta

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password,
        role=user.role,
        status=user.status,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create a user profile
    db_profile = UserProfile(user_id=db_user.id)
    db.add(db_profile)
    db.commit()

    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def forgot_password(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=1)

    db_token = PasswordResetToken(email=email, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    # In a real application, you would send an email to the user with the token.
    # For now, we will just return the token.
    return {"message": "Password reset token sent", "token": token}

def reset_password(db: Session, token: str, new_password: str):
    db_token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(db, db_token.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = get_password_hash(new_password)
    db.delete(db_token)
    db.commit()

    return {"message": "Password reset successful"}

def change_password(db: Session, user_id: str, current_password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    user.password_hash = get_password_hash(new_password)
    db.commit()

    return {"message": "Password changed successfully"}
