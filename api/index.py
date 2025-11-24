import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add project directory to Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Set environment variables for Vercel
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('VERCEL', '1')

# Initialize Django
import django
django.setup()

# Create WSGI application
application = get_wsgi_application()

def handler(request, response):
    """WSGI handler for Vercel"""
    return application(request, response)