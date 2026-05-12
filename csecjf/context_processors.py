"""
Context processors disponibles dans tous les templates.
"""

from django.conf import settings


def site_settings(request):
    """Injecte les paramètres généraux du site dans tous les contextes."""
    return {
        "SITE_NAME": "CSECJF Guinaw Rails Sud",
        "SITE_DESCRIPTION": "Centre Socio-Educatif et Culturel des Jeunes et des Femmes",
        "DEBUG": settings.DEBUG,
    }
