from fastapi import APIRouter, HTTPException
from db_utils import get_db_connection

router = APIRouter(prefix="/api/content", tags=["Content"])

@router.get("/public/user-dashboard")
def get_user_dashboard_content():
    """
    Get dashboard content for the user homepage
    This endpoint provides content for the main dashboard
    """
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Get hero content from content table
        cursor.execute("""
            SELECT title, content 
            FROM content 
            WHERE content_type = 'hero' AND status = 'active' 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        hero_data = cursor.fetchone()
        
        # Get platform statistics
        cursor.execute("SELECT COUNT(*) as total_jobs FROM jobs WHERE status = 'active'")
        total_jobs = cursor.fetchone()["total_jobs"]
        
        cursor.execute("SELECT COUNT(DISTINCT company_name) as total_companies FROM jobs WHERE status = 'active'")
        total_companies = cursor.fetchone()["total_companies"]
        
        cursor.execute("SELECT COUNT(*) as total_users FROM users WHERE status = 'active'")
        total_users = cursor.fetchone()["total_users"]
        
        cursor.execute("SELECT COUNT(*) as total_applications FROM applications")
        total_applications = cursor.fetchone()["total_applications"]
        
        # Get job categories with counts
        cursor.execute("""
            SELECT 
                skills_required,
                COUNT(*) as job_count
            FROM jobs 
            WHERE status = 'active' AND skills_required IS NOT NULL
            GROUP BY skills_required
            ORDER BY job_count DESC
            LIMIT 4
        """)
        categories_data = cursor.fetchall()
        
        # Get recent jobs
        cursor.execute("""
            SELECT 
                id, title, company_name, location, employment_type,
                salary_min, salary_max, experience_level, created_at
            FROM jobs 
            WHERE status = 'active'
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_jobs_data = cursor.fetchall()
        
        # Get recent announcements
        cursor.execute("""
            SELECT id, title, content, created_at 
            FROM announcements 
            ORDER BY created_at DESC 
            LIMIT 3
        """)
        announcements_data = cursor.fetchall()
        
        cursor.close()
        
        # Build hero section
        hero = {
            "title": hero_data["title"] if hero_data else "Find Your Dream Job",
            "subtitle": hero_data["content"] if hero_data else "Connect with top employers and discover opportunities that match your skills",
            "cta_text": "Start Your Job Search",
            "background_image": "/assets/images/hero-bg.jpg"
        }
        
        # Build stats section
        stats = {
            "total_jobs": total_jobs,
            "active_employers": total_companies,
            "successful_placements": total_applications,
            "active_users": total_users
        }
        
        # Build categories section
        featured_categories = []
        category_icons = ["💻", "🏥", "💰", "🎓", "🔬", "🎨"]
        for i, category in enumerate(categories_data):
            featured_categories.append({
                "id": i + 1,
                "name": category["skills_required"][:20] + "..." if len(category["skills_required"]) > 20 else category["skills_required"],
                "icon": category_icons[i % len(category_icons)],
                "job_count": category["job_count"],
                "description": f"Jobs requiring {category['skills_required']}"
            })
        
        # Build recent jobs section
        recent_jobs = []
        for job in recent_jobs_data:
            salary_range = "Not specified"
            if job["salary_min"] and job["salary_max"]:
                salary_range = f"${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
            elif job["salary_min"]:
                salary_range = f"From ${job['salary_min']:,.0f}"
            
            recent_jobs.append({
                "id": job["id"],
                "title": job["title"],
                "company": job["company_name"],
                "location": job["location"] or "Not specified",
                "salary_range": salary_range,
                "posted_date": job["created_at"].strftime("%Y-%m-%d") if job["created_at"] else None,
                "job_type": job["employment_type"] or "Not specified",
                "experience_level": job["experience_level"] or "Any level"
            })
        
        # Build announcements section
        announcements = []
        for announcement in announcements_data:
            announcements.append({
                "id": announcement["id"],
                "title": announcement["title"],
                "content": announcement["content"],
                "type": "info",
                "created_at": announcement["created_at"].isoformat() if announcement["created_at"] else None
            })
        
        dashboard_content = {
            "hero": hero,
            "stats": stats,
            "featured_categories": featured_categories,
            "recent_jobs": recent_jobs,
            "announcements": announcements
        }
        
        return dashboard_content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard content: {str(e)}")
    finally:
        connection.close()

@router.get("/public/about")
def get_about_content():
    """Get about page content"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT title, content 
            FROM content 
            WHERE content_type = 'about' AND status = 'active'
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        about_data = cursor.fetchone()
        cursor.close()
        
        if about_data:
            return {
                "title": about_data["title"],
                "content": about_data["content"]
            }
        else:
            raise HTTPException(status_code=404, detail="About content not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching about content: {str(e)}")
    finally:
        connection.close()

@router.get("/public/features")
def get_features_content():
    """Get platform features"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT title, content 
            FROM content 
            WHERE content_type = 'feature' AND status = 'active'
            ORDER BY created_at ASC
        """)
        features_data = cursor.fetchall()
        cursor.close()
        
        features = []
        feature_icons = ["🎯", "🔔", "📊", "👤", "⚡", "🔒", "📈", "🤝"]
        
        for i, feature in enumerate(features_data):
            features.append({
                "title": feature["title"],
                "description": feature["content"],
                "icon": feature_icons[i % len(feature_icons)]
            })
        
        return {"features": features}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching features: {str(e)}")
    finally:
        connection.close()

@router.get("/announcements")
def get_announcements():
    """Get system announcements"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, title, content, created_at, created_by
            FROM announcements 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        announcements = cursor.fetchall()
        cursor.close()
        
        return {
            "announcements": [
                {
                    "id": ann["id"],
                    "title": ann["title"],
                    "content": ann["content"],
                    "created_at": ann["created_at"].isoformat() if ann["created_at"] else None,
                    "created_by": ann["created_by"]
                } for ann in announcements
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching announcements: {str(e)}")
    finally:
        connection.close()

@router.get("/public/stats")
def get_platform_stats():
    """Get platform statistics"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        
        # Get actual stats from database
        cursor.execute("SELECT COUNT(*) as user_count FROM users WHERE status = 'active'")
        user_count = cursor.fetchone()["user_count"]
        
        cursor.execute("SELECT COUNT(*) as job_count FROM jobs WHERE status = 'active'")
        job_count = cursor.fetchone()["job_count"]
        
        cursor.execute("SELECT COUNT(*) as application_count FROM applications")
        application_count = cursor.fetchone()["application_count"]
        
        cursor.execute("SELECT COUNT(DISTINCT company_name) as company_count FROM jobs WHERE status = 'active'")
        company_count = cursor.fetchone()["company_count"]
        
        # Calculate success rate based on applications
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'accepted' THEN 1 END) as accepted,
                COUNT(*) as total
            FROM applications
        """)
        success_data = cursor.fetchone()
        success_rate = 0
        if success_data and success_data["total"] > 0:
            success_rate = (success_data["accepted"] / success_data["total"]) * 100
        
        cursor.close()
        
        return {
            "total_users": user_count,
            "active_jobs": job_count,
            "total_applications": application_count,
            "success_rate": f"{success_rate:.1f}%",
            "companies": company_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching platform stats: {str(e)}")
    finally:
        connection.close()

@router.post("/content")
def create_content(content_data: dict):
    """Create new content (admin only)"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO content (title, content, content_type, status, is_featured)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, title, content_type, created_at
        """, (
            content_data.get("title"),
            content_data.get("content"),
            content_data.get("content_type", "general"),
            content_data.get("status", "active"),
            content_data.get("is_featured", False)
        ))
        
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        
        return {
            "id": result["id"],
            "title": result["title"],
            "content_type": result["content_type"],
            "created_at": result["created_at"],
            "message": "Content created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating content: {str(e)}")
    finally:
        connection.close()
