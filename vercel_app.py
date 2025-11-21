import os
import sys
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django environment variables
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('SECRET_KEY', 'your-vercel-secret-key-change-this-in-dashboard')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '.vercel.app,127.0.0.1,localhost')
os.environ.setdefault('VERCEL', '1')

def handler(request, response):
    """Vercel serverless function handler for Django"""
    try:
        import django
        from django.core.wsgi import get_wsgi_application
        from django.core.handlers.wsgi import WSGIHandler
        from io import StringIO
        import json
        
        # Setup Django
        django.setup()
        
        # Create Django WSGI application
        application = get_wsgi_application()
        
        # Convert Vercel request to WSGI environ
        environ = {
            'REQUEST_METHOD': request.method,
            'PATH_INFO': request.path,
            'QUERY_STRING': request.query,
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', ''),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(request.body.decode('utf-8') if request.body else ''),
            'wsgi.errors': StringIO(),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'wsgi.headers': request.headers,
        }
        
        # Add HTTP headers
        for key, value in request.headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Create a simple response collector
        status = []
        headers = []
        body = []
        
        def start_response(status_line, response_headers):
            status.append(status_line)
            headers.extend(response_headers)
        
        # Call Django application
        response_body = application(environ, start_response)
        body.extend(response_body)
        
        # Set Vercel response
        if status:
            status_code = int(status[0].split()[0])
            response.status = status_code
            
        for header_name, header_value in headers:
            if header_name.lower() == 'content-type':
                response.headers["Content-Type"] = header_value
        
        # Return response body
        return [b''.join(body)]
        
    except Exception as e:
        print(f"Error in Django handler: {e}")
        import traceback
        traceback.print_exc()
        
        response.status = 500
        response.headers["Content-Type"] = "text/plain"
        return [f"Django application error: {str(e)}".encode()]

# For WSGI compatibility
application = handler