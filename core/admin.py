from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Household, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "household", "is_staff")
    list_filter = UserAdmin.list_filter + ("role", "household")
    fieldsets = UserAdmin.fieldsets + (
        ("Family", {"fields": ("role", "household")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Family", {"fields": ("role", "household")}),
    )


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("name",)
