from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.schemas.job.application_schema import Application, ApplicationCreate, ApplicationUpdate
from app.services import application_service
from app.core.auth import get_current_user, get_optional_current_user
from app.core.permissions import get_admin_user
from app.db.models.user.user_model import User
from app.api.deps import get_db

router = APIRouter(prefix="/api/applications", tags=["Applications"])

from typing import Optional

@router.post("/", response_model=Application)
def apply_for_job(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    user_id = current_user.id if current_user else None
    return application_service.create_application(db, application=application, user_id=user_id)

@router.get("/me", response_model=List[Application])
def read_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return application_service.get_user_applications(db, user_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[Application])
def read_applications_for_user(
    user_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return application_service.get_user_applications(db, user_id=user_id)

@router.get("/job/{job_id}", response_model=List[Application])
def read_applications_for_job(
    job_id: str,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    return application_service.get_job_applications(db, job_id=job_id)

@router.get("/{application_id}", response_model=Application)
def read_application_by_id(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Add logic here to ensure user can only access their own application or if they are admin
    app = application_service.get_application_by_id(db, application_id=application_id)
    if app.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to access this application")
    return app

@router.put("/{application_id}", response_model=Application)
def update_application_status(
    application_id: str,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return application_service.update_application(
        db,
        application_id=application_id,
        application_update=application_update,
        current_user_id=current_user.id,
        user_role=current_user.role
    )

@router.patch("/{application_id}", response_model=Application)
def patch_application_status(
    application_id: str,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return application_service.update_application(
        db,
        application_id=application_id,
        application_update=application_update,
        current_user_id=current_user.id,
        user_role=current_user.role
    )

@router.delete("/{application_id}")
def withdraw_job_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return application_service.withdraw_application(db, application_id=application_id, user_id=current_user.id)
