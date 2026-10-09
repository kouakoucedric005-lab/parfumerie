from django.conf import settings


def site(request):
    """Rend le nom du site, la devise et la quantité max disponibles dans tous les gabarits."""
    return {
        "NOM_SITE": settings.NOM_SITE,
        "DEVISE": settings.DEVISE,
        "QUANTITE_MAX": settings.QUANTITE_MAX_PANIER,
    }
