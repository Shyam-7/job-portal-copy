#!/bin/bash

# Job Portal Startup Script
echo "🚀 Starting Job Portal Application..."

# Check if PostgreSQL is running
if ! brew services list | grep -q "postgresql@14.*started"; then
    echo "📊 Starting PostgreSQL..."
    brew services start postgresql@14
    sleep 3
else
    echo "✅ PostgreSQL is already running"
fi

# Navigate to project directory
cd /Users/css/Documents/job-portal

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source .venv/bin/activate

# Navigate to backend
cd job_portal_backend

# Export PostgreSQL path
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Test database connection
echo "🔍 Testing database connection..."
if python -c "from db_utils import get_db_connection; conn = get_db_connection(); conn.close(); print('Database connection successful!')"; then
    echo "✅ Database connection verified"
else
    echo "❌ Database connection failed"
    echo "🔧 Running database setup..."
    python setup_postgres.py
fi

# Start the server
echo "🌐 Starting FastAPI server on http://localhost:8000..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
