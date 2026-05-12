"""
Formulaires de gestion des articles pour l'interface d'administration.
"""
from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """Formulaire complet pour créer et modifier un article."""

    class Meta:
        model = Article
        fields = [
            "title",
            "subtitle",
            "category",
            "content",
            "status",
            "images",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Titre de l'article",
                }
            ),
            "subtitle": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Sous-titre (optionnel)",
                }
            ),
            "category": forms.Select(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
            "content": forms.HiddenInput(),
            "images": forms.HiddenInput(),
        }

    def clean_images(self):
        images = self.cleaned_data.get("images")
        if not images or not isinstance(images, list):
            return []
        return images
