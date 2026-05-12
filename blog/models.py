"""
Modèles de l'application Blog.

Article : contenu principal avec système de statut (brouillon/publie),
          soft delete, et traçabilité complète des actions.
AuditLog : historique de toutes les actions effectuées.
"""
from django.db import models
from django.conf import settings


class GalleryImage(models.Model):
    """
    Modèle pour les images de la galerie photo.
    Les images uploadées sont stockées dans MEDIA_ROOT/gallery/.
    """
    image = models.ImageField("Image", upload_to="gallery/")
    caption = models.CharField("Légende", max_length=255, blank=True)
    category = models.CharField(
        "Catégorie",
        max_length=50,
        choices=[
            ("activites", "Activités"),
            ("formations", "Formations"),
            ("infrastructures", "Infrastructures"),
        ],
        default="activites",
    )
    order = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField("Date d'ajout", auto_now_add=True)

    class Meta:
        verbose_name = "Image de la galerie"
        verbose_name_plural = "Galerie photo"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"


class Article(models.Model):
    """
    Modèle principal d'article de blog.

    - Supporte le statut brouillon / publié
    - Supporte le soft delete (is_deleted)
    - Trace l'auteur, le modificateur, et le suppresseur
    """

    class Status(models.TextChoices):
        BROUILLON = "brouillon", "Brouillon"
        PUBLIE = "publie", "Publié"

    # --- Contenu ---
    title = models.CharField("Titre", max_length=255)
    subtitle = models.CharField("Sous-titre", max_length=255, blank=True)
    category = models.CharField(
        "Catégorie",
        max_length=50,
        choices=[
            ("Accompagnement", "Accompagnement"),
            ("Partenariat", "Partenariat"),
            ("Formation", "Formation"),
            ("Événement", "Événement"),
            ("Communauté", "Communauté"),
        ],
        default="Accompagnement",
    )
    content = models.TextField("Contenu")
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=Status.choices,
        default=Status.BROUILLON,
    )

    # --- Images (chemin ou base64) ---
    images = models.JSONField(
        "Images",
        default=list,
        blank=True,
        help_text="Liste d'objets {name, data} ou de chemins d'images.",
    )

    # --- Auteur et traçabilité ---
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles_created",
        verbose_name="Auteur",
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles_modified",
        verbose_name="Dernier modificateur",
    )

    # --- Dates ---
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    updated_at = models.DateTimeField("Date de modification", auto_now=True)
    published_at = models.DateTimeField(
        "Date de publication", blank=True, null=True
    )

    # --- Soft delete ---
    is_deleted = models.BooleanField("Supprimé", default=False)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles_deleted",
        verbose_name="Supprimé par",
    )
    deleted_at = models.DateTimeField(
        "Date de suppression", blank=True, null=True
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-définit la date de publication lors du premier passage en 'publié'."""
        if self.status == self.Status.PUBLIE and not self.published_at:
            from django.utils import timezone

            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def soft_delete(self, user):
        """Suppression logique (soft delete) avec traçabilité."""
        from django.utils import timezone

        self.is_deleted = True
        self.deleted_by = user
        self.deleted_at = timezone.now()
        self.save()
        # Enregistre l'action dans l'historique
        AuditLog.objects.create(
            user=user,
            article=self,
            action="delete",
            details=f"Article supprimé par {user.username}",
        )


class AuditLog(models.Model):
    """
    Historique d'activité — trace chaque action sur les articles.

    Actions possibles : create, update, delete, publish, unpublish
    """

    class Action(models.TextChoices):
        CREATE = "create", "Création"
        UPDATE = "update", "Modification"
        DELETE = "delete", "Suppression"
        PUBLISH = "publish", "Publication"
        UNPUBLISH = "unpublish", "Dépublication"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Utilisateur",
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Article",
    )
    action = models.CharField(
        "Action", max_length=20, choices=Action.choices
    )
    details = models.TextField("Détails", blank=True)
    created_at = models.DateTimeField(
        "Date", auto_now_add=True
    )

    class Meta:
        verbose_name = "Action d'audit"
        verbose_name_plural = "Historique d'activité"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_action_display()} — {self.article or 'N/A'} par {self.user or 'Inconnu'}"
