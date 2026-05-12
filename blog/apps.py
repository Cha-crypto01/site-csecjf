from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration de l'application Blog — Gestion des articles."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    verbose_name = "Blog et Articles"
