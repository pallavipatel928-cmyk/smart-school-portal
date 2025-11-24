"""
WSGI config for Smart School Portal on PythonAnywhere
"""
import os
import sys
from pathlib import Path

# Add your project directory to the sys.path
project_dir = Path(__file__).resolve().parent
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# Set environment variable to indicate PythonAnywhere deployment
os.environ.setdefault('PYTHONANYWHERE', '1')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import and initialize Django
import django
django.setup()

# Import the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()