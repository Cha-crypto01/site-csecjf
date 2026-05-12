from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    # Redirection de la racine vers la gestion
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("index.html", TemplateView.as_view(template_name="index.html")),
    # Pages publiques (accessibles directement par leur nom)
    path("about.html", TemplateView.as_view(template_name="about.html"), name="about"),
    path("services.html", TemplateView.as_view(template_name="services.html"), name="services"),
    path("achievements.html", TemplateView.as_view(template_name="achievements.html"), name="achievements"),
    path("contact.html", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("galerie.html", TemplateView.as_view(template_name="galerie.html"), name="galerie"),
    path("blog.html", TemplateView.as_view(template_name="blog.html"), name="blog"),
    path("admin.html", TemplateView.as_view(template_name="admin.html"), name="admin_legacy"),
    # Admin Django natif (réservé aux super admins)
    path("django-admin/", admin.site.urls),
    # Authentification
    path("", include("users.urls")),
    # Interface d'administration personnalisée (URL privée)
    path("gestion/", include("users.urls_admin")),
    # Gestion des articles (blog)
    path("gestion/blog/", include("blog.urls")),
    # API REST (pour le frontend existant)
    path("api/", include("blog.urls_api")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
