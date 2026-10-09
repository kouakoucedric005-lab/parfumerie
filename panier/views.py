from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from catalogue.models import Variante

from .forms import AjoutPanierForm, ModifierPanierForm, RetirerPanierForm
from .panier import Panier


def _retour(request, defaut):
    """Revient à la page d'origine (champ « next ») si elle appartient bien à ce site."""
    cible = request.POST.get("next", "")
    if cible and url_has_allowed_host_and_scheme(
        cible,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(cible)
    return redirect(defaut)


def detail(request):
    return render(request, "panier/detail.html", {"panier": Panier(request)})


@require_POST
def ajouter(request):
    formulaire = AjoutPanierForm(request.POST)
    if not formulaire.is_valid():
        messages.error(request, "Choisissez une contenance et une quantité valides.")
        return _retour(request, reverse("catalogue:liste"))

    variante = get_object_or_404(
        Variante.objects.select_related("parfum"),
        pk=formulaire.cleaned_data["variante"],
        parfum__actif=True,
    )
    nom = f"{variante.parfum.nom} ({variante.contenance_ml} ml)"
    if variante.stock < 1:
        messages.error(request, f"{nom} est actuellement épuisé.")
        return _retour(request, reverse("catalogue:detail", args=[variante.parfum.slug]))

    panier = Panier(request)
    demandee = formulaire.cleaned_data["quantite"]
    avant = panier.quantite_de(variante)
    panier.ajouter(variante, demandee)
    ajoutee = panier.quantite_de(variante) - avant

    if ajoutee > 0:
        messages.success(request, f"{nom} a été ajouté au panier.")
    if ajoutee < demandee:
        messages.warning(
            request,
            f"Quantité limitée à {panier.quantite_de(variante)} pour {nom} "
            "(stock ou maximum par commande).",
        )
    return _retour(request, reverse("panier:detail"))


@require_POST
def modifier(request):
    formulaire = ModifierPanierForm(request.POST)
    if formulaire.is_valid():
        variante = get_object_or_404(Variante, pk=formulaire.cleaned_data["variante"])
        Panier(request).definir(variante, formulaire.cleaned_data["quantite"])
    else:
        messages.error(request, "Quantité invalide.")
    return redirect("panier:detail")


@require_POST
def retirer(request):
    formulaire = RetirerPanierForm(request.POST)
    if formulaire.is_valid():
        variante = get_object_or_404(Variante, pk=formulaire.cleaned_data["variante"])
        Panier(request).retirer(variante)
        messages.success(request, "L'article a été retiré du panier.")
    return redirect("panier:detail")
