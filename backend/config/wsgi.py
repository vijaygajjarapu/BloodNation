import os

from django.core.wsgi import get_wsgi_application

# Defaults to production so a missing setting fails safely instead of running in debug.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
application = get_wsgi_application()
