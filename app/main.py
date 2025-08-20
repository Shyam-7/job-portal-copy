from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.common.auth_routes import router as auth_router
from app.api.user.routes.user_routes import router as user_router
from app.api.user.routes.saved_job_routes import router as saved_job_router
from app.api.job.routes.job_routes import router as job_router
from app.api.shared.application_routes import router as application_router
from app.api.admin.routes.content_routes import router as content_router
from app.api.shared.communication_routes import router as communication_router
from app.api.admin.routes.admin_dashboard_routes import router as admin_dashboard_router
from app.api.admin.routes.analytics_routes import router as analytics_router

app = FastAPI(
    title="Job Portal API",
    description="This is the API for the Job Portal application, migrated from Node.js to FastAPI.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(saved_job_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(content_router)
app.include_router(communication_router)
app.include_router(admin_dashboard_router)
app.include_router(analytics_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Portal API"}

import psycopg2
from psycopg2 import Error
from .config import settings

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/db-test")
def test_database_connection():
    try:
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
            cursor.close()
            connection.close()

            return {
                "status": "success",
                "message": "Database connection successful",
                "postgresql_version": db_version[0] if db_version else "Unknown"
            }
    except Error as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }
