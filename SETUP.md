# Project Setup Guide

This document provides step-by-step instructions on how to set up and run this project on your local machine.

## Prerequisites

- **Node.js and npm:** Required for the frontend application. You can download it from [https://nodejs.org/](https://nodejs.org/).
- **Python:** The backend is built with Python. This project uses Python 3.12. You can download it from [https://www.python.org/](https://www.python.org/).
- **PostgreSQL:** The application uses a PostgreSQL database. You can download it from [https://www.postgresql.org/](https://www.postgresql.org/).

## Backend Setup

1.  **Install Dependencies:**
    Navigate to the root of the project and install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up Environment Variables:**
    Create a `.env` file in the root of the project by copying the `.env.example` file (if it exists) or by creating a new file. The `.env` file should contain the following variables:
    ```
    DB_HOST=localhost
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=job_portal
    DB_PORT=5432
    JWT_SECRET=a-very-secret-key
    ```
    Replace `your_db_user` and `your_db_password` with your PostgreSQL credentials. The `JWT_SECRET` can be any long, random string.

3.  **Set up the Database:**
    - Make sure you have a PostgreSQL server running.
    - Create a new database named `job_portal`.
    - Run the database migrations to create the necessary tables:
      ```bash
      alembic upgrade head
      ```
      *Note: Alembic is not yet configured in this project. This step is a placeholder for future implementation.*

4.  **Run the Backend Server:**
    From the root of the project, run the following command:
    ```bash
    uvicorn app.main:app --reload
    ```
    The backend will be running at `http://localhost:8000`.

## Frontend Setup

1.  **Install Dependencies:**
    Navigate to the `job_portal_frontend` directory and install the Node.js dependencies:
    ```bash
    cd job_portal_frontend
    npm install
    ```

2.  **Run the Frontend Server:**
    ```bash
    npm start
    ```
    The frontend will be running at `http://localhost:4200`.

## Running the Tests

To run the backend tests, use the following command from the root of the project:
```bash
pytest app/tests/
```
The tests use a separate in-memory SQLite database, so they will not affect your PostgreSQL database.

## Project Structure

This section provides an overview of the backend project structure.

### `app/main.py`

This is the main entry point of the FastAPI application. It is responsible for:
- Initializing the FastAPI app.
- Configuring CORS middleware to allow requests from the frontend.
- Including all the API routers from the different modules.
- Defining the root (`/`) and health check (`/health`) endpoints.

### `app/api/common/auth_routes.py`

This file defines the endpoints for user authentication:
- `POST /api/auth/register`: Creates a new user.
- `POST /api/auth/login`: Authenticates a user and returns a JWT access token.

### `app/api/user/routes/user_routes.py`

This file defines the endpoints for user management and user profiles:
- `GET /api/users/profile`: Gets the profile of the currently logged-in user.
- `PATCH /api/users/profile`: Updates the profile of the currently logged-in user.
- `POST /api/users/profile/resume`: Uploads a resume for the currently logged-in user.
- `GET /api/users/`: Gets a list of all users (admin only).
- `GET /api/users/{user_id}`: Gets a user by their ID (admin only).
- `DELETE /api/users/{user_id}`: Deletes a user (admin only).
- `PATCH /api/users/{user_id}/status`: Updates a user's status (admin only).

### `app/api/job/routes/job_routes.py`

This file defines the endpoints for job management:
- `GET /api/jobs/`: Gets a list of all active jobs, with support for filtering and sorting.
- `GET /api/jobs/admin/all`: Gets a list of all jobs, including inactive ones (admin only).
- `GET /api/jobs/{job_id}`: Gets a job by its ID.
- `POST /api/jobs/`: Creates a new job (admin only).
- `PUT /api/jobs/{job_id}`: Updates a job (admin only).
- `DELETE /api/jobs/{job_id}`: Deletes a job (admin only).

### `app/api/shared/application_routes.py`

This file defines the endpoints for application management:
- `POST /api/applications/`: Creates a new application for a job.
- `GET /api/applications/me`: Gets a list of all applications for the currently logged-in user.
- `GET /api/applications/user/{user_id}`: Gets a list of all applications for a specific user (admin only).
- `GET /api/applications/job/{job_id}`: Gets a list of all applications for a specific job (admin only).
- `GET /api/applications/{application_id}`: Gets an application by its ID.
- `PUT /api/applications/{application_id}`: Updates an application.
- `PATCH /api/applications/{application_id}`: Partially updates an application.
- `DELETE /api/applications/{application_id}`: Deletes an application.

### `app/api/shared/communication_routes.py`

This file defines the endpoints for communication features:
- **Messages:**
  - `GET /api/communication/{application_id}/messages`: Gets all messages for a specific application.
  - `POST /api/communication/messages`: Creates a new message.
- **Announcements (Admin):**
  - `GET /api/communication/announcements/stats`: Gets statistics about announcements.
  - `GET /api/communication/announcements`: Gets a list of all announcements.
  - `GET /api/communication/announcements/scheduled`: Gets a list of scheduled announcements.
  - `GET /api/communication/announcements/drafts`: Gets a list of draft announcements.
  - `POST /api/communication/announcements`: Creates a new announcement.
  - `PUT /api/communication/announcements/{announcement_id}`: Updates an announcement.
  - `DELETE /api/communication/announcements/{announcement_id}/cancel`: Cancels a scheduled announcement.
- **Notifications (User):**
  - `GET /api/communication/notifications`: Gets a list of all notifications for the currently logged-in user.
  - `PUT /api/communication/notifications/{notification_id}/read`: Marks a notification as read.
  - `PUT /api/communication/notifications/read-all`: Marks all notifications as read.
  - `POST /api/communication/notifications/send`: Sends a custom notification to a user (admin only).
- **Notification Preferences (User):**
  - `GET /api/communication/preferences`: Gets the notification preferences for the currently logged-in user.
  - `PUT /api/communication/preferences`: Updates the notification preferences for the currently logged-in user.

### `app/api/admin/routes/content_routes.py`

This file defines the endpoints for content management:
- **Public Routes:**
  - `GET /api/content/public/user-dashboard`: Gets the content for the user dashboard.
  - `GET /api/content/public/section/{section}`: Gets content for a specific section.
  - `GET /api/content/public/section-type/{section_type}`: Gets content by section type.
- **Admin Routes:**
  - `GET /api/content/admin`: Gets all site content.
  - `POST /api/content/admin`: Creates new site content.
  - `PUT /api/content/admin/{content_id}`: Updates site content.
  - `DELETE /api/content/admin/{content_id}`: Deletes site content.

### `app/api/admin/routes/admin_dashboard_routes.py`

This file defines the endpoints for the admin dashboard:
- `GET /api/admin/dashboard/stats`: Gets statistics for the admin dashboard.
- `GET /api/admin/dashboard/recent-jobs`: Gets a list of recent jobs.
- `GET /api/admin/dashboard/recent-activity`: Gets a list of recent activity.

### `app/api/admin/services/admin_dashboard_service.py`

This file provides the business logic for the admin dashboard:
- `get_dashboard_stats`: Calculates and returns key statistics for the dashboard.
- `get_recent_jobs`: Gets a list of the most recently posted jobs.
- `get_recent_activity`: Gets a list of recent activities on the platform (new users, new applications, etc.).

### `app/api/admin/routes/analytics_routes.py`

This file defines the endpoints for the analytics page:
- `GET /api/analytics/overview`: Gets an overview of the analytics data.
- `GET /api/analytics/recent-activity`: Gets a list of recent activity.
- `GET /api/analytics/job-categories`: Gets the distribution of jobs by category.
- `GET /api/analytics/application-status`: Gets the distribution of applications by status.

### `app/api/admin/services/analytics_service.py`

This file provides the business logic for the analytics page:
- `get_dashboard_stats`: Calculates and returns key statistics for the dashboard.
- `get_recent_activity`: Gets a list of recent activities on the platform.
- `get_job_categories`: Gets the distribution of jobs by category.
- `get_application_status`: Gets the distribution of applications by status.
