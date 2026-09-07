import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Household(models.Model):
    """A single family unit; chores and points are scoped to it."""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Family member account with a parent (admin) or child (member) role."""

    class Role(models.TextChoices):
        PARENT = "parent", "Parent"
        CHILD = "child", "Child"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CHILD)
    household = models.ForeignKey(
        Household,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="members",
    )

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_child(self):
        return self.role == self.Role.CHILD

    @property
    def verified_points(self):
        """Total points from this member's verified chores (derived)."""
        total = self.chores.filter(status="verified").aggregate(
            total=models.Sum("points"))["total"]
        return total or 0


class Chore(models.Model):
    """A task assigned to a family member, worth points once verified."""

    class Status(models.TextChoices):
        ASSIGNED = "assigned", "Assigned"
        DONE = "done", "Done (awaiting verification)"
        VERIFIED = "verified", "Verified"

    class Recurrence(models.TextChoices):
        NONE = "none", "One-off"
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chores"
    )
    household = models.ForeignKey(
        Household, on_delete=models.CASCADE, related_name="chores"
    )
    points = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ASSIGNED
    )
    recurrence = models.CharField(
        max_length=10, choices=Recurrence.choices, default=Recurrence.NONE
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> {self.assignee}"

    def next_due_date(self):
        base = self.due_date or timezone.localdate()
        if self.recurrence == self.Recurrence.DAILY:
            return base + datetime.timedelta(days=1)
        if self.recurrence == self.Recurrence.WEEKLY:
            return base + datetime.timedelta(days=7)
        return None

    def spawn_next(self):
        """Create the next occurrence for a recurring chore, else None."""
        if self.recurrence == self.Recurrence.NONE:
            return None
        return Chore.objects.create(
            title=self.title, description=self.description,
            assignee=self.assignee, household=self.household,
            points=self.points, recurrence=self.recurrence,
            status=Chore.Status.ASSIGNED, due_date=self.next_due_date(),
        )
