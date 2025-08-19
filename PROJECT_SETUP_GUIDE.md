# Job Portal - PostgreSQL Setup and Project Running Guide

## 🗄️ Connecting to PostgreSQL Database with pgAdmin

### Step 1: Open pgAdmin
1. Open **pgAdmin 4** from Applications (already installed on your system)
2. You'll be prompted to set a master password for pgAdmin - choose a secure password

### Step 2: Create a New Server Connection
1. Right-click on "Servers" in the left panel
2. Select "Create" → "Server..."
3. In the "General" tab:
   - **Name**: `Job Portal Local`
4. In the "Connection" tab:
   - **Host name/address**: `127.0.0.1` or `localhost`
   - **Port**: `5432`
   - **Maintenance database**: `postgres`
   - **Username**: `css` (your current user)
   - **Password**: Leave empty (no password for local development)
   - **Save password**: Check this box

### Step 3: Connect and Explore
1. Click "Save" to create the connection
2. Expand "Job Portal Local" → "Databases" → "job_portal"
3. Navigate to "Schemas" → "public" → "Tables" to see all your tables:
   - `users`
   - `jobs`
   - `applications` 
   - `job_seeker_profiles`
   - `notifications`
   - `announcements`
   - `content`

### Step 4: View Data
1. Right-click on any table (e.g., `users`)
2. Select "View/Edit Data" → "All Rows"
3. You'll see the PostgreSQL data including the test users we created

---

## 🚀 How to Run the Job Portal Project

### Prerequisites Check
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# Should show: postgresql@14 started
```

### Step 1: Start PostgreSQL (if not running)
```bash
brew services start postgresql@14
```

### Step 2: Navigate to Project Directory
```bash
cd /Users/css/Documents/job-portal
```

### Step 3: Activate Python Virtual Environment
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### Step 5: Navigate to Backend Directory
```bash
cd job_portal_backend
```

### Step 6: Set Environment Variables
Ensure your `.env` file has the correct PostgreSQL settings:
```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=css
DB_PASSWORD=
DB_NAME=job_portal
JWT_SECRET=mysecret
```

### Step 7: Start the FastAPI Server
```bash
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Verify Server is Running
Open a new terminal and test:
```bash
# Test basic connectivity
curl http://localhost:8000/

# Test database connection
curl http://localhost:8000/api/db-test

# Test health endpoint
curl http://localhost:8000/health
```

---

## 🧪 Testing the API Endpoints

### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123",
    "name": "New User"
  }'
```

### User Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securepass123"
  }'
```

### View API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 Database Management Commands

### Connect to PostgreSQL CLI
```bash
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
psql -U css -d job_portal
```

### Useful SQL Commands
```sql
-- List all tables
\dt

-- Describe a table structure
\d users

-- View all users
SELECT * FROM users;

-- Count records in each table
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs
UNION ALL
SELECT 'applications', COUNT(*) FROM applications;

-- Exit psql
\q
```

---

## 🔧 Troubleshooting

### PostgreSQL Not Starting
```bash
# Check if PostgreSQL is installed
brew list | grep postgresql

# Restart PostgreSQL
brew services restart postgresql@14

# Check PostgreSQL logs
tail -f /opt/homebrew/var/log/postgresql@14.log
```

### Port 8000 Already in Use
```bash
# Kill existing processes on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Virtual Environment Issues
```bash
# Recreate virtual environment if needed
cd /Users/css/Documents/job-portal
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U css -d postgres -c "SELECT version();"

# Recreate database if needed
python setup_postgres.py
```

---

## 📋 Project Structure Overview

```
job-portal/
├── job_portal_backend/          # FastAPI Backend
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Database configuration
│   ├── auth_routes_mysql.py     # Authentication routes
│   ├── job_routes.py            # Job management routes
│   ├── application_routes.py    # Application routes
│   ├── user_routes.py           # User management routes
│   ├── admin_routes.py          # Admin routes
│   ├── communication_routes.py  # Communication routes
│   ├── db_utils.py              # Database utilities
│   ├── setup_postgres.py        # Database setup script
│   └── .env                     # Environment variables
├── job_portal_frontend/         # Angular Frontend
├── requirements.txt             # Python dependencies
└── .venv/                       # Python virtual environment
```

---

## 🎯 Quick Start Commands

For daily development, use these commands:

```bash
# 1. Start PostgreSQL
brew services start postgresql@14

# 2. Navigate to project
cd /Users/css/Documents/job-portal

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Start backend server
cd job_portal_backend
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 5. In another terminal, start frontend (if needed)
cd /Users/css/Documents/job-portal/job_portal_frontend
ng serve
```

Your backend will be available at: http://localhost:8000
Your frontend will be available at: http://localhost:4200

---

## 🔍 Monitoring and Logs

### View Server Logs
```bash
# If running in background
tail -f server.log

# Live monitoring
uvicorn main:app --reload --log-level debug
```

### Database Performance
Use pgAdmin to:
- Monitor active connections
- View query performance
- Analyze table sizes
- Check index usage

---

This guide provides everything you need to connect to your PostgreSQL database with pgAdmin and run your Job Portal project successfully!
