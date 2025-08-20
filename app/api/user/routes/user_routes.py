from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.user.user_schema import User, UserStatusUpdate
from app.db.schemas.user.user_profile_schema import UserProfile, UserProfileUpdate
from app.services import user_service
from app.core.auth import get_current_user
from app.core.permissions import get_admin_user
from app.db.models.user.user_model import User as UserModel
from app.api.deps import get_db

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/profile", response_model=UserProfile)
def read_users_me(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return user_service.get_user_profile(db, user_id=current_user.id)

@router.patch("/profile", response_model=UserProfile)
def update_user_me(
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return user_service.update_user_profile(db, user_id=current_user.id, profile_update=profile_update)

@router.post("/profile/resume", response_model=UserProfile)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await user_service.upload_resume(db, user_id=current_user.id, file=file)

@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin_user: UserModel = Depends(get_admin_user)
):
    users = user_service.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: UserModel = Depends(get_admin_user)
):
    # This should probably return the user profile instead of the user model.
    # For now, I will leave it as it is to avoid breaking other parts of the app.
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def remove_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: UserModel = Depends(get_admin_user)
):
    return user_service.delete_user(db, user_id=user_id)

@router.patch("/{user_id}/status", response_model=User)
def update_user_status_by_id(
    user_id: str,
    status_update: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin_user: UserModel = Depends(get_admin_user)
):
    return user_service.update_user_status(db, user_id=user_id, status=status_update.status)
