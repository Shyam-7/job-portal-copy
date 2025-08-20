from sqlalchemy.orm import Session
from app.db.models.communication.announcement_model import Announcement
from app.db.models.communication.notification_model import Notification
from app.db.models.communication.notification_preference_model import NotificationPreference
from app.db.models.communication.message_model import Message
from app.db.models.job.application_model import Application
from app.db.schemas.communication.announcement_schema import AnnouncementCreate, AnnouncementUpdate
from app.db.schemas.communication.notification_preference_schema import NotificationPreferenceUpdate
from app.db.schemas.communication.message_schema import MessageCreate
from fastapi import HTTPException
from datetime import datetime

# Messages
def get_messages_for_application(db: Session, application_id: str, user_id: str, user_role: str):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.user_id != user_id and user_role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to view messages for this application")

    messages = db.query(Message).filter(Message.application_id == application_id).all()
    return messages

def create_message(db: Session, message: MessageCreate, user_id: str, user_role: str):
    application = db.query(Application).filter(Application.id == message.application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.user_id != user_id and user_role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to send messages for this application")

    db_message = Message(**message.dict(), sender_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# Announcements
def get_announcements(db: Session, status: str = None):
    query = db.query(Announcement)
    if status:
        query = query.filter(Announcement.status == status)
    return query.all()

def create_announcement(db: Session, announcement: AnnouncementCreate, user_id: str):
    db_announcement = Announcement(**announcement.dict(), created_by=user_id)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def get_announcement_stats(db: Session):
    return {
        "total": db.query(Announcement).count(),
        "draft": db.query(Announcement).filter(Announcement.status == 'draft').count(),
        "scheduled": db.query(Announcement).filter(Announcement.status == 'scheduled').count(),
        "sent": db.query(Announcement).filter(Announcement.status == 'sent').count(),
    }

def update_announcement(db: Session, announcement_id: str, announcement_update: AnnouncementUpdate):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    update_data = announcement_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_announcement, key, value)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def cancel_scheduled_announcement(db: Session, announcement_id: str):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    if db_announcement.status != 'scheduled':
        raise HTTPException(status_code=400, detail="Announcement is not scheduled")
    db_announcement.status = 'cancelled'
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Notifications
def get_user_notifications(db: Session, user_id: str):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

def mark_notification_as_read(db: Session, notification_id: str, user_id: str):
    db_notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if not db_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db_notification.is_read = True
    db_notification.read_at = datetime.utcnow()
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def mark_all_notifications_as_read(db: Session, user_id: str):
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({"is_read": True, "read_at": datetime.utcnow()})
    db.commit()
    return {"message": "All notifications marked as read"}

# Notification Preferences
def get_notification_preferences(db: Session, user_id: str):
    preferences = db.query(NotificationPreference).filter(NotificationPreference.user_id == user_id).first()
    if not preferences:
        # Create default preferences if they don't exist
        preferences = NotificationPreference(user_id=user_id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    return preferences

def update_notification_preferences(db: Session, user_id: str, preferences_update: NotificationPreferenceUpdate):
    db_preferences = get_notification_preferences(db, user_id)
    update_data = preferences_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_preferences, key, value)
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def send_custom_notification(db: Session, user_id: str, title: str, message: str):
    db_notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type='custom'
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
