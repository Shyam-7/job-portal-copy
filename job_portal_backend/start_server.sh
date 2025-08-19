#!/bin/bash
cd /Users/css/Documents/job-portal/job_portal_backend
/Users/css/Documents/job-portal/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
