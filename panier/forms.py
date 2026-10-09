from django import forms

from .panier import QUANTITE_MAX


class AjoutPanierForm(forms.Form):
    variante = forms.IntegerField(min_value=1)
    quantite = forms.IntegerField(min_value=1, max_value=QUANTITE_MAX, initial=1)


class ModifierPanierForm(forms.Form):
    variante = forms.IntegerField(min_value=1)
    quantite = forms.IntegerField(min_value=0, max_value=QUANTITE_MAX)


class RetirerPanierForm(forms.Form):
    variante = forms.IntegerField(min_value=1)
