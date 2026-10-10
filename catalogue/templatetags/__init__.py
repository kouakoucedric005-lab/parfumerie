"""Template tags personnalisés pour la parfumerie."""
from django import template

register = template.Library()


@register.simple_tag
def image_src(parfum):
    """
    Retourne l'URL de l'image d'un parfum dans cet ordre de priorité :
    1. Fichier uploadé localement (si le fichier existe vraiment)
    2. URL externe (image_url)
    3. Chaîne vide (le template affiche alors le placeholder)
    """
    # Priorité 1 : fichier uploadé ET existant physiquement
    if parfum.image:
        try:
            # Vérifie que le fichier existe réellement (évite les erreurs sur Render)
            parfum.image.file  # lève ValueError si manquant
            return parfum.image.url
        except (ValueError, FileNotFoundError, OSError):
            pass

    # Priorité 2 : URL externe (Unsplash, CDN, etc.)
    if parfum.image_url:
        return parfum.image_url

    return ""
