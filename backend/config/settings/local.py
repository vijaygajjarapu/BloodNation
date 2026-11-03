"""Local development on a developer computer."""

from config.env import env_bool, env_list, env_str

from .base import *  # noqa: F403

DEBUG = env_bool("DJANGO_DEBUG", True)
# Not a secret: only for local development. Staging and production require a real value.
SECRET_KEY = env_str("DJANGO_SECRET_KEY", "local-development-only-not-a-secret")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ("localhost", "127.0.0.1", "[::1]"))
