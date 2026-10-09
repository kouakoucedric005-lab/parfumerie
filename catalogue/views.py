from decimal import Decimal, InvalidOperation

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Collection, Famille, Genre, Parfum, Variante

PAR_PAGE = 12

# clé dans l'adresse -> (libellé affiché, ordre de tri)
TRIS = {
    "popularite": ("Popularité", ("-meilleure_vente", "-cree_le")),
    "nouveautes": ("Nouveautés", ("-cree_le",)),
    "prix_croissant": ("Prix croissant", ("prix_a_partir_de", "nom")),
    "prix_decroissant": ("Prix décroissant", ("-prix_a_partir_de", "nom")),
}
TRI_PAR_DEFAUT = "popularite"


def _parfums_visibles():
    return Parfum.objects.visibles().avec_prix().prefetch_related("variantes")


def accueil(request):
    base = _parfums_visibles()
    contexte = {
        "nouveautes": base.filter(nouveau=True)[:8],
        "meilleures_ventes": base.filter(meilleure_vente=True)[:8],
        "familles": Famille.choices,
        "collections": Collection.objects.all()[:3],
    }
    return render(request, "catalogue/accueil.html", contexte)


def liste(request):
    get = request.GET
    parfums = _parfums_visibles()

    filtres = {
        "genre": get.get("genre", ""),
        "famille": get.get("famille", ""),
        "marque": get.get("marque", ""),
        "collection": get.get("collection", ""),
        "contenance": get.get("contenance", ""),
        "prix_max": get.get("prix_max", "").strip(),
        "q": get.get("q", "").strip(),
        "tri": get.get("tri", TRI_PAR_DEFAUT),
    }

    if filtres["genre"] in Genre.values:
        parfums = parfums.filter(genre=filtres["genre"])
    else:
        filtres["genre"] = ""

    if filtres["famille"] in Famille.values:
        parfums = parfums.filter(famille=filtres["famille"])
    else:
        filtres["famille"] = ""

    if filtres["marque"]:
        parfums = parfums.filter(marque=filtres["marque"])

    if filtres["collection"]:
        parfums = parfums.filter(collection__slug=filtres["collection"])

    if filtres["contenance"].isdigit():
        parfums = parfums.filter(
            id__in=Variante.objects.filter(
                contenance_ml=int(filtres["contenance"])
            ).values("parfum_id")
        )
    else:
        filtres["contenance"] = ""

    if filtres["prix_max"]:
        try:
            parfums = parfums.filter(
                prix_a_partir_de__lte=Decimal(filtres["prix_max"].replace(",", "."))
            )
        except InvalidOperation:
            filtres["prix_max"] = ""

    if filtres["q"]:
        parfums = parfums.filter(
            Q(nom__icontains=filtres["q"])
            | Q(marque__icontains=filtres["q"])
            | Q(notes_tete__icontains=filtres["q"])
            | Q(notes_coeur__icontains=filtres["q"])
            | Q(notes_fond__icontains=filtres["q"])
        )

    if filtres["tri"] not in TRIS:
        filtres["tri"] = TRI_PAR_DEFAUT
    parfums = parfums.order_by(*TRIS[filtres["tri"]][1])

    paginator = Paginator(parfums, PAR_PAGE)
    page = paginator.get_page(get.get("page"))

    # Paramètres de l'adresse sans « page », pour les liens de pagination.
    autres_parametres = get.copy()
    autres_parametres.pop("page", None)

    filtres_actifs = any(
        valeur
        for cle, valeur in filtres.items()
        if cle != "tri"
    )

    contexte = {
        "page": page,
        "nb_resultats": paginator.count,
        "filtres": filtres,
        "filtres_actifs": filtres_actifs,
        "querystring": autres_parametres.urlencode(),
        "tris": [(cle, libelle) for cle, (libelle, _) in TRIS.items()],
        "genres": Genre.choices,
        "familles": Famille.choices,
        "marques": Parfum.objects.visibles()
        .order_by("marque")
        .values_list("marque", flat=True)
        .distinct(),
        "collections": Collection.objects.all(),
        "contenances": Variante.objects.filter(parfum__actif=True)
        .order_by("contenance_ml")
        .values_list("contenance_ml", flat=True)
        .distinct(),
    }
    return render(request, "catalogue/liste.html", contexte)


def detail(request, slug):
    parfum = get_object_or_404(
        Parfum.objects.visibles().prefetch_related("variantes", "images"), slug=slug
    )
    variantes = list(parfum.variantes.all())
    choisie = parfum.variante_par_defaut or (variantes[0] if variantes else None)
    similaires = (
        _parfums_visibles().filter(famille=parfum.famille).exclude(pk=parfum.pk)[:4]
    )
    contexte = {
        "parfum": parfum,
        "variantes": variantes,
        "choisie": choisie,
        "similaires": similaires,
    }
    return render(request, "catalogue/detail.html", contexte)
