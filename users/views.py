"""
Vues d'authentification et de gestion des utilisateurs.
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.core.paginator import Paginator

from .models import User
from .forms import UserAdminForm
from .decorators import super_admin_required, admin_required
from blog.models import Article, AuditLog


# --- Dashboard ---

@login_required
@admin_required
def dashboard(request):
    """Tableau de bord principal de l'administration."""

    # Statistiques générales
    total_articles = Article.objects.filter(is_deleted=False).count()
    total_published = Article.objects.filter(is_deleted=False, status="publie").count()
    total_drafts = Article.objects.filter(is_deleted=False, status="brouillon").count()
    total_users = User.objects.filter(is_active=True).count()

    # Derniers articles publiés
    recent_articles = Article.objects.filter(
        is_deleted=False, status="publie"
    ).select_related("author").order_by("-published_at")[:5]

    # Activité récente (20 dernières actions)
    recent_activity = AuditLog.objects.select_related(
        "user", "article"
    ).order_by("-created_at")[:20]

    # Articles par catégorie
    articles_by_category = (
        Article.objects.filter(is_deleted=False)
        .values("category")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # Articles par auteur
    articles_by_author = (
        Article.objects.filter(is_deleted=False)
        .values("author__username")
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    context = {
        "total_articles": total_articles,
        "total_published": total_published,
        "total_drafts": total_drafts,
        "total_users": total_users,
        "recent_articles": recent_articles,
        "recent_activity": recent_activity,
        "articles_by_category": articles_by_category,
        "articles_by_author": articles_by_author,
    }
    return render(request, "admin/dashboard.html", context)


# --- Authentification ---

def login_view(request):
    """Page de connexion à l'interface d'administration."""
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Authentification par email uniquement
        user = None
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(
                request, username=user_obj.username, password=password
            )
        except User.DoesNotExist:
            user = None

        if user is not None and user.is_active:
            login(request, user)
            next_url = request.GET.get("next", "admin_dashboard")
            return redirect(next_url)
        else:
            messages.error(
                request,
                "Identifiants incorrects ou compte désactivé. Veuillez réessayer.",
            )

    return render(request, "users/login.html")


def logout_view(request):
    """Déconnexion sécurisée."""
    logout(request)
    return redirect("login")


# --- Gestion des utilisateurs (Super Admin uniquement) ---

@login_required
@super_admin_required
def user_list(request):
    """Liste de tous les utilisateurs avec leurs rôles."""
    users_list = User.objects.all().order_by("-date_joined")
    paginator = Paginator(users_list, 20)
    page = request.GET.get("page", 1)
    users = paginator.get_page(page)
    return render(request, "admin/user_list.html", {"users": users})


@login_required
@super_admin_required
def user_create(request):
    """Création d'un nouvel utilisateur."""
    if request.method == "POST":
        form = UserAdminForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"L'utilisateur {user.username} a été créé avec succès.",
            )
            return redirect("user_list")
    else:
        form = UserAdminForm()

    return render(request, "admin/user_form.html", {"form": form, "editing": False})


@login_required
@super_admin_required
def user_edit(request, user_id):
    """Modification d'un utilisateur existant."""
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserAdminForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"L'utilisateur {user.username} a été modifié.",
            )
            return redirect("user_list")
    else:
        form = UserAdminForm(instance=user)

    return render(
        request, "admin/user_form.html", {"form": form, "editing": True, "user_obj": user}
    )


@login_required
@super_admin_required
def user_delete(request, user_id):
    """Suppression (désactivation) d'un utilisateur."""
    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "Vous ne pouvez pas vous supprimer vous-même.")
        return redirect("user_list")

    if request.method == "POST":
        user.is_active = False
        user.save()
        messages.success(
            request,
            f"L'utilisateur {user.username} a été désactivé.",
        )
        return redirect("user_list")

    return render(request, "admin/user_confirm_delete.html", {"user_obj": user})
