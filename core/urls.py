from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("household/", views.household_members, name="household_members"),
    path("chores/new/", views.chore_create, name="chore_create"),
    path("chores/", views.my_chores, name="my_chores"),
    path("chores/<int:chore_id>/done/", views.chore_mark_done, name="chore_mark_done"),
    path("chores/verify/", views.pending_verifications, name="pending_verifications"),
    path("chores/<int:chore_id>/verify/", views.chore_verify, name="chore_verify"),
    path("members/new/", views.member_create, name="member_create"),
    path("health/", views.health, name="health"),
    path("ping/", views.ping, name="ping"),
]
