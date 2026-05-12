"""
API REST pour exposer les articles publiés au frontend existant (blog.html).
"""
from rest_framework import serializers, viewsets, routers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import path, include
from .models import Article, GalleryImage


class ArticleSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les articles publiés."""

    author_name = serializers.CharField(
        source="author.get_full_name", read_only=True
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "subtitle",
            "category",
            "content",
            "images",
            "author_name",
            "published_at",
            "created_at",
        ]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """API publique : liste des articles publiés (non supprimés)."""

    queryset = Article.objects.filter(
        is_deleted=False, status="publie"
    ).select_related("author")
    serializer_class = ArticleSerializer
    ordering = ["-published_at"]


# Router REST
router = routers.DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="api-article")

@api_view(["GET"])
def gallery_images(request):
    """API publique : retourne la liste des images de la galerie."""
    images = GalleryImage.objects.all()
    data = [
        {
            "id": img.id,
            "url": request.build_absolute_uri(img.image.url),
            "caption": img.caption,
            "category": img.category,
            "category_label": img.get_category_display(),
        }
        for img in images
    ]
    return Response(data)


urlpatterns = [
    path("", include(router.urls)),
    path("gallery/", gallery_images, name="api-gallery"),
]
