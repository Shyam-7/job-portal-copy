from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from db_utils import get_db_connection

router = APIRouter(prefix="/api/users", tags=["Users"])

# Schemas
class UserProfile(BaseModel):
    id: str
    email: str
    name: Optional[str]
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserStatusUpdate(BaseModel):
    status: str

@router.get("/profile", response_model=UserProfile)
def get_user_profile():
    """Get current user profile"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()  # Remove dictionary=True
        
        # In a real app, get user_id from JWT token
        user_id = "a0a1c6b8-d735-4367-b901-6039115a1d16"  # Test User for testing
        
        cursor.execute("""
            SELECT id, email, name, role, status, created_at, updated_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserProfile(**user)
    finally:
        connection.close()

@router.put("/profile", response_model=UserProfile)
def update_user_profile(user_update: UserUpdate):
    """Update current user profile"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # In a real app, get user_id from JWT token
        user_id = "550e8400-e29b-41d4-a716-446655440001"  # John Doe for testing
        
        # Build update query
        update_fields = []
        params = []
        
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            update_fields.append(f"{field} = %s")
            params.append(value)
        
        if update_fields:
            params.append(user_id)
            cursor.execute(f"""
                UPDATE users 
                SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP 
                WHERE id = %s
            """, params)
            connection.commit()
        
        # Fetch updated user
        cursor.execute("""
            SELECT id, email, name, role, status, created_at, updated_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        return UserProfile(**user)
    finally:
        connection.close()

@router.patch("/profile", response_model=UserProfile)
def patch_user_profile(user_update: UserUpdate):
    """Update current user profile (PATCH method for frontend compatibility)"""
    return update_user_profile(user_update)

@router.get("/{user_id}", response_model=UserProfile)
def get_user_by_id(user_id: str):
    """Get user by ID - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT id, email, name, role, status, created_at, updated_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserProfile(**user)
    finally:
        connection.close()

@router.delete("/{user_id}")
def delete_user(user_id: str):
    """Delete user - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        # Soft delete by setting status to 'deleted'
        cursor.execute("""
            UPDATE users 
            SET status = 'deleted', updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (user_id,))
        connection.commit()
        cursor.close()
        
        return {"message": "User deleted successfully"}
    finally:
        connection.close()

@router.patch("/{user_id}/status", response_model=UserProfile)
def update_user_status(user_id: str, status_update: UserStatusUpdate):
    """Update user status - Admin only"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update status
        cursor.execute("""
            UPDATE users 
            SET status = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (status_update.status, user_id))
        connection.commit()
        
        # Fetch updated user
        cursor.execute("""
            SELECT id, email, name, role, status, created_at, updated_at
            FROM users 
            WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        return UserProfile(**user)
    finally:
        connection.close()
