"""
WSGI config for CSECJF project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csecjf.settings")
application = get_wsgi_application()
