from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


def home(request):
    """Landing page that extends the base layout and shows an HTMX demo."""
    return render(request, "home.html")


def health(request):
    """Lightweight health check used to confirm the app is up."""
    return JsonResponse({"status": "ok"})


def ping(request):
    """Tiny HTMX fragment endpoint used by the home page demo button."""
    return HttpResponse("<span>pong</span>")
