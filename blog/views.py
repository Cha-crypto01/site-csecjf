"""
Vues CRUD complètes pour la gestion des articles (blog).

Chaque action est tracée dans AuditLog.
Respecte les permissions selon le rôle.
"""
import django.db.models as models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Article, AuditLog, GalleryImage
from .forms import ArticleForm
from users.decorators import admin_required, super_admin_required


def galerie(request):
    """Page publique de la galerie photo."""
    images = GalleryImage.objects.all()
    return render(request, "galerie.html", {"gallery_images": images})


@login_required
@admin_required
def gallery_list(request):
    """Liste des images de la galerie dans l'admin."""
    images = GalleryImage.objects.all()
    return render(request, "admin/gallery_list.html", {"images": images})


@login_required
@admin_required
def gallery_add(request):
    """Ajout d'une image à la galerie."""
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption", "").strip()
        category = request.POST.get("category", "activites")
        try:
            order = int(request.POST.get("order", 0))
        except (ValueError, TypeError):
            order = 0

        if not image:
            messages.error(request, "Veuillez sélectionner une image sur votre ordinateur.")
        elif not image.content_type.startswith("image/"):
            messages.error(request, "Le fichier sélectionné n'est pas une image valide.")
        else:
            try:
                GalleryImage.objects.create(
                    image=image,
                    caption=caption,
                    category=category,
                    order=order,
                )
                messages.success(request, f"Image « {caption or image.name} » ajoutée avec succès.")
                return redirect("gallery_list")
            except Exception as e:
                messages.error(request, f"Erreur lors de l'ajout : {e}")

    return render(request, "admin/gallery_form.html")


@login_required
@admin_required
def gallery_delete(request, pk):
    """Suppression d'une image de la galerie."""
    img = get_object_or_404(GalleryImage, pk=pk)

    if request.method == "POST":
        img.delete()
        messages.success(request, "Image supprimée de la galerie.")
        return redirect("gallery_list")

    return render(request, "admin/gallery_confirm_delete.html", {"image": img})


@login_required
@admin_required
def article_list(request):
    """
    Liste des articles (non supprimés).
    - Super Admin : voit tous les articles
    - Admin : voit ses articles + les articles publiés
    - Rédacteur : voit uniquement ses brouillons
    """
    if request.user.is_super_admin():
        articles = Article.objects.filter(is_deleted=False)
    elif request.user.is_admin():
        articles = Article.objects.filter(
            is_deleted=False
        ).filter(
            # Ses propres articles ou les articles publiés
            models.Q(author=request.user) | models.Q(status="publie")
        )
    else:
        # Rédacteur : uniquement ses brouillons
        articles = Article.objects.filter(
            is_deleted=False,
            author=request.user,
            status="brouillon",
        )

    articles = articles.select_related("author", "last_modified_by").order_by(
        "-created_at"
    )

    # Filtres
    status_filter = request.GET.get("status", "")
    category_filter = request.GET.get("category", "")

    if status_filter:
        articles = articles.filter(status=status_filter)
    if category_filter:
        articles = articles.filter(category=category_filter)

    paginator = Paginator(articles, 20)
    page = request.GET.get("page", 1)
    articles_page = paginator.get_page(page)

    deleted_articles = []
    if request.user.is_super_admin():
        deleted_articles = Article.objects.filter(is_deleted=True).order_by("-deleted_at")

    context = {
        "articles": articles_page,
        "current_status": status_filter,
        "current_category": category_filter,
        "deleted_articles": deleted_articles,
    }
    return render(request, "admin/article_list.html", context)


@login_required
@admin_required
def article_create(request):
    """
    Création d'un nouvel article.
    - Admin / Super Admin : peut publier directement
    - (Accès refusé aux rédacteurs via le décorateur)
    """
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            # Si l'utilisateur n'est pas admin, force le statut brouillon
            if not request.user.is_admin():
                article.status = "brouillon"

            article.save()

            # Trace la création
            AuditLog.objects.create(
                user=request.user,
                article=article,
                action="publish" if article.status == "publie" else "create",
                details=f"Article créé par {request.user.username} "
                f"avec le statut '{article.status}'",
            )

            messages.success(
                request,
                f"L'article « {article.title} » a été "
                f"{'publié' if article.status == 'publie' else 'enregistré comme brouillon'}.",
            )
            return redirect("article_list")
        else:
            messages.error(
                request,
                "Erreur lors de la validation du formulaire. Veuillez corriger les champs.",
            )
    else:
        form = ArticleForm()

    return render(
        request,
        "admin/article_form.html",
        {"form": form, "editing": False},
    )


@login_required
@admin_required
def article_edit(request, article_id):
    """
    Modification d'un article existant.
    - Super Admin : peut modifier tout article
    - Admin : peut modifier ses articles uniquement
    """
    article = get_object_or_404(Article, id=article_id, is_deleted=False)

    # Vérification des permissions
    if not request.user.is_super_admin() and article.author != request.user:
        messages.error(
            request,
            "Vous ne pouvez modifier que vos propres articles.",
        )
        return redirect("article_list")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            old_status = article.status
            updated = form.save(commit=False)
            updated.last_modified_by = request.user
            updated.save()

            # Détermine l'action
            if old_status != updated.status and updated.status == "publie":
                action = "publish"
            elif old_status != updated.status and updated.status == "brouillon":
                action = "unpublish"
            else:
                action = "update"

            AuditLog.objects.create(
                user=request.user,
                article=article,
                action=action,
                details=f"Article modifié par {request.user.username} "
                f"(statut: {old_status} → {updated.status})",
            )

            messages.success(
                request,
                f"L'article « {article.title} » a été modifié avec succès.",
            )
            return redirect("article_list")
        else:
            messages.error(request, "Erreur lors de la modification.")
    else:
        form = ArticleForm(instance=article)

    return render(
        request,
        "admin/article_form.html",
        {"form": form, "editing": True, "article": article},
    )


@login_required
def article_delete(request, article_id):
    """
    Suppression logique (soft delete) d'un article.
    - Super Admin : peut supprimer n'importe quel article
    - Admin : peut supprimer ses propres articles uniquement
    """
    article = get_object_or_404(Article, id=article_id, is_deleted=False)

    if not request.user.is_super_admin() and article.author != request.user:
        messages.error(
            request,
            "Vous ne pouvez supprimer que vos propres articles.",
        )
        return redirect("article_list")

    if request.method == "POST":
        article.soft_delete(request.user)
        messages.success(
            request,
            f"L'article « {article.title} » a été supprimé.",
        )
        return redirect("article_list")

    return render(
        request,
        "admin/article_confirm_delete.html",
        {"article": article},
    )


@login_required
@super_admin_required
def article_restore(request, article_id):
    """
    Restauration d'un article supprimé (Super Admin uniquement).
    """
    article = get_object_or_404(Article, id=article_id, is_deleted=True)

    if request.method == "POST":
        article.is_deleted = False
        article.deleted_by = None
        article.deleted_at = None
        article.save()

        AuditLog.objects.create(
            user=request.user,
            article=article,
            action="update",
            details=f"Article restauré par {request.user.username}",
        )

        messages.success(
            request,
            f"L'article « {article.title} » a été restauré.",
        )
        return redirect("article_list")

    return render(
        request,
        "admin/article_restore.html",
        {"article": article},
    )

