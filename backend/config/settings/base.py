"""Settings shared by every environment. Secrets and debug are set per environment."""

from pathlib import Path

from config.env import env_str

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APP_VERSION = env_str("APP_VERSION", "0.1.0")

DEBUG = False
ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "apps.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database is configured in Step 8C (PostgreSQL with PostGIS). No product models exist yet.
DATABASES: dict = {}

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
