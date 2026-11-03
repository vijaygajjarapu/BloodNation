import importlib
import sys

import pytest
from django.core.exceptions import ImproperlyConfigured

PRODUCTION = "config.settings.production"
STAGING = "config.settings.staging"


@pytest.fixture(autouse=True)
def fresh_modules():
    for name in (PRODUCTION, STAGING):
        sys.modules.pop(name, None)
    yield
    for name in (PRODUCTION, STAGING):
        sys.modules.pop(name, None)


def test_test_settings_load():
    from django.conf import settings

    assert settings.DEBUG is False
    assert "apps.core" in settings.INSTALLED_APPS


def test_production_requires_secret_key(monkeypatch):
    monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    monkeypatch.setenv("DJANGO_ALLOWED_HOSTS", "example.com")
    with pytest.raises(ImproperlyConfigured):
        importlib.import_module(PRODUCTION)


def test_production_requires_allowed_hosts(monkeypatch):
    monkeypatch.setenv("DJANGO_SECRET_KEY", "x" * 50)
    monkeypatch.delenv("DJANGO_ALLOWED_HOSTS", raising=False)
    with pytest.raises(ImproperlyConfigured):
        importlib.import_module(PRODUCTION)


def test_production_is_safe_when_configured(monkeypatch):
    monkeypatch.setenv("DJANGO_SECRET_KEY", "x" * 50)
    monkeypatch.setenv("DJANGO_ALLOWED_HOSTS", "example.com")
    module = importlib.import_module(PRODUCTION)
    assert module.DEBUG is False
    assert module.SESSION_COOKIE_SECURE is True
    assert module.CSRF_COOKIE_SECURE is True
    assert module.ALLOWED_HOSTS == ["example.com"]


def test_staging_requires_secret_key(monkeypatch):
    monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    monkeypatch.setenv("DJANGO_ALLOWED_HOSTS", "staging.example.com")
    with pytest.raises(ImproperlyConfigured):
        importlib.import_module(STAGING)
