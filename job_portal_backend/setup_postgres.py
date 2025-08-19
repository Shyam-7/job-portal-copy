#!/usr/bin/env python3
"""
PostgreSQL Database Setup Script for Job Portal
This script creates the database and tables for the job portal application.
"""

import psycopg2
from psycopg2 import sql
from config import settings
import sys

def create_database():
    """Create the job_portal database if it doesn't exist"""
    try:
        # Connect to default postgres database to create our database
        connection = psycopg2.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database='postgres',  # Connect to default database first
            port=settings.db_port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(settings.db_name)
            ))
            print(f"✅ Database '{settings.db_name}' created successfully!")
        else:
            print(f"✅ Database '{settings.db_name}' already exists!")
            
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all necessary tables"""
    try:
        connection = psycopg2.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
            port=settings.db_port
        )
        cursor = connection.cursor()
        
        # Enable UUID extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'job_seeker',
                status VARCHAR(50) DEFAULT 'active',
                last_active_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create jobs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                title VARCHAR(255) NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                location VARCHAR(255),
                employment_type VARCHAR(100),
                description TEXT,
                requirements TEXT,
                salary_min DECIMAL(10,2),
                salary_max DECIMAL(10,2),
                experience_level VARCHAR(100),
                skills_required TEXT,
                benefits TEXT,
                is_remote BOOLEAN DEFAULT FALSE,
                application_deadline TIMESTAMP,
                posted_by VARCHAR(36),
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (posted_by) REFERENCES users(id)
            );
        """)
        
        # Create applications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                job_id VARCHAR(36) NOT NULL,
                user_id VARCHAR(36) NOT NULL,
                cover_letter TEXT,
                resume_url VARCHAR(500),
                status VARCHAR(50) DEFAULT 'applied',
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES jobs(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(job_id, user_id)
            );
        """)
        
        # Create job_seeker_profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_seeker_profiles (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                user_id VARCHAR(36) NOT NULL,
                skills TEXT,
                experience TEXT,
                education TEXT,
                bio TEXT,
                cover_letter TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        
        # Create notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                user_id VARCHAR(36) NOT NULL,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT FALSE,
                notification_type VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        
        # Create announcements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                created_by VARCHAR(36),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users(id)
            );
        """)
        
        # Create content table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content (
                id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                content_type VARCHAR(100),
                status VARCHAR(50),
                tags JSON,
                view_count INTEGER DEFAULT 0,
                is_featured BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_applications_job ON applications(job_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main function to set up the database"""
    print("🚀 Setting up PostgreSQL database for Job Portal...")
    
    # Check database connection first
    try:
        connection = psycopg2.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database='postgres',
            port=settings.db_port
        )
        connection.close()
        print("✅ PostgreSQL connection successful!")
    except Exception as e:
        print(f"❌ Cannot connect to PostgreSQL: {e}")
        print("\nPlease ensure:")
        print("1. PostgreSQL is running")
        print("2. Database credentials in .env are correct")
        print("3. User has necessary permissions")
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 Database setup completed successfully!")
    print(f"Database: {settings.db_name}")
    print(f"Host: {settings.db_host}:{settings.db_port}")
    print(f"User: {settings.db_user}")

if __name__ == "__main__":
    main()
