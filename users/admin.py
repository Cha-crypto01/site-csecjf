from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Interface d'administration Django native pour les utilisateurs."""

    list_display = (
        "username",
        "email",
        "role",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "is_active")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Rôle CSECJF", {"fields": ("role", "phone", "avatar")}),
    )
