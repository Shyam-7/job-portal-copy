<p align="center">
  <h1 align="center">🏢 Job Portal</h1>
  <p align="center">
    A full-stack job portal application with role-based access for <strong>Job Seekers</strong>, <strong>Employers</strong>, and <strong>Admins</strong>.
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Angular-19-dd0031?logo=angular&logoColor=white" alt="Angular 19" />
    <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/PostgreSQL-14+-4169e1?logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/TailwindCSS-4-06b6d4?logo=tailwindcss&logoColor=white" alt="TailwindCSS" />
    <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  </p>
</p>

---

## 📌 Overview

**Job Portal** is a production-ready web application that connects job seekers with employers. It features a modern Angular frontend, a Python FastAPI backend with a microservices-style architecture, and a PostgreSQL database — all tied together with JWT authentication and role-based permissions.

> **🔗 Repository:** [github.com/Shyam-7/job-portal-copy](https://github.com/Shyam-7/job-portal-copy)

---

## ✨ Key Features

| Module | Highlights |
|--------|-----------|
| **🔐 Authentication** | JWT-based signup/signin, password hashing (bcrypt), role-based access control |
| **🔍 Job Search** | Browse, search & filter jobs by keyword, location, employment type |
| **📄 Applications** | Apply to jobs, track application status, view application history |
| **👤 User Profiles** | Manage profile, view dashboard analytics, save jobs |
| **📊 Admin Dashboard** | Manage users, jobs, content; view platform analytics |
| **📢 Notifications** | In-app announcements, notification preferences, communication system |
| **📝 CMS** | Admin-managed content for homepage banners, featured jobs, etc. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Angular 19, TypeScript, TailwindCSS 4, Chart.js, Font Awesome |
| **Backend** | Python, FastAPI, Pydantic, SQLAlchemy, Alembic |
| **Database** | PostgreSQL 14+ |
| **Auth** | JWT (python-jose), Passlib + bcrypt |
| **Email** | FastAPI-Mail |
| **Dev Tools** | Karma/Jasmine (testing), Angular SSR |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Angular 19 Frontend                     │
│         (Components · Services · Guards · Interceptors)     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend (Python)                  │
│                                                             │
│  ┌──────────┐ ┌────────┐ ┌──────┐ ┌──────────────────────┐  │
│  │   Auth   │ │  Jobs  │ │ User │ │  Admin / Analytics   │  │
│  │  Service │ │ Service│ │Serv. │ │      Service         │  │
│  └──────────┘ └────────┘ └──────┘ └──────────────────────┘  │
│  ┌──────────────────┐  ┌─────────────────────────────────┐  │
│  │  Applications    │  │  Communication / Notifications  │  │
│  │     Service      │  │           Service               │  │
│  └──────────────────┘  └─────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLAlchemy ORM
┌──────────────────────────▼──────────────────────────────────┐
│                    PostgreSQL Database                       │
│        (Users · Jobs · Applications · Content · Comms)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
job-portal/
├── job_portal_backend/          # FastAPI backend
│   ├── main.py                  # App entry point & router registration
│   ├── config.py                # Environment configuration (Pydantic)
│   ├── enhanced_auth_routes.py  # Authentication endpoints
│   ├── job_routes.py            # Job CRUD endpoints
│   ├── application_routes.py    # Job application endpoints
│   ├── user_routes.py           # User profile endpoints
│   ├── admin_routes.py          # Admin management endpoints
│   ├── content_routes.py        # CMS content endpoints
│   ├── communication_routes.py  # Notifications & announcements
│   ├── db_utils.py              # Database connection utilities
│   ├── run.py                   # Server runner
│   ├── api/                     # Structured API modules
│   ├── core/                    # Auth, security, permissions
│   ├── db/                      # Models, schemas, database layer
│   ├── services/                # Business logic layer
│   ├── tasks/                   # Background tasks
│   ├── utils/                   # Utility helpers
│   └── tests/                   # Unit & integration tests
│
├── job_portal_frontend/         # Angular 19 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── core/            # Auth guards, services, models
│   │   │   ├── modules/
│   │   │   │   ├── admin/       # Dashboard, analytics, content mgmt
│   │   │   │   ├── auth/        # Login, signup, password reset
│   │   │   │   └── user/        # Job search, applications, profile
│   │   │   ├── shared/          # Reusable components & layouts
│   │   │   └── app.routes.ts    # Application routing
│   │   └── assets/              # Static assets
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── requirements.txt             # Python backend dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** ≥ 18 & **npm** ≥ 9
- **Python** ≥ 3.10
- **PostgreSQL** ≥ 14

### 1. Clone the Repository

```bash
git clone https://github.com/Shyam-7/job-portal-copy.git
cd job-portal-copy
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp job_portal_backend/.env.example job_portal_backend/.env
# Edit .env with your PostgreSQL credentials:
#   DB_HOST=localhost
#   DB_USER=your_user
#   DB_PASSWORD=your_password
#   DB_NAME=job_portal
#   DB_PORT=5432
#   JWT_SECRET=your_secret_key

# Start the backend
cd job_portal_backend
uvicorn main:app --reload --port 8000
```

> 📖 **API Docs** available at [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

### 3. Frontend Setup

```bash
cd job_portal_frontend

# Install dependencies
npm install

# Start the dev server
npm start
```

> 🌐 **Frontend** available at [http://localhost:4200](http://localhost:4200)

---

## 🔌 API Endpoints

| Service | Endpoint | Description |
|---------|----------|-------------|
| **Auth** | `POST /api/auth/signin` | User login |
| **Auth** | `POST /api/auth/signup` | User registration |
| **Auth** | `GET /api/auth/users/all` | List all users (admin) |
| **Jobs** | `GET /api/jobs/` | List all jobs |
| **Jobs** | `GET /api/jobs/search?q=keyword` | Search jobs |
| **Jobs** | `POST /api/jobs/` | Create a job (admin) |
| **Jobs** | `PUT /api/jobs/{id}` | Update a job (admin) |
| **Jobs** | `DELETE /api/jobs/{id}` | Delete a job (admin) |
| **Applications** | `POST /api/applications/` | Apply for a job |
| **Applications** | `GET /api/applications/` | List user applications |
| **Users** | `GET /api/user/profile` | Get user profile |
| **Content** | `GET /api/content/` | Get CMS content |
| **Admin** | `GET /api/admin/dashboard` | Admin dashboard data |
| **Comms** | `GET /api/communication/notifications` | Get notifications |
| **Health** | `GET /health` | Health check |

---

## 🗄️ Database Schema

| Table | Key Columns |
|-------|------------|
| **users** | id, name, email, password_hash, role, status, created_at |
| **jobs** | id, title, company_name, description, location, salary_min/max, employment_type, status |
| **applications** | id, user_id, job_id, status, applied_at |
| **content** | id, type, title, body, status |
| **notifications** | id, user_id, message, read, created_at |

---

## 🧪 Running Tests

```bash
# Backend tests
cd job_portal_backend
pytest tests/

# Frontend tests
cd job_portal_frontend
npm test
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Angular, FastAPI & PostgreSQL
</p>
