import os

from django.core.asgi import get_asgi_application

# Defaults to production so a missing setting fails safely instead of running in debug.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
application = get_asgi_application()
