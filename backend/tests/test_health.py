from django.conf import settings


def test_health_returns_ok(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "bloodnation-backend",
        "version": settings.APP_VERSION,
    }


def test_health_exposes_no_secrets(client):
    body = client.get("/health/").content.decode()
    assert settings.SECRET_KEY not in body


def test_health_only_allows_get(client):
    assert client.post("/health/").status_code == 405
