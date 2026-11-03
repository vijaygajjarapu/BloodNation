"""Automated tests."""
from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-only-not-a-secret"
ALLOWED_HOSTS = ["testserver", "localhost"]
