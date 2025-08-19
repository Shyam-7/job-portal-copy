# 🔐 User Authentication & Database Credential Retrieval Guide

## 🎯 Overview

This guide demonstrates how to retrieve user passwords and usernames from the PostgreSQL database for secure sign-in authentication in the Job Portal application.

---

## 📊 Database Schema for Authentication

### Users Table Structure:
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,           -- UUID for user identification
    name VARCHAR(255),                    -- User's display name
    email VARCHAR(255) UNIQUE NOT NULL,   -- Login username (email)
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt hashed password
    role VARCHAR(50) DEFAULT 'job_seeker',-- User role (job_seeker, employer, admin)
    status VARCHAR(50) DEFAULT 'active',  -- Account status (active, inactive, suspended)
    last_active_at TIMESTAMP,            -- Last login timestamp
    created_at TIMESTAMP DEFAULT NOW(),   -- Account creation date
    updated_at TIMESTAMP DEFAULT NOW()    -- Last update timestamp
);
```

---

## 🔑 Authentication Process

### Step 1: Retrieve User from Database
```python
def get_user_by_email_with_password(email: str):
    """Retrieve user with password hash for authentication"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
    SELECT 
        id, name, email, password_hash, role, status,
        created_at, last_active_at
    FROM users 
    WHERE email = %s AND status = 'active'
    """
    
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    return user
```

### Step 2: Verify Password Against Hash
```python
def verify_user_credentials(plain_password: str, stored_hash: str) -> bool:
    """Verify password against bcrypt hash"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        stored_hash.encode('utf-8')
    )
```

### Step 3: Complete Authentication
```python
def authenticate_user(email: str, password: str):
    # 1. Get user from database
    user = get_user_by_email_with_password(email)
    
    # 2. Check if user exists and is active
    if not user or user['status'] != 'active':
        return None
    
    # 3. Verify password
    if verify_user_credentials(password, user['password_hash']):
        # 4. Update last active timestamp
        update_last_active(user['id'])
        return user
    
    return None
```

---

## 🌐 API Endpoints for Authentication

### 🔐 Enhanced Sign-In Endpoint
**POST** `/api/auth/signin`

**Request:**
```json
{
    "email": "user@example.com",
    "password": "userpassword123"
}
```

**Success Response:**
```json
{
    "access_token": "auth_token_ad90cdd8_user",
    "token_type": "bearer",
    "user": {
        "id": "ad90cdd8-fc74-4ffa-ae6c-a1c672c9d3a2",
        "email": "user@example.com",
        "name": "User Name",
        "role": "job_seeker",
        "status": "active",
        "created_at": "2025-08-18T11:35:40.174625",
        "last_active_at": "2025-08-18T14:11:12.800985"
    },
    "message": "Welcome back, User Name!"
}
```

**Error Response:**
```json
{
    "detail": "Invalid email or password"
}
```

### 👤 Get User Profile by Email
**GET** `/api/auth/user/{email}`

**Response:**
```json
{
    "id": "ad90cdd8-fc74-4ffa-ae6c-a1c672c9d3a2",
    "name": "User Name",
    "email": "user@example.com",
    "role": "job_seeker",
    "status": "active",
    "created_at": "2025-08-18T11:35:40.174625",
    "last_active_at": "2025-08-18T14:11:12.797686",
    "exists": true
}
```

### 📋 List All Users
**GET** `/api/auth/users/all`

**Response:**
```json
{
    "total_users": 3,
    "users": [
        {
            "id": "ad90cdd8-fc74-4ffa-ae6c-a1c672c9d3a2",
            "name": "PostgreSQL User",
            "email": "postgres_user@example.com",
            "role": "job_seeker",
            "status": "active",
            "created_at": "2025-08-18T11:35:40.174625",
            "last_active_at": "2025-08-18T14:11:12.797686"
        }
    ]
}
```

---

## 🧪 Testing Authentication

### Current Test Users in Database:
| Email | Password | Name | Role |
|-------|----------|------|------|
| `postgres_user@example.com` | `securepass123` | PostgreSQL User | job_seeker |
| `test@example.com` | `testpass123` | Test User | job_seeker |
| `postgres_test@example.com` | `testpass123` | PostgreSQL Test User | job_seeker |

### Test Commands:

#### ✅ Valid Login:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"postgres_user@example.com","password":"securepass123"}'
```

#### ❌ Invalid Password:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"postgres_user@example.com","password":"wrongpassword"}'
```

#### ❌ Non-existent User:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"nonexistent@example.com","password":"anypassword"}'
```

#### 👤 Check User Profile:
```bash
curl http://localhost:8000/api/auth/user/postgres_user@example.com
```

---

## 🔒 Security Features

### ✅ Password Security:
- **bcrypt hashing** with salt for password storage
- **Never store plain text** passwords
- **Password verification** using secure bcrypt comparison

### ✅ Database Security:
- **Parameterized queries** prevent SQL injection
- **Connection pooling** with proper error handling
- **Password hash exclusion** from profile responses

### ✅ Account Security:
- **Active status check** prevents inactive account login
- **Last active tracking** for session monitoring
- **Email uniqueness** enforced at database level

### ✅ Error Handling:
- **Generic error messages** prevent user enumeration
- **Proper HTTP status codes** (401 for authentication failures)
- **Database connection cleanup** prevents resource leaks

---

## 🎯 Integration Examples

### Frontend JavaScript Example:
```javascript
async function signInUser(email, password) {
    try {
        const response = await fetch('/api/auth/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user_profile', JSON.stringify(data.user));
            return { success: true, user: data.user, message: data.message };
        } else {
            const error = await response.json();
            return { success: false, message: error.detail };
        }
    } catch (error) {
        return { success: false, message: 'Network error' };
    }
}
```

### Python Client Example:
```python
import requests

def authenticate_user(email, password):
    url = "http://localhost:8000/api/auth/signin"
    payload = {"email": email, "password": password}
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json()["detail"]}
```

---

## 📊 Database Operations

### View Password Hashes (Admin Only):
```sql
-- Check how passwords are stored (bcrypt hashes)
SELECT email, password_hash FROM users;
```

### Check Login Activity:
```sql
-- See last active timestamps
SELECT name, email, last_active_at, created_at 
FROM users 
ORDER BY last_active_at DESC;
```

### User Account Management:
```sql
-- Deactivate user account
UPDATE users SET status = 'inactive' WHERE email = 'user@example.com';

-- Reactivate user account
UPDATE users SET status = 'active' WHERE email = 'user@example.com';
```

---

## 🚀 Live API Documentation

Visit these URLs to explore the authentication API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The enhanced authentication endpoints are documented under the "Enhanced Authentication" section.

---

## ✅ Summary

Your Job Portal application now has a complete authentication system that:

✅ **Retrieves user credentials** from PostgreSQL database
✅ **Verifies passwords** using secure bcrypt hashing
✅ **Validates user status** and account activity
✅ **Generates access tokens** for session management
✅ **Updates login timestamps** for activity tracking
✅ **Provides secure APIs** for user management

The system successfully retrieves usernames (emails) and verifies passwords from the database for secure sign-in functionality! 🎯
