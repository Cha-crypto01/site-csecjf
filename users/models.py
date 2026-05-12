"""
Modèle User personnalisé avec système de rôles :

- super_admin : accès total, gère les comptes et les permissions
- admin : publie, modifie et supprime ses articles
- redacteur : crée des brouillons, modifie ses brouillons
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur CSECJF avec rôles étendus.

    Rôles disponibles via le champ `role` :
    - super_admin : Super Admin (gère tout)
    - admin       : Admin (publie/modifie/supprime)
    - redacteur   : Rédacteur (brouillons uniquement)
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ADMIN = "admin", "Admin"
        REDACTEUR = "redacteur", "Rédacteur"

    role = models.CharField(
        "Rôle",
        max_length=20,
        choices=Role.choices,
        default=Role.REDACTEUR,
        help_text="Définit les permissions de l'utilisateur dans l'interface d'administration.",
    )

    # Métadonnées supplémentaires
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    avatar = models.ImageField(
        "Avatar", upload_to="avatars/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    # --- Permissions helpers ---

    def is_super_admin(self):
        """Vérifie si l'utilisateur est Super Admin."""
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser

    def is_admin(self):
        """Vérifie si l'utilisateur est Admin (ou supérieur)."""
        return self.role in (self.Role.SUPER_ADMIN, self.Role.ADMIN)

    def can_publish(self):
        """Peut publier des articles (Admin et Super Admin)."""
        return self.is_admin()

    def can_delete_any(self):
        """Peut supprimer n'importe quel article (Super Admin uniquement)."""
        return self.is_super_admin()

    def can_manage_users(self):
        """Peut gérer les comptes utilisateurs (Super Admin uniquement)."""
        return self.is_super_admin()
