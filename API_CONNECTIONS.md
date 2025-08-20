# API Connection Map

This document maps the frontend features to the backend API endpoints that power them.

## Authentication

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| User Signup | `auth.service.ts: signup()` | `POST /api/auth/register` | `auth_routes.py: register()` |
| User Login | `auth.service.ts: login()` | `POST /api/auth/login` | `auth_routes.py: login()` |
| Forgot Password | `auth.service.ts: requestPasswordReset()` | `POST /api/auth/forgot-password` | `auth_routes.py: request_password_reset()` |
| Reset Password | `auth.service.ts: resetPassword()` | `POST /api/auth/reset-password` | `auth_routes.py: reset_user_password()` |
| Change Password | `auth.service.ts: changePassword()` | `POST /api/auth/change-password` | `auth_routes.py: change_user_password()` |

## User Profile

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| Get User Profile | `user.service.ts: getUserProfile()` | `GET /api/users/profile` | `user_routes.py: read_users_me()` |
| Update User Profile | `user.service.ts: updateUserProfile()` | `PATCH /api/users/profile` | `user_routes.py: update_user_me()` |
| Upload Resume | (handled in component) | `POST /api/users/profile/resume` | `user_routes.py: upload_resume()` |

## Job Management

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| Get All Jobs | `job.service.ts: getJobs()` | `GET /api/jobs/` | `job_routes.py: read_all_active_jobs()` |
| Get Jobs with Filters | `job.service.ts: getJobsWithFilters()` | `GET /api/jobs/` | `job_routes.py: read_all_active_jobs()` |
| Get Job by ID | `job.service.ts: getJobById()` | `GET /api/jobs/{job_id}` | `job_routes.py: read_job_by_id()` |
| Create Job (Admin) | `job.service.ts: addJob()` | `POST /api/jobs/` | `job_routes.py: create_new_job()` |
| Update Job (Admin) | `job.service.ts: updateJob()` | `PUT /api/jobs/{job_id}` | `job_routes.py: update_existing_job()` |
| Delete Job (Admin) | `job.service.ts: deleteJob()` | `DELETE /api/jobs/{job_id}` | `job_routes.py: remove_job()` |

## Application Management

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| Apply for Job | `application.service.ts: applyToJob()` | `POST /api/applications/` | `application_routes.py: apply_for_job()` |
| Get My Applications | `application.service.ts: getUserApplications()` | `GET /api/applications/me` | `application_routes.py: read_my_applications()` |
| Get User Applications (Admin) | `job.service.ts: getUserApplications()` | `GET /api/applications/user/{user_id}` | `application_routes.py: read_applications_for_user()` |
| Update Application (Admin) | `job.service.ts: updateApplication()` | `PUT /api/applications/{application_id}` | `application_routes.py: update_application_status()` |
| Withdraw Application | `job.service.ts: withdrawApplication()` | `DELETE /api/applications/{application_id}` | `application_routes.py: withdraw_job_application()` |

## Communication

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| Get Messages | (not in a service) | `GET /api/communication/{application_id}/messages` | `communication_routes.py: read_messages_for_application()` |
| Send Message | (not in a service) | `POST /api/communication/messages` | `communication_routes.py: create_new_message()` |
| Get Announcements (Admin) | `communication.service.ts: getAnnouncements()` | `GET /api/communication/announcements` | `communication_routes.py: read_announcements()` |
| ... | ... | ... | ... |

## Admin

| Frontend Feature | Frontend Service Method | Backend Endpoint | Backend Route Function |
| --- | --- | --- | --- |
| Get Dashboard Stats | `admin-dashboard.service.ts: getDashboardStats()` | `GET /api/admin/dashboard/stats` | `admin_dashboard_routes.py: read_dashboard_stats()` |
| Get Recent Jobs | `admin-dashboard.service.ts: getRecentJobs()` | `GET /api/admin/dashboard/recent-jobs` | `admin_dashboard_routes.py: read_recent_jobs()` |
| Get Recent Activity | `admin-dashboard.service.ts: getRecentActivity()` | `GET /api/admin/dashboard/recent-activity` | `admin_dashboard_routes.py: read_recent_activity()` |
| Get Analytics Overview | `analytics.service.ts: getAnalyticsOverview()` | `GET /api/analytics/overview` | `analytics_routes.py: read_analytics_overview()` |
| ... | ... | ... | ... |
