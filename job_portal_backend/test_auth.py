#!/usr/bin/env python3
"""
User Authentication Test Script
This script demonstrates how to retrieve user credentials from PostgreSQL database for sign-in
"""

import sys
import os
sys.path.append('/Users/css/Documents/job-portal/job_portal_backend')

from db_utils import get_db_connection
import bcrypt

def get_user_credentials(email: str):
    """
    Retrieve user credentials from database for authentication
    Returns user data including hashed password for verification
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Query to get user with password hash for authentication
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
        WHERE email = %s AND status = 'active'
        """
        
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'password_hash': user['password_hash'],
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

def verify_user_password(plain_password: str, stored_hash: str) -> bool:
    """
    Verify if the provided password matches the stored hash
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def authenticate_user(email: str, password: str):
    """
    Complete user authentication process
    """
    print(f"🔍 Attempting to authenticate user: {email}")
    
    # Step 1: Retrieve user from database
    user = get_user_credentials(email)
    
    if not user:
        print("❌ User not found or inactive")
        return None
    
    print(f"✅ User found: {user['name']} ({user['role']})")
    
    # Step 2: Verify password
    if verify_user_password(password, user['password_hash']):
        print("✅ Password verified successfully")
        
        # Remove password hash from return data for security
        user_safe = {k: v for k, v in user.items() if k != 'password_hash'}
        return user_safe
    else:
        print("❌ Invalid password")
        return None

def list_all_users():
    """
    List all users in the database (for testing purposes)
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, role, status, created_at FROM users ORDER BY created_at")
        users = cursor.fetchall()
        
        print("\n📋 All users in database:")
        print("-" * 80)
        for user in users:
            print(f"ID: {user['id'][:8]}...")
            print(f"Name: {user['name']}")
            print(f"Email: {user['email']}")
            print(f"Role: {user['role']}")
            print(f"Status: {user['status']}")
            print(f"Created: {user['created_at']}")
            print("-" * 40)
            
        cursor.close()
        return users
    finally:
        connection.close()

if __name__ == "__main__":
    print("🚀 PostgreSQL User Authentication Test")
    print("=" * 50)
    
    # List all users first
    users = list_all_users()
    
    if users:
        print(f"\n📊 Found {len(users)} users in database")
        
        # Test authentication with existing users
        test_cases = [
            ("postgres_user@example.com", "securepass123"),
            ("test@example.com", "testpass123"),
            ("postgres_test@example.com", "testpass123"),
            ("nonexistent@example.com", "wrongpass"),  # Should fail
            ("postgres_user@example.com", "wrongpass")  # Should fail
        ]
        
        print("\n🧪 Testing Authentication:")
        print("=" * 50)
        
        for email, password in test_cases:
            print(f"\n🔐 Testing: {email}")
            result = authenticate_user(email, password)
            
            if result:
                print(f"✅ Login successful!")
                print(f"   User ID: {result['id']}")
                print(f"   Name: {result['name']}")
                print(f"   Role: {result['role']}")
            else:
                print(f"❌ Login failed!")
            print("-" * 30)
    else:
        print("❌ No users found in database")
