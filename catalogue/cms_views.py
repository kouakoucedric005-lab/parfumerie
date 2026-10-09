"""Vues du système de gestion de contenu (CMS) de la Parfumerie."""
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CollectionForm, ParfumForm, VarianteForm
from .models import Collection, Parfum, Variante


def cms_dashboard(request):
    """Tableau de bord principal du CMS."""
    total_parfums = Parfum.objects.count()
    total_actifs = Parfum.objects.filter(actif=True).count()
    total_collections = Collection.objects.count()
    total_marques = Parfum.objects.values("marque").distinct().count()
    
    ruptures = Variante.objects.filter(stock=0).select_related("parfum")[:5]
    derniers_parfums = Parfum.objects.order_by("-cree_le")[:6]

    context = {
        "total_parfums": total_parfums,
        "total_actifs": total_actifs,
        "total_collections": total_collections,
        "total_marques": total_marques,
        "ruptures": ruptures,
        "derniers_parfums": derniers_parfums,
    }
    return render(request, "cms/dashboard.html", context)


def cms_parfum_liste(request):
    """Liste complète des parfums dans le CMS avec recherche."""
    q = request.GET.get("q", "").strip()
    parfums = Parfum.objects.annotate(nb_variantes=Count("variantes")).order_by("-cree_le")

    if q:
        parfums = parfums.filter(
            Q(nom__icontains=q) | Q(marque__icontains=q) | Q(description__icontains=q)
        )

    return render(request, "cms/parfum_liste.html", {"parfums": parfums, "q": q})


def cms_parfum_ajouter(request):
    """Création d'un nouveau parfum via le CMS."""
    if request.method == "POST":
        form = ParfumForm(request.POST, request.FILES)
        if form.is_valid():
            parfum = form.save()
            Variante.objects.create(parfum=parfum, contenance_ml=50, prix=240.00, stock=10)
            Variante.objects.create(parfum=parfum, contenance_ml=100, prix=360.00, stock=5)
            
            messages.success(request, f"Le parfum « {parfum.nom} » a été ajouté au catalogue !")
            return redirect("catalogue:cms_parfum_image", pk=parfum.pk)
    else:
        form = ParfumForm()

    return render(request, "cms/parfum_form.html", {"form": form, "titre_page": "Ajouter un Parfum"})


def cms_parfum_editer(request, pk):
    """Édition d'un parfum existant et de ses variantes de prix/stock."""
    parfum = get_object_or_404(Parfum, pk=pk)

    if request.method == "POST":
        if "action_variante" in request.POST:
            v_form = VarianteForm(request.POST)
            if v_form.is_valid():
                var = v_form.save(commit=False)
                var.parfum = parfum
                var.save()
                messages.success(request, f"Contenance {var.contenance_ml} ml ajoutée !")
                return redirect("catalogue:cms_parfum_editer", pk=parfum.pk)
        else:
            form = ParfumForm(request.POST, request.FILES, instance=parfum)
            if form.is_valid():
                form.save()
                messages.success(request, f"Le parfum « {parfum.nom} » a été mis à jour !")
                return redirect("catalogue:cms_parfum_liste")
    else:
        form = ParfumForm(instance=parfum)

    variante_form = VarianteForm()
    variantes = parfum.variantes.all()

    return render(
        request,
        "cms/parfum_form.html",
        {
            "form": form,
            "parfum": parfum,
            "variantes": variantes,
            "variante_form": variante_form,
            "titre_page": f"Éditer {parfum.nom}",
        },
    )


def cms_parfum_image(request, pk):
    """Page simplifiée dédiée uniquement au changement d'image d'un parfum."""
    parfum = get_object_or_404(Parfum, pk=pk)

    if request.method == "POST":
        if "image" in request.FILES:
            parfum.image = request.FILES["image"]
            parfum.save()
            messages.success(request, f"Image de « {parfum.nom} » mise à jour avec succès !")
            return redirect("catalogue:cms_parfum_liste")
        else:
            messages.error(request, "Veuillez sélectionner une image valide sur votre appareil.")

    return render(request, "cms/parfum_image.html", {"parfum": parfum})


def cms_parfum_supprimer(request, pk):
    """Suppression d'un parfum du CMS."""
    parfum = get_object_or_404(Parfum, pk=pk)
    if request.method == "POST":
        nom = parfum.nom
        parfum.delete()
        messages.success(request, f"Le parfum « {nom} » a été supprimé.")
        return redirect("catalogue:cms_parfum_liste")

    return render(request, "cms/parfum_confirm_delete.html", {"parfum": parfum})


def cms_collections(request):
    """Gestion des collections du site."""
    collections = Collection.objects.annotate(nb_parfums=Count("parfums"))
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            col = form.save()
            messages.success(request, f"La collection « {col.nom} » a été créée !")
            return redirect("catalogue:cms_collections")
    else:
        form = CollectionForm()

    return render(request, "cms/collections.html", {"collections": collections, "form": form})
