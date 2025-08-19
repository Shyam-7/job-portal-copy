# 🖥️ pgAdmin GUI - Step-by-Step Visual Guide

## 📋 Your Database Connection Details
- **Host**: `127.0.0.1`
- **Port**: `5432`
- **Database**: `job_portal`
- **Username**: `css`
- **Password**: (leave empty)

---

## 🎯 Step 1: Launch pgAdmin
pgAdmin should now be opening. If not, you can find it in your Applications folder.

## 🎯 Step 2: Set Master Password (First Time Only)
When pgAdmin opens for the first time, it will ask for a master password:
- Set any secure password (this is just for pgAdmin security)
- Remember this password for future pgAdmin sessions

## 🎯 Step 3: Create Server Connection

### What you'll see:
- Left sidebar with "Servers" folder
- Main dashboard area

### What to do:
1. **Right-click** on "Servers" in the left sidebar
2. Select **"Create"** → **"Server..."**

## 🎯 Step 4: Fill Server Details

### General Tab:
- **Name**: `Job Portal Database` (or any name you like)

### Connection Tab:
- **Host name/address**: `127.0.0.1`
- **Port**: `5432`
- **Maintenance database**: `postgres`
- **Username**: `css`
- **Password**: (leave this field EMPTY)
- **Save password?**: ✅ Check this box

### Click "Save"

## 🎯 Step 5: Navigate to Your Data

After successful connection, you'll see this hierarchy in the left sidebar:

```
📁 Servers
  └── 📁 Job Portal Database
      └── 📁 Databases
          ├── 📁 postgres
          └── 📁 job_portal ← Click here to expand
              └── 📁 Schemas
                  └── 📁 public ← Click here to expand
                      └── 📁 Tables ← Click here to expand
                          ├── 📊 announcements
                          ├── 📊 applications
                          ├── 📊 content
                          ├── 📊 job_seeker_profiles
                          ├── 📊 jobs
                          ├── 📊 notifications
                          └── 📊 users ← Your data is here!
```

## 🎯 Step 6: View Your Data

### To see data in the `users` table:
1. **Right-click** on `users` table
2. Select **"View/Edit Data"** → **"All Rows"**

### You should see a table like this:
| id | name | email | role | status | created_at |
|---|---|---|---|---|---|
| a0a1c6b8-d735-4367-b901-6039115a1d16 | Test User | test@example.com | job_seeker | active | 2025-08-18... |
| de5be416-f721-4b2e-a8fa-6e5d63cb41b4 | PostgreSQL Test User | postgres_test@example.com | job_seeker | active | 2025-08-18... |
| ad90cdd8-fc74-4ffa-ae6c-a1c672c9d3a2 | PostgreSQL User | postgres_user@example.com | job_seeker | active | 2025-08-18... |

### To see data in other tables:
- Right-click **"jobs"** → "View/Edit Data" → "All Rows" (currently empty)
- Right-click **"applications"** → "View/Edit Data" → "All Rows" (currently empty)
- And so on...

## 🎯 Step 7: Run Custom SQL Queries

### To execute SQL commands:
1. **Right-click** on `job_portal` database
2. Select **"Query Tool"**
3. In the SQL editor that opens, you can type queries like:

```sql
-- See all users
SELECT * FROM users;

-- Count records in all tables
SELECT 
    'users' as table_name, 
    COUNT(*) as count 
FROM users
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs
UNION ALL
SELECT 'applications', COUNT(*) FROM applications;

-- See table structure
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;
```

4. Click the **"Execute"** button (⚡ icon) or press **F5**

---

## 🚨 Troubleshooting

### ❌ "Connection refused" error:
```bash
# Make sure PostgreSQL is running
brew services start postgresql@14
```

### ❌ "Authentication failed" error:
- Make sure Username is `css` (your system username)
- Leave Password field EMPTY
- Host should be `127.0.0.1`

### ❌ Can't find pgAdmin:
```bash
# Install pgAdmin if not found
brew install --cask pgadmin4

# Or open from Applications
open /Applications/pgAdmin\ 4.app
```

### ❌ Database not found:
```bash
# Recreate database if needed
cd /Users/css/Documents/job-portal/job_portal_backend
python setup_postgres.py
```

---

## 🎉 What You Should See

Once connected successfully, you'll have a full GUI interface where you can:

✅ **Browse all your tables visually**
✅ **See data in spreadsheet format**
✅ **Edit data directly in the GUI**
✅ **Run SQL queries with syntax highlighting**
✅ **Monitor database performance**
✅ **Create/modify tables visually**
✅ **Import/export data**

Your PostgreSQL database with Job Portal data is now fully accessible through the pgAdmin graphical interface! 🎯
