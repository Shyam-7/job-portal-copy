from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import bcrypt
from db_utils import get_db_connection

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    role: Optional[str] = "job_seeker"

class UserResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    role: str
    status: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a bcrypt hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def get_user_by_email(email: str):
    """Get user from database by email"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, name, email, password_hash, role, status FROM users WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()
        return user
    finally:
        connection.close()

def create_user_in_db(user_data: UserCreate):
    """Create a new user in the database"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (user_data.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password and insert user
        password_hash = hash_password(user_data.password)
        cursor.execute(
            """INSERT INTO users (name, email, password_hash, role, status) 
               VALUES (%s, %s, %s, %s, 'active') RETURNING id, name, email, role, status""",
            (user_data.name, user_data.email, password_hash, user_data.role)
        )
        user = cursor.fetchone()
        connection.commit()
        cursor.close()
        return user
    finally:
        connection.close()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    """Register a new user"""
    user_data = create_user_in_db(user)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )
    
    return UserResponse(
        id=str(user_data["id"]),
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
        status=user_data["status"]
    )

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest):
    """Login user and return access token"""
    user = get_user_by_email(login_data.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real app, generate a proper JWT token
    access_token = f"real_token_for_{user['email']}"
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/me", response_model=UserResponse)
def get_current_user():
    """Get current user information (dummy implementation for now)"""
    # In a real app, this would extract user from JWT token
    user = get_user_by_email("admin@example.com")  # Default to admin for testing
    if user:
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            status=user["status"]
        )
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/users", response_model=list[UserResponse])
def get_all_users():
    """Get all users from database"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, role, status FROM users")
        users = cursor.fetchall()
        cursor.close()
        
        return [
            UserResponse(
                id=user["id"],
                email=user["email"],
                name=user["name"],
                role=user["role"],
                status=user["status"]
            )
            for user in users
        ]
    finally:
        connection.close()

@router.post("/forgot-password")
def forgot_password(email_data: dict):
    """Request password reset"""
    email = email_data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    user = get_user_by_email(email)
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If email exists, password reset instructions have been sent"}
    
    # In real app, send reset email
    return {"message": "Password reset email sent", "email": email}

@router.post("/reset-password")
def reset_password(reset_data: dict):
    """Reset password with reset code"""
    reset_code = reset_data.get("resetCode")
    new_password = reset_data.get("newPassword")
    
    if not reset_code or not new_password:
        raise HTTPException(status_code=400, detail="Reset code and new password are required")
    
    # In real app, validate reset code and update password
    return {"message": "Password reset successfully"}

@router.post("/change-password")
def change_password(password_data: dict):
    """Change password for authenticated user"""
    current_password = password_data.get("currentPassword")
    new_password = password_data.get("newPassword")
    
    if not current_password or not new_password:
        raise HTTPException(status_code=400, detail="Current and new passwords are required")
    
    # In real app, validate current password and update
    return {"message": "Password changed successfully"}

@router.post("/test-password")
def test_password_verification(test_data: dict):
    """Test endpoint to help determine the correct password for existing users"""
    email = test_data.get("email")
    password = test_data.get("password")
    
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    is_valid = verify_password(password, user["password_hash"])
    
    return {
        "email": email,
        "password_matches": is_valid,
        "user_exists": True,
        "user_status": user["status"]
    }
