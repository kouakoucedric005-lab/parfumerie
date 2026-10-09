from .panier import Panier


def panier(request):
    """Nombre d'articles du panier, affiché à côté de l'icône dans l'en-tête."""
    return {"panier_nb": len(Panier(request))}
