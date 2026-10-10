"""Remplace l'ensemble des parfums de démonstration par les jus d'exception des plus grandes Collections Privées (Dior, Tom Ford, Chanel, YSL, Guerlain, Armani).

Usage : python manage.py charger_demo
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from catalogue.models import Collection, Concentration, Famille, Genre, Parfum, Variante

COLLECTIONS_PRIVEE = [
    ("Collection Privée Dior", "Élixir et jus emblématiques de la Haute Parfumerie Christian Dior.", 1),
    ("Tom Ford Private Blend", "Laboratoire olfactif privé de Tom Ford pour passionnés de parfum.", 2),
    ("Les Exclusifs de Chanel", "Créations rares inspirées de l'histoire et des lieux de Mademoiselle Chanel.", 3),
    ("Le Vestiaire YSL", "Interprétations olfactives des pièces iconiques de la maison Yves Saint Laurent.", 4),
    ("Haute Parfumerie Rare", "Extraits précieux et nectars rares des plus grands parfumeurs.", 5),
]

# Images Unsplash libres de droits — parfums de luxe
PARFUMS_PRIVEE = [
    # (nom, marque, famille, genre, concentration, (notes_tete, notes_coeur, notes_fond), description, nouveau, meilleure_vente, collection_nom, prix_50, image_url)
    (
        "Gris Dior", "Dior Collection Privée", Famille.FLORAL, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("bergamote, pamplemousse", "rose de mai, jasmin, ylang-ylang", "patchouli, mousse de chêne, ambre, cèdre"),
        "Un chypre emblématique et audacieux, traduction olfactive du gris historique de la maison Dior.",
        True, True, "Collection Privée Dior", "240.00",
        "https://images.unsplash.com/photo-1541643600914-78b084683702?w=600&q=80"
    ),
    (
        "Bois d'Argent", "Dior Collection Privée", Famille.BOISE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("encens, baie de genièvre", "iris de florence, myrrhe", "miel, cuir, vanille, ambre"),
        "Un sillage poudré et boisé devenu culte, où l'iris précieux rencontre un encens mystique.",
        False, True, "Collection Privée Dior", "240.00",
        "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=600&q=80"
    ),
    (
        "Tobacolor", "Dior Collection Privée", Famille.AMBRE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("feuilles de tabac, agrumes", "miel, fruits secs, pêche", "tabac blond, vanille, ambre fumé"),
        "Un oriental tabacé et gourmand, véritable symphonie de tabacs blonds et d'orient.",
        True, False, "Collection Privée Dior", "250.00",
        "https://images.unsplash.com/photo-1588514912908-53b8e1bf3c74?w=600&q=80"
    ),
    (
        "Oud Wood", "Tom Ford Private Blend", Famille.BOISE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("bois de rose, cardamome, poivre de sichuan", "bois d'oud précieux, santal, vétiver", "fève tonka, vanille, ambre"),
        "L'un des ingrédients les plus rares et précieux de la parfumerie, sublimé dans un accord boisé fumé.",
        False, True, "Tom Ford Private Blend", "280.00",
        "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=600&q=80"
    ),
    (
        "Tobacco Vanille", "Tom Ford Private Blend", Famille.AMBRE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("feuille de tabac, épices douces", "vanille, cacao, fleur de tabac, fève tonka", "fruits secs, notes boisées"),
        "Une réinvention moderne d'un club de gentlemen anglais, opulent et chaleureux.",
        True, True, "Tom Ford Private Blend", "280.00",
        "https://images.unsplash.com/photo-1575995872537-3793d29d972c?w=600&q=80"
    ),
    (
        "Lost Cherry", "Tom Ford Private Blend", Famille.GOURMAND, Genre.FEMME, Concentration.EXTRAIT,
        ("cerise noire, liqueur de griotte, amande amère", "griotte, rose de turquie, jasmin sambac", "baume du pérou, fève tonka, santal, vétiver"),
        "Un voyage interdit au cœur d'une cerise juteuse croquante enrobée de liqueur suave.",
        True, True, "Tom Ford Private Blend", "320.00",
        "https://images.unsplash.com/photo-1615634260167-c8cdede054de?w=600&q=80"
    ),
    (
        "Tuxedo", "YSL Le Vestiaire", Famille.AMBRE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("feuille de violette, bergamote, coriandre", "rose, poivre noir, muguet", "patchouli, ambre gris, bourbon vanille"),
        "L'élégance impertinente du smoking noir YSL incarnée par un patchouli sombre embrasé d'épices.",
        True, True, "Le Vestiaire YSL", "260.00",
        "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=600&q=80"
    ),
    (
        "Babycat", "YSL Le Vestiaire", Famille.AMBRE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("poivre noir, poivre rose, élémi", "encens, safran", "bourbon vanille, daim, cèdre"),
        "Un accord vanille-cuir sulfureux et enveloppant, sillage couture de la maison Saint Laurent.",
        True, True, "Le Vestiaire YSL", "275.00",
        "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=600&q=80"
    ),
    (
        "Coromandel", "Chanel Les Exclusifs", Famille.AMBRE, Genre.FEMME, Concentration.EAU_DE_PARFUM,
        ("agrumes, néroli, orange amère", "jasmin, rose, patchouli, iris", "benjoin, encens, vanille, ambre"),
        "Inspiré des paravents de laque asiatiques de Gabrielle Chanel : un oriental intense et envoûtant.",
        False, True, "Les Exclusifs de Chanel", "290.00",
        "https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=600&q=80"
    ),
    (
        "Sycomore", "Chanel Les Exclusifs", Famille.BOISE, Genre.MIXTE, Concentration.EAU_DE_PARFUM,
        ("baie de genièvre, cyprès", "vétiver de haïti, poivre rose", "santal, tabac, violette"),
        "Un grand boisé sculpté autour du vétiver noble, évoquant l'élégance de l'automne.",
        False, False, "Les Exclusifs de Chanel", "290.00",
        "https://images.unsplash.com/photo-1596178065887-1198b6148b2b?w=600&q=80"
    ),
    (
        "Spiriteuse Double Vanille", "Guerlain L'Art et la Matière", Famille.GOURMAND, Genre.FEMME, Concentration.EXTRAIT,
        ("baie rose, bergamote, encens", "ylang-ylang, cèdre, rose", "vanille de madagascar, benjoin, rhum"),
        "L'or noir de la parfumerie magnifié par Guerlain : une vanille ambrée d'une sensualité absolue.",
        True, True, "Haute Parfumerie Rare", "310.00",
        "https://images.unsplash.com/photo-1600612253971-46d75b937f8e?w=600&q=80"
    ),
    (
        "Rose d'Arabie", "Armani Privé", Famille.AMBRE, Genre.MIXTE, Concentration.EXTRAIT,
        ("safran, cardamome", "rose de damas, patchouli", "bois d'oud, ambre, vanille"),
        "Une ode majestueuse à la rose d'orient enluminée par l'or liquide de l'oud.",
        False, True, "Haute Parfumerie Rare", "295.00",
        "https://images.unsplash.com/photo-1585386959984-a4155224a1ad?w=600&q=80"
    ),
]

CONTENANCES_PRIVEE = {
    50: (Decimal("1.0"), 12),
    100: (Decimal("1.55"), 8),
    250: (Decimal("2.8"), 3),
}


class Command(BaseCommand):
    help = "Supprime les parfums de démo et les remplace par la Collection Privée."

    def handle(self, *args, **options):
        # 1. Nettoyage des anciens parfums 'Démo'
        anciennes_demos = Parfum.objects.filter(marque__icontains="démo")
        nb_suppr = anciennes_demos.count()
        anciennes_demos.delete()
        if nb_suppr > 0:
            self.stdout.write(self.style.WARNING(f"Supprimé {nb_suppr} anciens parfums de démo."))

        # Nettoyage des anciennes collections fictives inutilisées
        Collection.objects.filter(nom__in=["Signatures", "Fraîcheurs"]).delete()

        # 2. Enregistrement des Collections Privées
        collections_dict = {}
        for nom, description, ordre in COLLECTIONS_PRIVEE:
            col, _ = Collection.objects.get_or_create(
                nom=nom, defaults={"description": description, "ordre": ordre}
            )
            collections_dict[nom] = col

        # 3. Enregistrement des Jus de Collection Privée
        for (
            nom, marque, famille, genre, concentration, notes, description,
            nouveau, meilleure_vente, collection_nom, prix_50, image_url
        ) in PARFUMS_PRIVEE:
            parfum, cree = Parfum.objects.update_or_create(
                nom=nom,
                marque=marque,
                defaults={
                    "famille": famille,
                    "genre": genre,
                    "concentration": concentration,
                    "notes_tete": notes[0],
                    "notes_coeur": notes[1],
                    "notes_fond": notes[2],
                    "description": description,
                    "nouveau": nouveau,
                    "meilleure_vente": meilleure_vente,
                    "collection": collections_dict.get(collection_nom),
                    "image": "",          # Pas de fichier local
                    "image_url": image_url,  # URL externe Unsplash
                    "actif": True,
                },
            )

            # Contenances de Collection Privée (50ml, 100ml, 250ml Flacon d'Exception)
            for ml, (coefficient, stock) in CONTENANCES_PRIVEE.items():
                prix = (Decimal(prix_50) * coefficient).quantize(Decimal("1.00"))
                Variante.objects.get_or_create(
                    parfum=parfum,
                    contenance_ml=ml,
                    defaults={"prix": prix, "stock": stock},
                )

            self.stdout.write(f"{'Créé' if cree else 'Mis à jour'} : {parfum.nom} ({parfum.marque})")

        self.stdout.write(self.style.SUCCESS("Catalogue de Collection Privée chargé avec succès !"))
