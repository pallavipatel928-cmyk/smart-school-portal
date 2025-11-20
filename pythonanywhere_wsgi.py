# +++++++++++ DJANGO +++++++++++
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/smart-school-portal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# Activate your virtual env
activate_this = '/home/yourusername/.virtualenvs/schoolportal/bin/activate_this.py'
if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django
import django
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

django.setup()
application = StaticFilesHandler(get_wsgi_application())