from sqlalchemy.orm import Session
from app.db.models.content.content_model import SiteContent
from app.db.schemas.content.content_schema import SiteContentCreate, SiteContentUpdate
from fastapi import HTTPException

def get_all_content(db: Session):
    return db.query(SiteContent).order_by(SiteContent.section_type, SiteContent.title).all()

def get_content_by_section(db: Session, section: str):
    # Since the content table doesn't have section field, search by title
    return db.query(SiteContent).filter(SiteContent.title.ilike(f'%{section}%')).first()

def get_content_by_section_type(db: Session, section_type: str):
    return db.query(SiteContent).filter(SiteContent.section_type == section_type).order_by(SiteContent.title).all()

def create_content(db: Session, content: SiteContentCreate):
    db_content = db.query(SiteContent).filter(SiteContent.title == content.title).first()
    if db_content:
        raise HTTPException(status_code=400, detail="Content with this title already exists")
    db_content = SiteContent(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def update_content(db: Session, content_id: str, content_update: SiteContentUpdate):
    db_content = db.query(SiteContent).filter(SiteContent.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")

    update_data = content_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_content, key, value)

    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def delete_content(db: Session, content_id: str):
    db_content = db.query(SiteContent).filter(SiteContent.id == content_id).first()
    if not db_content:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(db_content)
    db.commit()
    return {"message": "Content deleted successfully"}

def get_user_dashboard_content(db: Session):
    dashboard_content = db.query(SiteContent).filter(SiteContent.section == "user-dashboard").first()
    if not dashboard_content:
        # Return default content if nothing is found in the database
        return {
          'hero': {
            'title': 'Find Your Dream Job',
            'subtitle': 'Connect with top employers and discover opportunities that match your skills.',
            'searchSuggestions': 'Software Engineer, Marketing Manager, Data Analyst',
            'ctaButtonText': 'Find Job'
          }
        }
    return dashboard_content.additional_data
