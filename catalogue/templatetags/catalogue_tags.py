"""Template tags personnalisés pour la parfumerie."""
from django import template

register = template.Library()


@register.simple_tag
def image_src(parfum):
    """
    Retourne l'URL de l'image d'un parfum dans cet ordre de priorité :
    1. Fichier uploadé localement (si le fichier existe vraiment sur le disque)
    2. URL externe (image_url — Unsplash, CDN, etc.)
    3. Chaîne vide → le template affiche le placeholder texte
    """
    # Priorité 1 : fichier uploadé ET existant physiquement sur le serveur
    if parfum.image:
        try:
            parfum.image.file  # lève une exception si le fichier est absent
            return parfum.image.url
        except (ValueError, FileNotFoundError, OSError):
            pass  # Fichier absent (cas Render filesystem éphémère)

    # Priorité 2 : URL externe stockée dans la base de données
    if parfum.image_url:
        return parfum.image_url

    # Aucune image disponible
    return ""
