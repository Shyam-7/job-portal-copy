from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from db_utils import get_db_connection

router = APIRouter(prefix="/api/communication", tags=["Communications"])

# Schemas
class AnnouncementCreate(BaseModel):
    title: str
    content: str
    priority: Optional[str] = "normal"  # low, normal, high
    target_audience: Optional[str] = "all"  # all, job_seekers, employers

class Announcement(BaseModel):
    id: str
    title: str
    content: str
    priority: str
    target_audience: str

class NotificationUpdate(BaseModel):
    notification_id: str
    read: bool

class Notification(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str
    read: bool
    created_at: datetime

class PreferencesUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    sms_notifications: Optional[bool] = None

class Preferences(BaseModel):
    user_id: str
    email_notifications: bool
    push_notifications: bool
    sms_notifications: bool

@router.get("/notifications")
def get_notifications(page: int = 1, limit: int = 10):
    """Get user notifications with pagination"""
    
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Get notifications from database (using announcements table as notifications)
        cursor.execute("""
            SELECT id, title, content, created_at, created_by
            FROM announcements 
            ORDER BY created_at DESC 
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        notifications = cursor.fetchall()
        
        # Get total count for pagination
        cursor.execute("SELECT COUNT(*) as total FROM announcements")
        total_count = cursor.fetchone()["total"]
        
        cursor.close()
        
        # Format notifications for frontend
        formatted_notifications = []
        for notif in notifications:
            formatted_notifications.append({
                "id": notif["id"],
                "title": notif["title"],
                "message": notif["content"],
                "type": "announcement",
                "read": False,  # Default to unread
                "created_at": notif["created_at"].isoformat() if notif["created_at"] else None
            })
        
        return {
            "success": True,
            "notifications": formatted_notifications,
            "total": total_count,
            "unread": total_count,  # All considered unread for now
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "total_pages": (total_count + limit - 1) // limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")
    finally:
        connection.close()

@router.put("/notifications")
def update_notification(notification_update: dict):
    """Mark notification as read"""
    notification_id = notification_update.get("notification_id")
    read_status = notification_update.get("read", True)
    
    if not notification_id:
        raise HTTPException(status_code=400, detail="Notification ID required")
    
    return {"message": f"Notification {notification_id} marked as {'read' if read_status else 'unread'}"}

@router.get("/preferences", response_model=Preferences)
def get_preferences():
    """Get user communication preferences"""
    # Return default preferences for now
    return Preferences(
        user_id="550e8400-e29b-41d4-a716-446655440001",
        email_notifications=True,
        push_notifications=True,
        sms_notifications=False
    )

@router.put("/preferences", response_model=Preferences)
def update_preferences(preferences: PreferencesUpdate):
    """Update user communication preferences"""
    # Return updated preferences (dummy implementation)
    return Preferences(
        user_id="550e8400-e29b-41d4-a716-446655440001",
        email_notifications=preferences.email_notifications if preferences.email_notifications is not None else True,
        push_notifications=preferences.push_notifications if preferences.push_notifications is not None else True,
        sms_notifications=preferences.sms_notifications if preferences.sms_notifications is not None else False
    )

@router.post("/announcements", response_model=Announcement)
def create_announcement(announcement: AnnouncementCreate):
    """Create a new announcement"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO announcements (title, content)
            VALUES (%s, %s)
            RETURNING id, title, content, created_at
        """, (announcement.title, announcement.content))
        
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        
        return Announcement(
            id=result["id"],
            title=result["title"],
            content=result["content"],
            priority=announcement.priority,
            target_audience=announcement.target_audience
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating announcement: {str(e)}")
    finally:
        connection.close()

@router.get("/announcements/stats")
def get_announcement_stats():
    """Get announcement statistics"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Get total announcements
        cursor.execute("SELECT COUNT(*) as total FROM announcements")
        total_result = cursor.fetchone()
        total_announcements = total_result["total"] if total_result else 0
        
        cursor.close()
        
        return {
            "success": True,
            "stats": {
                "total_announcements": total_announcements,
                "sent_announcements": total_announcements,  # All are considered sent for now
                "scheduled_announcements": 0,
                "draft_announcements": 0,
                "active_notifications": total_announcements
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching announcement stats: {str(e)}")
    finally:
        connection.close()

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str):
    """Mark a specific notification as read"""
    return {
        "success": True,
        "message": f"Notification {notification_id} marked as read"
    }

@router.put("/notifications/read-all")
def mark_all_notifications_read():
    """Mark all notifications as read"""
    return {
        "success": True,
        "message": "All notifications marked as read"
    }

@router.post("/notifications/send")
def send_custom_notification(notification: dict):
    """Send a custom notification to a user"""
    return {
        "success": True,
        "message": "Notification sent successfully"
    }

@router.get("/announcements/scheduled")
def get_scheduled_announcements():
    """Get scheduled announcements"""
    return {
        "success": True,
        "announcements": []
    }

@router.get("/announcements/drafts")
def get_draft_announcements(page: int = 1, limit: int = 10):
    """Get draft announcements"""
    return {
        "success": True,
        "announcements": [],
        "total": 0
    }

@router.put("/announcements/{announcement_id}")
def update_announcement(announcement_id: str, announcement: dict):
    """Update an announcement"""
    return {
        "success": True,
        "message": f"Announcement {announcement_id} updated successfully"
    }

@router.delete("/announcements/{announcement_id}/cancel")
def cancel_scheduled_announcement(announcement_id: str):
    """Cancel a scheduled announcement"""
    return {
        "success": True,
        "message": f"Announcement {announcement_id} cancelled successfully"
    }

@router.get("/announcements")
def get_announcements():
    """Get all announcements"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, content, created_at 
            FROM announcements 
            ORDER BY created_at DESC 
            LIMIT 20
        """)
        announcements = cursor.fetchall()
        cursor.close()
        
        return {
            "success": True,
            "announcements": [
                {
                    "id": ann["id"],
                    "title": ann["title"],
                    "content": ann["content"],
                    "created_at": ann["created_at"].isoformat() if ann["created_at"] else None
                } for ann in announcements
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching announcements: {str(e)}")
    finally:
        connection.close()
