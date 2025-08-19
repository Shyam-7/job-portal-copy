# PostgreSQL Migration Guide

This guide walks you through migrating the Job Portal application from MySQL to PostgreSQL.

## Prerequisites

1. **Install PostgreSQL** (if not already installed):
   ```bash
   # macOS with Homebrew
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Install Python PostgreSQL adapter**:
   ```bash
   pip install psycopg2-binary
   ```

## Migration Steps

### 1. Update Dependencies

The `requirements.txt` has been updated to use `psycopg2-binary` instead of `mysql-connector-python`.

### 2. Update Environment Configuration

Update your `.env` file with PostgreSQL settings:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_NAME=job_portal
JWT_SECRET=mysecret
```

**Note**: Replace `your_postgres_password` with your actual PostgreSQL password.

### 3. Create PostgreSQL Database

Run the setup script to create the database and tables:

```bash
cd job_portal_backend
python setup_postgres.py
```

This script will:
- Create the `job_portal` database
- Create all necessary tables with proper schema
- Set up indexes for optimal performance
- Enable UUID extension

### 4. Data Migration (if needed)

If you have existing data in MySQL that you want to migrate:

1. **Export data from MySQL**:
   ```bash
   mysqldump -u root -p job_portal > mysql_backup.sql
   ```

2. **Convert MySQL dump to PostgreSQL format** (manual process):
   - Replace MySQL-specific syntax with PostgreSQL equivalents
   - Update data types if necessary
   - Handle AUTO_INCREMENT to SERIAL conversions

3. **Import to PostgreSQL**:
   ```bash
   psql -U postgres -d job_portal -f converted_backup.sql
   ```

### 5. Updated Files

The following files have been updated for PostgreSQL compatibility:

- `config.py` - Updated database URL format
- `db/session.py` - Updated SQLAlchemy engine configuration
- `db_utils.py` - New shared database utility functions
- `main.py` - Updated database test endpoint
- All route files (`*_routes.py`) - Updated database connections
- `requirements.txt` - Updated dependencies

### 6. Key Differences

| Aspect | MySQL | PostgreSQL |
|--------|-------|------------|
| Driver | `mysql-connector-python` | `psycopg2-binary` |
| URL Format | `mysql+mysqlconnector://` | `postgresql+psycopg2://` |
| Default Port | 3306 | 5432 |
| Auto Increment | `AUTO_INCREMENT` | `SERIAL` or `gen_random_uuid()` |
| JSON Support | JSON type | JSON/JSONB types |
| Case Sensitivity | Case insensitive | Case sensitive |

### 7. Testing the Migration

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test database connection**:
   ```bash
   curl http://localhost:8000/api/db-test
   ```

   You should see a response indicating successful PostgreSQL connection.

4. **Test API endpoints**:
   ```bash
   # Test user registration
   curl -X POST http://localhost:8000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpass123","name":"Test User"}'
   ```

### 8. Performance Optimizations

PostgreSQL-specific optimizations included:

- Proper indexing on frequently queried columns
- UUID extension for better ID generation
- JSON/JSONB support for flexible data storage
- Connection pooling with SQLAlchemy

### 9. Backup and Recovery

**Backup PostgreSQL database**:
```bash
pg_dump -U postgres -d job_portal > postgres_backup.sql
```

**Restore PostgreSQL database**:
```bash
psql -U postgres -d job_portal < postgres_backup.sql
```

### 10. Troubleshooting

**Common Issues**:

1. **Connection refused**: Ensure PostgreSQL is running
   ```bash
   brew services start postgresql  # macOS
   sudo systemctl start postgresql  # Linux
   ```

2. **Authentication failed**: Check username/password in `.env`

3. **Database doesn't exist**: Run `setup_postgres.py` script

4. **Permission denied**: Ensure PostgreSQL user has necessary privileges
   ```sql
   GRANT ALL PRIVILEGES ON DATABASE job_portal TO postgres;
   ```

**Verify Migration Success**:
```bash
# Check if all tables were created
psql -U postgres -d job_portal -c "\dt"

# Check table structure
psql -U postgres -d job_portal -c "\d users"
```

## Conclusion

The migration from MySQL to PostgreSQL is now complete. The application should work identically with improved performance and better data integrity features provided by PostgreSQL.

All API endpoints remain the same, and the application maintains full backward compatibility in terms of functionality.
