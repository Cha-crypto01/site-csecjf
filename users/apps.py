from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration de l'application Users — Gestion des utilisateurs et rôles."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Utilisateurs et Rôles"
