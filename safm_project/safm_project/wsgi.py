"""
WSGI config for safm_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Production: sets the DJANGO_SETTINGS_MODULE environment variable to safm_project.settings.production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safm_project.settings.production')

application = get_wsgi_application()
