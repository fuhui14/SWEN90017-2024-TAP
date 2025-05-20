#!/usr/bin/env bash

# Exit immediately if any command fails, and ensure all background subprocesses are
# terminated when this script exits.
set -e
trap "echo; echo 'Stopping all subprocesses…'; kill 0" EXIT

# If you use a Python virtual environment named "venv", activate it.
# Otherwise, remove or adjust this block as needed.
if [ -f venv/bin/activate ]; then
  echo "Activating Python virtual environment…"
  source venv/bin/activate
fi

# Change to the directory where this script resides (assumed to be `backend/`).
cd "$(dirname "$0")"

# ─── Start Redis Server ───────────────────────────────────────────────────────
echo
echo "🟢 Starting Redis server…"
redis-server &

# ─── Start Celery Worker ──────────────────────────────────────────────────────
echo
echo "🟢 Starting Celery worker…"
# Replace `project_name` with your Django project module name (the folder
# that contains settings.py and is a sibling to manage.py).
celery -A project_name worker --loglevel=info &

# ─── (Optional) Start Celery Beat ─────────────────────────────────────────────
echo
echo "🟢 Starting Celery beat…"
celery -A project_name beat --loglevel=info &

# ─── Start Django Development Server ─────────────────────────────────────────
echo
echo "🟢 Starting Django development server on http://127.0.0.1:8000…"
python manage.py runserver 0.0.0.0:8000 &

# ─── Start React Development Server ───────────────────────────────────────────
echo
echo "🟢 Starting React frontend…"
# Navigate up one level from `backend/` into the `frontend/` directory.
cd ../frontend

# Install Node dependencies (comment out if already installed).
npm install

# Launch the React development server (e.g., create-react-app setup).
npm start

# Wait for the React process (foreground) or until user interrupts (Ctrl+C).
wait
