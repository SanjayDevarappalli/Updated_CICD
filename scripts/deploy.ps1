# Deployment script for CI/CD pipeline (Windows PowerShell)
# This script runs on the self-hosted runner after CI tests pass

$PROJECT_DIR = "C:\Users\windows\OneDrive\Desktop\sanjay'sn floder\CICD_project_django"
$SERVER_LOG = "$PROJECT_DIR\server.log"

Write-Host "Starting deployment..."

Set-Location $PROJECT_DIR

# Pull latest changes
Write-Host "Pulling latest code..."
git pull origin main

# Install/update dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
Write-Host "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
Write-Host "Collecting static files..."
python manage.py collectstatic --noinput

# Stop existing server if running
Write-Host "Restarting application server..."
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*manage.py runserver*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# Start server in background
Start-Process -FilePath "python" -ArgumentList "manage.py runserver 0.0.0.0:8000" -WorkingDirectory $PROJECT_DIR -WindowStyle Hidden -RedirectStandardOutput $SERVER_LOG -RedirectStandardError $SERVER_LOG

Write-Host "Deployment complete!"
Write-Host "Application running at http://localhost:8000"
