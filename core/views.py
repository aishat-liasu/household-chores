from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ChoreForm, MemberCreationForm
from .models import Chore


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


@login_required
def household_members(request):
    """List members of the signed-in user's household (household-scoped)."""
    household = request.user.household
    members = household.members.all() if household else []
    return render(request, "household/members.html",
                  {"household": household, "members": members})


@login_required
def chore_create(request):
    """Parent-only: create a chore and assign it to a household member."""
    if not request.user.is_parent:
        raise PermissionDenied
    household = request.user.household
    if request.method == "POST":
        form = ChoreForm(request.POST, household=household)
        if form.is_valid():
            chore = form.save(commit=False)
            chore.household = household
            chore.status = Chore.Status.ASSIGNED
            chore.save()
            return redirect("dashboard")
    else:
        form = ChoreForm(household=household)
    return render(request, "chores/create.html", {"form": form})


@login_required
def my_chores(request):
    """List the signed-in member's own chores (pending first)."""
    chores = request.user.chores.order_by("status", "-created_at")
    return render(request, "chores/mine.html", {"chores": chores})


@login_required
@require_POST
def chore_mark_done(request, chore_id):
    """Member marks their own chore done (awaiting verification). No points yet."""
    chore = get_object_or_404(Chore, id=chore_id)
    if chore.assignee_id != request.user.id:
        raise PermissionDenied
    if chore.status == Chore.Status.ASSIGNED:
        chore.status = Chore.Status.DONE
        chore.save(update_fields=["status"])
    return render(request, "chores/_chore_row.html", {"chore": chore})


def health(request):
    """Lightweight health check used to confirm the app is up."""
    return JsonResponse({"status": "ok"})


def ping(request):
    """Tiny HTMX fragment endpoint used by the home page demo button."""
    return HttpResponse("<span>pong</span>")
