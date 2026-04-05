#!/bin/bash
# Deployment script for CI/CD pipeline
# This script runs on the self-hosted runner after CI tests pass

set -e

PROJECT_DIR="C:/Users/windows/OneDrive/Desktop/sanjay'sn floder/CICD_project_django"
WEB_USER="runner"

echo "Starting deployment..."

cd "$PROJECT_DIR"

# Pull latest changes
echo "Pulling latest code..."
git pull origin main

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Stop existing server if running
echo "Restarting application server..."
pkill -f "python manage.py runserver" || true

# Start server in background
nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &

echo "Deployment complete!"
echo "Application running at http://localhost:8000"
