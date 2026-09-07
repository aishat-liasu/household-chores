from django.contrib.auth.models import AbstractUser
from django.db import models


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
