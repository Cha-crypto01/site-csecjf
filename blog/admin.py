from django.contrib import admin
from .models import Article, AuditLog, GalleryImage


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Configuration de l'interface Django native pour les articles."""

    list_display = (
        "title",
        "author",
        "status",
        "category",
        "created_at",
        "is_deleted",
    )
    list_filter = ("status", "category", "is_deleted", "author")
    search_fields = ("title", "content")
    actions = ["soft_delete_selected"]

    def soft_delete_selected(self, request, queryset):
        """Action admin pour soft-delete en masse."""
        from django.utils import timezone

        for article in queryset:
            article.is_deleted = True
            article.deleted_by = request.user
            article.deleted_at = timezone.now()
            article.save()

    soft_delete_selected.short_description = "Supprimer (soft delete) les articles sélectionnés"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Interface d'administration pour la galerie photo."""

    list_display = ("caption", "category", "order", "created_at", "image_preview")
    list_filter = ("category",)
    search_fields = ("caption",)
    ordering = ("order", "-created_at")

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width:60px;height:40px;object-fit:cover;border-radius:4px;">'
        return "—"
    image_preview.short_description = "Aperçu"
    image_preview.allow_tags = True


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Configuration de l'interface Django native pour l'audit."""

    list_display = ("action", "user", "article", "created_at")
    list_filter = ("action", "created_at")
    readonly_fields = ("user", "article", "action", "details", "created_at")
