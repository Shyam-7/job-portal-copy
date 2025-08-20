from sqlalchemy.orm import Session
from sqlalchemy import func, text, or_
from app.db.models.user.user_model import User
from app.db.models.job.job_model import Job
from app.db.models.job.application_model import Application
from datetime import datetime, timedelta

def get_dashboard_stats(db: Session):
    totalUsers = db.query(User).count()
    totalJobs = db.query(Job).count()
    activeJobs = db.query(Job).filter(Job.status == 'active').count()
    totalApplications = db.query(Application).count()
    pendingApplications = db.query(Application).filter(Application.status.in_(['submitted', 'under_review', 'pending', 'reviewing'])).count()
    scheduledInterviews = db.query(Application).filter(Application.status.in_(['interview', 'interview_scheduled', 'interviewing'])).count()

    return {
        "totalUsers": totalUsers,
        "totalJobs": totalJobs,
        "totalApplications": totalApplications,
        "pendingApplications": pendingApplications,
        "scheduledInterviews": scheduledInterviews,
        "activeJobs": activeJobs
    }

def get_recent_jobs(db: Session, limit: int = 5):
    return db.query(
        Job.id,
        Job.title,
        Job.company_name,
        Job.status,
        Job.created_at,
        func.count(Application.id).label('applicationCount')
    ).outerjoin(Application, Job.id == Application.job_id)\
    .group_by(Job.id, Job.title, Job.company_name, Job.status, Job.created_at)\
    .order_by(Job.created_at.desc())\
    .limit(limit)\
    .all()

def get_recent_activity(db: Session, limit: int = 5):
    recent_applications = db.query(Application).order_by(Application.created_at.desc()).limit(limit).all()
    recent_users = db.query(User).filter(User.role == 'job_seeker').order_by(User.created_at.desc()).limit(limit).all()
    recent_job_posts = db.query(Job).order_by(Job.created_at.desc()).limit(limit).all()

    all_activities = []
    for app in recent_applications:
        all_activities.append({
            "id": app.id,
            "type": "application",
            "message": f"{app.full_name} applied to {app.job.title}",
            "user_name": app.full_name,
            "user_initials": ''.join([n[0] for n in (app.full_name or 'U').split()]).upper(),
            "timestamp": app.created_at
        })
    for user in recent_users:
        all_activities.append({
            "id": user.id,
            "type": "user_registered",
            "message": f"{user.name} joined the platform",
            "user_name": user.name,
            "user_initials": ''.join([n[0] for n in (user.name or 'U').split()]).upper(),
            "timestamp": user.created_at
        })
    for job in recent_job_posts:
        all_activities.append({
            "id": job.id,
            "type": "job_posted",
            "message": f"New job posted: {job.title} at {job.company_name}",
            "user_name": job.poster.name if job.poster else "Admin",
            "user_initials": ''.join([n[0] for n in ((job.poster.name if job.poster else "A") or 'U').split()]).upper(),
            "timestamp": job.created_at
        })

    sorted_activities = sorted(all_activities, key=lambda x: x['timestamp'], reverse=True)
    return sorted_activities[:limit]

def get_job_categories(db: Session):
    return db.query(Job.category, func.count(Job.id).label('count')).group_by(Job.category).order_by(func.count(Job.id).desc()).all()

def get_application_status(db: Session):
    return db.query(Application.status, func.count(Application.id).label('count')).group_by(Application.status).order_by(func.count(Application.id).desc()).all()

def get_monthly_trends(db: Session, months: int = 6):
    trends = []
    today = datetime.utcnow()
    for i in range(months):
        month_start = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
        next_month_start = (month_start + timedelta(days=32)).replace(day=1)

        month_str = month_start.strftime('%Y-%m')

        users = db.query(User).filter(User.created_at >= month_start, User.created_at < next_month_start).count()
        jobs = db.query(Job).filter(Job.created_at >= month_start, Job.created_at < next_month_start).count()
        applications = db.query(Application).filter(Application.created_at >= month_start, Application.created_at < next_month_start).count()

        trends.append({
            "month": month_str,
            "users": users,
            "jobs": jobs,
            "applications": applications
        })
    return trends

def get_conversion_data(db: Session):
    total_applications = db.query(Application).count()
    total_interviews = db.query(Application).filter(Application.status.in_(['interview', 'interview_scheduled', 'interviewing'])).count()
    total_hires = db.query(Application).filter(Application.status == 'hired').count()

    # Mocking total visits for now
    total_visits = total_applications * 10

    return {
        "totalVisits": total_visits,
        "totalApplications": total_applications,
        "totalInterviews": total_interviews,
        "totalHires": total_hires,
        "visitToApplicationRate": total_applications / total_visits if total_visits > 0 else 0,
        "applicationToInterviewRate": total_interviews / total_applications if total_applications > 0 else 0,
        "interviewToHireRate": total_hires / total_interviews if total_interviews > 0 else 0
    }

def get_top_jobs(db: Session, limit: int = 10):
    return db.query(
        Job.id,
        Job.title,
        Job.company_name,
        func.count(Application.id).label('applications')
    ).join(Application, Job.id == Application.job_id)\
    .group_by(Job.id, Job.title, Job.company_name)\
    .order_by(func.count(Application.id).desc())\
    .limit(limit)\
    .all()

def get_user_activity(db: Session, days: int = 30):
    activity = []
    today = datetime.utcnow()
    for i in range(days):
        day = today - timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')

        registrations = db.query(User).filter(func.date(User.created_at) == day.date()).count()
        applications = db.query(Application).filter(func.date(Application.created_at) == day.date()).count()

        activity.append({
            "date": day_str,
            "registrations": registrations,
            "logins": 0, # Placeholder
            "applications": applications
        })
    return activity

def export_report(db: Session, type: str):
    return {"message": f"Exporting {type} report..."}

def refresh_data(db: Session):
    return {"message": "Refreshing data..."}
