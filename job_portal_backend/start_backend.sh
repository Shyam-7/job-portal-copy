#!/bin/bash
cd /Users/css/Documents/job-portal/job_portal_backend
export $(cat .env | xargs)
exec /Users/css/Documents/job-portal/.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
