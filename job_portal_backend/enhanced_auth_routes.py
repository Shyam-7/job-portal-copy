from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
import bcrypt
from datetime import datetime
from db_utils import get_db_connection

router = APIRouter(prefix="/api/auth", tags=["Enhanced Authentication"])

# Enhanced Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    role: str
    status: str
    created_at: datetime
    last_active_at: Optional[datetime]

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserProfileResponse
    message: str

def get_user_by_email_with_password(email: str):
    """
    Retrieve complete user information from database including password hash
    This is used for authentication purposes
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # SQL query to retrieve user with all authentication details
        query = """
        SELECT 
            id, 
            name, 
            email, 
            password_hash, 
            role, 
            status,
            created_at,
            last_active_at
        FROM users 
        WHERE email = %s
        """
        
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'password_hash': user['password_hash'],  # This contains the bcrypt hash
                'role': user['role'],
                'status': user['status'],
                'created_at': user['created_at'],
                'last_active_at': user['last_active_at']
            }
        return None
        
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        connection.close()

def verify_user_credentials(plain_password: str, stored_hash: str) -> bool:
    """
    Verify if the provided password matches the stored bcrypt hash
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def update_last_active(user_id: str):
    """
    Update user's last active timestamp after successful login
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET last_active_at = CURRENT_TIMESTAMP WHERE id = %s",
            (user_id,)
        )
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating last active: {e}")
    finally:
        connection.close()

@router.post("/signin", response_model=AuthResponse)
def sign_in_user(login_data: LoginRequest):
    """
    Enhanced sign-in endpoint that retrieves and validates user credentials from PostgreSQL database
    
    Process:
    1. Retrieve user record from database by email
    2. Verify the provided password against stored bcrypt hash
    3. Check if user account is active
    4. Generate access token
    5. Update last active timestamp
    6. Return user profile with token
    """
    
    # Step 1: Retrieve user from database
    user = get_user_by_email_with_password(login_data.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Step 2: Verify password against stored hash
    if not verify_user_credentials(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Step 3: Check if user account is active
    if user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive. Please contact support.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Step 4: Generate access token (in production, use proper JWT)
    access_token = f"auth_token_{user['id'][:8]}_{user['email'].split('@')[0]}"
    
    # Step 5: Update last active timestamp
    update_last_active(user["id"])
    
    # Step 6: Prepare user profile response (exclude password hash)
    user_profile = UserProfileResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
        status=user["status"],
        created_at=user["created_at"],
        last_active_at=datetime.now()  # Updated timestamp
    )
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_profile,
        message=f"Welcome back, {user['name']}!"
    )

@router.get("/user/{email}")
def get_user_profile_by_email(email: str):
    """
    Retrieve user profile by email (without password hash for security)
    Useful for checking if user exists before login
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Query without password hash for security
        query = """
        SELECT 
            id, 
            name, 
            email, 
            role, 
            status,
            created_at,
            last_active_at
        FROM users 
        WHERE email = %s
        """
        
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role'],
            'status': user['status'],
            'created_at': user['created_at'],
            'last_active_at': user['last_active_at'],
            'exists': True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()

@router.get("/users/all")
def list_all_users():
    """
    List all users in the database (for admin/testing purposes)
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT 
            id, 
            name, 
            email, 
            role, 
            status,
            created_at,
            last_active_at
        FROM users 
        ORDER BY created_at DESC
        """
        
        cursor.execute(query)
        users = cursor.fetchall()
        cursor.close()
        
        return {
            'total_users': len(users),
            'users': [
                {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'role': user['role'],
                    'status': user['status'],
                    'created_at': user['created_at'],
                    'last_active_at': user['last_active_at']
                } for user in users
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        connection.close()
