from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.schemas.user.user_schema import UserCreate, User, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest
from app.services.auth_service import create_user, authenticate_user, forgot_password, reset_password, change_password
from app.core.auth import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def request_password_reset(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return forgot_password(db, email=request.email)

@router.post("/reset-password")
def reset_user_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    return reset_password(db, token=request.token, new_password=request.new_password)

@router.post("/change-password")
def change_user_password(request: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return change_password(db, user_id=current_user.id, current_password=request.current_password, new_password=request.new_password)
