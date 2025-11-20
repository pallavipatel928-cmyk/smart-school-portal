# Quick Setup Script for Smart School Management Portal
# This script automates the setup process

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Smart School Management Portal - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.10+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if virtual environment exists
Write-Host ""
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host ""
Write-Host "Setting up database..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "✓ Database setup complete" -ForegroundColor Green

# Create media and static directories
Write-Host ""
Write-Host "Creating directories..." -ForegroundColor Yellow
if (-not (Test-Path "media")) { New-Item -ItemType Directory -Path "media" | Out-Null }
if (-not (Test-Path "media/profile_pictures")) { New-Item -ItemType Directory -Path "media/profile_pictures" | Out-Null }
if (-not (Test-Path "media/assignments")) { New-Item -ItemType Directory -Path "media/assignments" | Out-Null }
if (-not (Test-Path "media/submissions")) { New-Item -ItemType Directory -Path "media/submissions" | Out-Null }
Write-Host "✓ Directories created" -ForegroundColor Green

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear
Write-Host "✓ Static files collected" -ForegroundColor Green

# Prompt for superuser creation
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Create Admin Account" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
$createSuperuser = Read-Host "Do you want to create an admin account? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
}

# Setup complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser and visit:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Admin panel:" -ForegroundColor Yellow
Write-Host "  http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
