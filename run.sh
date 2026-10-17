#!/bin/bash
# One command to start Scam Shield: ./run.sh
cd "$(dirname "$0")"
source .venv/bin/activate
git pull --ff-only 2>/dev/null | tail -1
echo "Dashboard: http://localhost:8000   (Ctrl+C stops it; ./run.sh starts it again)"
exec uvicorn app.main:app --port 8000
