from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import parent_required
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
@parent_required
def member_create(request):
    """Parent-only: create another family member's account."""
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
@parent_required
def chore_create(request):
    """Parent-only: create a chore and assign it to a household member."""
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


@login_required
@parent_required
def pending_verifications(request):
    """Parent-only: chores in the parent's household awaiting verification."""
    chores = Chore.objects.filter(
        household=request.user.household, status=Chore.Status.DONE)
    return render(request, "chores/verify_list.html", {"chores": chores})


@login_required
@parent_required
@require_POST
def chore_verify(request, chore_id):
    """Parent-only: approve a done chore in the parent's household."""
    chore = get_object_or_404(Chore, id=chore_id, household=request.user.household)
    if chore.status == Chore.Status.DONE:
        chore.status = Chore.Status.VERIFIED
        chore.save(update_fields=["status"])
        chore.spawn_next()
    return render(request, "chores/_verify_row.html", {"chore": chore})


@login_required
def points_tally(request):
    """Each household member's total verified points."""
    household = request.user.household
    members = household.members.all() if household else []
    rows = [(m, m.verified_points) for m in members]
    return render(request, "chores/tally.html", {"rows": rows})


def health(request):
    """Lightweight health check used to confirm the app is up."""
    return JsonResponse({"status": "ok"})


def ping(request):
    """Tiny HTMX fragment endpoint used by the home page demo button."""
    return HttpResponse("<span>pong</span>")
