"""Production. Fails safely at start-up if required values are missing."""

from config.env import env_bool, env_list, require_env

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = require_env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured("Environment variable DJANGO_ALLOWED_HOSTS is required but not set.")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Hosting is not chosen yet (HOSTING-01). Set DJANGO_SECURE_SSL_REDIRECT=false only if TLS is
# handled elsewhere and you understand the effect.
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
