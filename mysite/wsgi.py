"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/opt/bitnami/projects/mysite')
sys.path.append('/home/bitnami/.local/lib/python3.8/site-packages')

os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/projects/mysite/egg_cache")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

os.environ['HTTPS'] = "on"
os.environ['wsgi.url_scheme'] = 'https'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()