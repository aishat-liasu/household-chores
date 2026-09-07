from django.http import JsonResponse


def health(request):
    """Lightweight health check used to confirm the app is up."""
    return JsonResponse({"status": "ok"})
