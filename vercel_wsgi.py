import os
import sys
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('SECRET_KEY', 'your-secret-key-change-this-in-vercel-dashboard')
os.environ.setdefault('DEBUG', 'False')

# Handle Vercel's serverless environment
try:
    import django
    from django.core.wsgi import get_wsgi_application
    
    # Setup Django
    django.setup()
    
    # Create the WSGI application
    application = get_wsgi_application()
    
    # Vercel expects a 'handler' variable
    handler = application
    
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()
    
    # Return a simple WSGI app for error handling
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Application initialization failed. Check logs for details.']
    
    # Vercel expects a 'handler' variable
    handler = application