# 🔧 pgAdmin Setup Guide - Visual Steps

## Quick Connection Details
- **Host**: `127.0.0.1` (or `localhost`)
- **Port**: `5432`
- **Database**: `job_portal`
- **Username**: `css`
- **Password**: (leave empty)

---

## Step-by-Step pgAdmin Setup

### 1. Launch pgAdmin 4
```bash
# Open pgAdmin from Applications folder
open -a "pgAdmin 4"
```

### 2. Create Server Connection

**In pgAdmin Interface:**

1. **Right-click** on "Servers" in the left sidebar
2. Select **"Create"** → **"Server..."**

**General Tab:**
- **Name**: `Job Portal Local` (any name you prefer)

**Connection Tab:**
- **Host name/address**: `127.0.0.1`
- **Port**: `5432`
- **Maintenance database**: `postgres`
- **Username**: `css`
- **Password**: (leave blank)
- ✅ **Save password**: Check this box

3. Click **"Save"**

### 3. Navigate to Your Database

**After successful connection:**

```
📁 Servers
  └── 📁 Job Portal Local
      └── 📁 Databases
          ├── 📁 postgres (system database)
          └── 📁 job_portal ← YOUR DATABASE
              └── 📁 Schemas
                  └── 📁 public
                      └── 📁 Tables
                          ├── 📊 users
                          ├── 📊 jobs
                          ├── 📊 applications
                          ├── 📊 job_seeker_profiles
                          ├── 📊 notifications
                          ├── 📊 announcements
                          └── 📊 content
```

### 4. View Table Data

**To see data in any table:**
1. **Right-click** on table name (e.g., `users`)
2. Select **"View/Edit Data"** → **"All Rows"**
3. You'll see all records in a spreadsheet-like view

**Current Users Table Data:**
| id | name | email | role | status |
|---|---|---|---|---|
| a0a1c6b8-d735-... | Test User | test@example.com | job_seeker | active |
| de5be416-f721-... | PostgreSQL Test User | postgres_test@example.com | job_seeker | active |
| ad90cdd8-fc74-... | PostgreSQL User | postgres_user@example.com | job_seeker | active |

### 5. Run SQL Queries

**To execute custom SQL:**
1. **Right-click** on `job_portal` database
2. Select **"Query Tool"**
3. Type your SQL queries, for example:

```sql
-- Get all users
SELECT * FROM users;

-- Count records in each table
SELECT 
    'users' as table_name, 
    COUNT(*) as record_count 
FROM users
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs
UNION ALL
SELECT 'applications', COUNT(*) FROM applications;

-- Show table structure
SELECT 
    column_name, 
    data_type, 
    is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;
```

---

## 🚀 Running the Project

### Option 1: Quick Start (Recommended)
```bash
cd /Users/css/Documents/job-portal
./start_project.sh
```

### Option 2: Manual Start
```bash
# 1. Start PostgreSQL
brew services start postgresql@14

# 2. Navigate to project
cd /Users/css/Documents/job-portal

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Go to backend directory
cd job_portal_backend

# 5. Set PostgreSQL path
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# 6. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Background Mode
```bash
cd /Users/css/Documents/job-portal/job_portal_backend
source ../.venv/bin/activate
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

---

## 🌐 Access Points

Once running, your application will be available at:

- **🏠 Main API**: http://localhost:8000/
- **📚 API Documentation (Swagger)**: http://localhost:8000/docs
- **📖 Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **🔍 Database Test**: http://localhost:8000/api/db-test
- **❤️ Health Check**: http://localhost:8000/health

---

## 🧪 API Testing Examples

### Test Database Connection
```bash
curl http://localhost:8000/api/db-test
```

### Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@jobportal.com",
    "password": "secure123",
    "name": "Demo User"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@jobportal.com",
    "password": "secure123"
  }'
```

---

## 📊 Database Status Check

Your PostgreSQL database is currently:
- ✅ **Running** on port 5432
- ✅ **Connected** to Job Portal application
- ✅ **Contains** 7 tables with sample data
- ✅ **Has** 3 test users ready for testing

**Connection verified**: PostgreSQL 14.19 on macOS ARM64

---

## 🔧 Troubleshooting

### pgAdmin Connection Issues
1. **Ensure PostgreSQL is running**:
   ```bash
   brew services list | grep postgresql
   ```

2. **Check if port 5432 is available**:
   ```bash
   lsof -i :5432
   ```

3. **Test connection manually**:
   ```bash
   psql -U css -d job_portal -c "SELECT version();"
   ```

### Server Won't Start
1. **Check if port 8000 is free**:
   ```bash
   lsof -i :8000
   ```

2. **Kill existing processes**:
   ```bash
   pkill -f uvicorn
   ```

3. **Check logs**:
   ```bash
   tail -f server.log
   ```

Your Job Portal application is ready to use! 🎉
