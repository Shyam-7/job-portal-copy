# 🎯 Quick pgAdmin Reference Card

## 📊 What You'll See in pgAdmin

### 🗂️ Your Database Structure:
```
Job Portal Database
└── job_portal
    └── public schema
        └── 7 Tables:
            ├── announcements (0 rows)
            ├── applications (0 rows)  
            ├── content (0 rows)
            ├── job_seeker_profiles (0 rows)
            ├── jobs (0 rows)
            ├── notifications (0 rows)
            └── users (3 rows) ← HAS DATA
```

### 👥 Current Users Data:
| Name | Email | Role |
|------|-------|------|
| Test User | test@example.com | job_seeker |
| PostgreSQL Test User | postgres_test@example.com | job_seeker |
| PostgreSQL User | postgres_user@example.com | job_seeker |

---

## 🚀 Quick Connection Steps:

1. **Open pgAdmin 4** (should be opening now)
2. **Right-click "Servers"** → Create → Server
3. **Enter details:**
   - Name: `Job Portal Database`
   - Host: `127.0.0.1`
   - Port: `5432`
   - Username: `css`
   - Password: (empty)
4. **Save** and connect
5. **Navigate:** Servers → Job Portal Database → Databases → job_portal → Schemas → public → Tables
6. **View data:** Right-click `users` → View/Edit Data → All Rows

---

## 🎨 What the pgAdmin Interface Looks Like:

```
┌─────────────────────────────────────────────────────────────┐
│ File  Edit  View  Tools  Help                               │
├─────────────────┬───────────────────────────────────────────┤
│ 📁 Servers      │                                           │
│  └─🖥️ Job Portal│        Data Grid Area                     │
│    └─📁 Database│    ┌─────────────────────────────────┐     │
│      └─📁 job_po│    │ id    │ name  │ email │ role     │     │
│        └─📁 Sche│    ├───────┼───────┼───────┼─────────┤     │
│          └─📁 pu│    │ a0a1c │ Test  │ test@ │ job_seek │     │
│            └─📊 │    │ de5be │ Post  │ post@ │ job_seek │     │
│              users   │ ad90c │ User  │ user@ │ job_seek │     │
│              jobs    └─────────────────────────────────┘     │
│              apps                                            │
│                                                              │
└─────────────────┴──────────────────────────────────────────┘
```

---

## 🔍 Useful pgAdmin Features:

### 📋 View Data:
- Right-click table → "View/Edit Data" → "All Rows"

### ✏️ Edit Data:
- Double-click any cell to edit directly

### 🔎 Filter Data:
- Use the filter icon in the data grid toolbar

### 📊 Run Queries:
- Right-click database → "Query Tool"

### 📈 Table Info:
- Right-click table → "Properties" to see structure

### 💾 Export Data:
- Right-click table → "Import/Export..."

---

## 🧪 Test Queries to Try:

```sql
-- See all users with creation dates
SELECT name, email, created_at FROM users ORDER BY created_at;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals
FROM pg_stats 
WHERE schemaname = 'public';

-- Show table structure
\d users
```

Your data is ready to explore in pgAdmin! 🎉
