"""
Décorateurs de permissions pour restreindre l'accès aux vues selon le rôle.
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(*roles):
    """
    Vérifie que l'utilisateur connecté possède l'un des rôles spécifiés.

    Utilisation :
        @role_required('super_admin', 'admin')
        def ma_vue(request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.role not in roles and not request.user.is_super_admin():
                raise PermissionDenied(
                    "Vous n'avez pas les permissions nécessaires."
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def super_admin_required(view_func):
    """Restreint l'accès aux Super Admins uniquement."""
    return role_required("super_admin")(view_func)


def admin_required(view_func):
    """Restreint l'accès aux Admins et Super Admins."""
    return role_required("super_admin", "admin")(view_func)
