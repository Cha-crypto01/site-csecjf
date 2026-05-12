"""
URLs de gestion des articles et de la galerie dans l'interface d'administration.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_list, name="article_list"),
    path("create/", views.article_create, name="article_create"),
    path("<int:article_id>/edit/", views.article_edit, name="article_edit"),
    path("<int:article_id>/delete/", views.article_delete, name="article_delete"),
    path(
        "<int:article_id>/restore/",
        views.article_restore,
        name="article_restore",
    ),
    path("galerie/", views.gallery_list, name="gallery_list"),
    path("galerie/add/", views.gallery_add, name="gallery_add"),
    path(
        "galerie/<int:pk>/delete/",
        views.gallery_delete,
        name="gallery_delete",
    ),
]
