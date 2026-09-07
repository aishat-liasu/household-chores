from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import MemberCreationForm


def home(request):
    """Landing page that extends the base layout and shows an HTMX demo."""
    return render(request, "home.html")


@login_required
def dashboard(request):
    """A signed-in member's landing area; used to prove auth protection."""
    return render(request, "dashboard.html")


@login_required
def member_create(request):
    """Parent-only: create another family member's account."""
    if not request.user.is_parent:
        raise PermissionDenied
    if request.method == "POST":
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = MemberCreationForm()
    return render(request, "members/create.html", {"form": form})


def health(request):
    """Lightweight health check used to confirm the app is up."""
    return JsonResponse({"status": "ok"})


def ping(request):
    """Tiny HTMX fragment endpoint used by the home page demo button."""
    return HttpResponse("<span>pong</span>")
