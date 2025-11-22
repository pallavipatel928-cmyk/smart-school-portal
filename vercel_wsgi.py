import os
import sys
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('SECRET_KEY', 'your-vercel-secret-key-change-this-in-dashboard')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '.vercel.app,127.0.0.1,localhost')

def handler(request, response):
    """Vercel serverless function handler"""
    try:
        import django
        from django.core.wsgi import get_wsgi_application
        
        # Setup Django
        django.setup()
        
        # Create the WSGI application
        application = get_wsgi_application()
        
        # Simple response for now
        response.status = 200
        response.headers["Content-Type"] = "text/plain"
        return [b"Smart School Portal is working on Vercel!"]
        
    except Exception as e:
        print(f"Error during Django setup: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        response.status = 500
        response.headers["Content-Type"] = "text/plain"
        return [f"Application error: {str(e)}".encode()]

# For WSGI compatibility
app = handler