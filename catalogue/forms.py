"""Formulaires pour la gestion des parfums, collections et contenances dans le CMS."""
from django import forms
from .models import Collection, Parfum, Variante


class ParfumForm(forms.ModelForm):
    """Formulaire complet de création et d'édition d'un parfum."""

    class Meta:
        model = Parfum
        fields = [
            "nom",
            "marque",
            "famille",
            "genre",
            "concentration",
            "collection",
            "description",
            "notes_tete",
            "notes_coeur",
            "notes_fond",
            "image",
            "nouveau",
            "meilleure_vente",
            "actif",
        ]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: Bleu de Chanel"}),
            "marque": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: Chanel"}),
            "famille": forms.Select(attrs={"class": "champ-select"}),
            "genre": forms.Select(attrs={"class": "champ-select"}),
            "concentration": forms.Select(attrs={"class": "champ-select"}),
            "collection": forms.Select(attrs={"class": "champ-select"}),
            "description": forms.Textarea(attrs={"class": "champ-textarea", "rows": 4, "placeholder": "Description détaillée de la fragrance..."}),
            "notes_tete": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: bergamote, citron, menthe"}),
            "notes_coeur": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: jasmin, poivre, gingembre"}),
            "notes_fond": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: cèdre, santal, ambre"}),
            "image": forms.FileInput(attrs={"class": "champ-file"}),
            "nouveau": forms.CheckboxInput(attrs={"class": "champ-checkbox"}),
            "meilleure_vente": forms.CheckboxInput(attrs={"class": "champ-checkbox"}),
            "actif": forms.CheckboxInput(attrs={"class": "champ-checkbox"}),
        }


class VarianteForm(forms.ModelForm):
    """Formulaire d'ajout/modification d'une contenance (variante)."""

    class Meta:
        model = Variante
        fields = ["contenance_ml", "prix", "stock"]
        widgets = {
            "contenance_ml": forms.NumberInput(attrs={"class": "champ-input", "placeholder": "50"}),
            "prix": forms.NumberInput(attrs={"class": "champ-input", "step": "0.50", "placeholder": "89.00"}),
            "stock": forms.NumberInput(attrs={"class": "champ-input", "placeholder": "10"}),
        }


class CollectionForm(forms.ModelForm):
    """Formulaire de gestion des collections."""

    class Meta:
        model = Collection
        fields = ["nom", "description", "ordre"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "champ-input", "placeholder": "ex: Haute Parfumerie"}),
            "description": forms.Textarea(attrs={"class": "champ-textarea", "rows": 3}),
            "ordre": forms.NumberInput(attrs={"class": "champ-input"}),
        }
