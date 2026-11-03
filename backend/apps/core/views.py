from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    """Proves the application is running. Exposes no secrets or infrastructure details."""
    return JsonResponse(
        {
            "status": "ok",
            "service": "bloodnation-backend",
            "version": settings.APP_VERSION,
        }
    )
