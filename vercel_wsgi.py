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
os.environ.setdefault('ALLOWED_HOSTS', '.vercel.app,127.0.0.1,localhost')

# Ensure VERCEL environment variable is set for database config
os.environ.setdefault('VERCEL', '1')

def handler(request, response):
    """Vercel serverless function handler"""
    try:
        import django
        from django.core.wsgi import get_wsgi_application
        
        # Setup Django
        django.setup()
        
        # Create the WSGI application
        application = get_wsgi_application()
        
        # Call the WSGI application
        return application(request, response)
        
    except Exception as e:
        print(f"Error during Django setup: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        response.status = 500
        response.headers["Content-Type"] = "text/plain"
        return [b"Application initialization failed. Check logs for details."]

# For compatibility with WSGI servers
try:
    import django
    from django.core.wsgi import get_wsgi_application
    
    # Setup Django
    django.setup()
    
    # Create the WSGI application
    application = get_wsgi_application()
    
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