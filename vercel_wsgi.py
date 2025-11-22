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
        from io import StringIO
        
        # Setup Django
        django.setup()
        
        # Create the WSGI application
        application = get_wsgi_application()
        
        # Convert Vercel request to WSGI environ
        environ = {
            'REQUEST_METHOD': getattr(request, 'method', 'GET'),
            'PATH_INFO': getattr(request, 'path', '/'),
            'QUERY_STRING': getattr(request, 'query', ''),
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', ''),
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(getattr(request, 'body', b'').decode('utf-8') if getattr(request, 'body', b'') else ''),
            'wsgi.errors': StringIO(),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'wsgi.headers': getattr(request, 'headers', {}),
        }
        
        # Add HTTP headers
        for key, value in getattr(request, 'headers', {}).items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Create a simple response collector
        status = []
        headers = []
        body = []
        
        def start_response(status_line, response_headers):
            status.append(status_line)
            headers.extend(response_headers)
        
        # Call Django application
        try:
            response_body = application(environ, start_response)
            body.extend(response_body)
        except Exception as e:
            print(f"Error calling Django app: {e}")
            raise
        
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
app = handler