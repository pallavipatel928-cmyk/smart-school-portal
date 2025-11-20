#!/bin/bash

# Quick Setup Script for Smart School Management Portal (Linux/macOS)
# This script automates the setup process

echo "========================================"
echo "Smart School Management Portal - Setup"
echo "========================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found! Please install Python 3.10+ first."
    exit 1
fi

# Check if virtual environment exists
echo ""
echo "Checking virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# Run migrations
echo ""
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate
echo "✓ Database setup complete"

# Create media and static directories
echo ""
echo "Creating directories..."
mkdir -p media/profile_pictures media/assignments media/submissions
echo "✓ Directories created"

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "✓ Static files collected"

# Prompt for superuser creation
echo ""
echo "========================================"
echo "Create Admin Account"
echo "========================================"
echo ""
read -p "Do you want to create an admin account? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Setup complete
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then open your browser and visit:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin/"
echo ""
