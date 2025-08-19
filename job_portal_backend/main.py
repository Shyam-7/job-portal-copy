from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from config import settings
import psycopg2
from psycopg2 import Error
from content_routes import router as content_router
from user_routes import router as user_router
from job_routes import router as job_router
from application_routes import router as application_router
from communication_routes import router as communication_router
from admin_routes import router as admin_router
from enhanced_auth_routes import router as auth_router

app = FastAPI(
    title="Job Portal API",
    description="This is the API for the Job Portal application with all microservices.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(content_router)
app.include_router(user_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(communication_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Portal API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/test")
def test_endpoint():
    return {"message": "Test endpoint working", "status": "success"}

@app.get("/api/db-test")
def test_database_connection():
    try:
        # Test database connection
        connection = psycopg2.connect(
            host=settings.db_host,
            user=settings.db_user,
            password=settings.db_password,
            database=settings.db_name,
            port=settings.db_port
        )
        
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            cursor.execute("SELECT current_database();")
            database_name = cursor.fetchone()
            cursor.close()
            connection.close()
            
            return {
                "status": "success",
                "message": "Database connection successful",
                "postgresql_version": db_version[0] if db_version else "Unknown",
                "connected_database": database_name[0] if database_name else "None",
                "connection_details": {
                    "host": settings.db_host,
                    "port": settings.db_port,
                    "user": settings.db_user,
                    "database": settings.db_name
                }
            }
    except Error as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "connection_details": {
                "host": settings.db_host,
                "port": settings.db_port,
                "user": settings.db_user,
                "database": settings.db_name
            }
        }
