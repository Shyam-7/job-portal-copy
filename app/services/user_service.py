from sqlalchemy.orm import Session
from app.db.models.user.user_model import User
from app.db.models.user.user_profile_model import UserProfile
from app.db.schemas.user.user_profile_schema import UserProfileUpdate
import os
import uuid
from fastapi import HTTPException, UploadFile
import aiofiles

async def upload_resume(db: Session, user_id: str, file: UploadFile):
    profile = get_user_profile(db, user_id)

    # Create resumes directory if it doesn't exist
    resumes_dir = "resumes"
    os.makedirs(resumes_dir, exist_ok=True)

    # Generate a unique filename
    file_extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(resumes_dir, filename)

    # Save the file
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Update the user's profile with the resume URL
    profile.resume_url = file_path
    db.commit()
    db.refresh(profile)
    return profile

def get_user_profile(db: Session, user_id: str):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user_profile(db: Session, user_id: str, profile_update: UserProfileUpdate):
    profile = get_user_profile(db, user_id)
    update_data = profile_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

def delete_user(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        db.delete(profile)

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

def update_user_status(db: Session, user_id: str, status: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = status
    db.commit()
    db.refresh(user)
    return user
