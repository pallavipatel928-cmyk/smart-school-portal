import os
import sys
from pathlib import Path

# Add project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    import django
    django.setup()
    print("Django setup successful!")
    
    # Test importing the WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application loaded successfully!")
    
except Exception as e:
    print(f"Error during Django setup: {e}")
    import traceback
    traceback.print_exc()