from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Concentration, Famille, Genre, Parfum, Variante


def creer_parfum(nom="Test", prix="80.00", stock=5, **champs):
    """Crée un parfum avec une contenance de 50 ml."""
    donnees = {
        "marque": "Marque",
        "famille": Famille.FLORAL,
        "genre": Genre.FEMME,
        "concentration": Concentration.EAU_DE_PARFUM,
    }
    donnees.update(champs)
    parfum = Parfum.objects.create(nom=nom, **donnees)
    Variante.objects.create(
        parfum=parfum, contenance_ml=50, prix=Decimal(prix), stock=stock
    )
    return parfum


class ModelesTests(TestCase):
    def test_le_slug_est_genere_et_reste_unique(self):
        premier = creer_parfum("Nuit d'Ambre")
        second = creer_parfum("Nuit d'Ambre")
        self.assertEqual(premier.slug, "nuit-dambre")
        self.assertEqual(second.slug, "nuit-dambre-2")

    def test_les_notes_sont_decoupees(self):
        parfum = creer_parfum(notes_tete="citron, menthe ,")
        self.assertEqual(parfum.notes_tete_liste, ["citron", "menthe"])

    def test_variante_par_defaut_ignore_les_ruptures(self):
        parfum = creer_parfum(stock=0)
        grande = Variante.objects.create(
            parfum=parfum, contenance_ml=100, prix=Decimal("120"), stock=3
        )
        self.assertEqual(parfum.variante_par_defaut, grande)


class PagesTests(TestCase):
    def test_accueil(self):
        creer_parfum(nouveau=True)
        reponse = self.client.get(reverse("catalogue:accueil"))
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Nouveautés")

    def test_liste_affiche_seulement_les_parfums_actifs(self):
        creer_parfum("Visible")
        creer_parfum("Masque", actif=False)
        reponse = self.client.get(reverse("catalogue:liste"))
        self.assertContains(reponse, "Visible")
        self.assertNotContains(reponse, "Masque")

    def test_filtre_par_genre(self):
        creer_parfum("Pour elle", genre=Genre.FEMME)
        creer_parfum("Pour lui", genre=Genre.HOMME)
        reponse = self.client.get(reverse("catalogue:liste"), {"genre": "homme"})
        self.assertContains(reponse, "Pour lui")
        self.assertNotContains(reponse, "Pour elle")

    def test_filtre_par_prix_maximum(self):
        creer_parfum("Abordable", prix="50")
        creer_parfum("Precieux", prix="200")
        reponse = self.client.get(reverse("catalogue:liste"), {"prix_max": "100"})
        self.assertContains(reponse, "Abordable")
        self.assertNotContains(reponse, "Precieux")

    def test_recherche_par_note(self):
        creer_parfum("Vanille", notes_fond="vanille")
        creer_parfum("Citronne", notes_tete="citron")
        reponse = self.client.get(reverse("catalogue:liste"), {"q": "vanille"})
        self.assertContains(reponse, "Vanille")
        self.assertNotContains(reponse, "Citronne")

    def test_aucun_resultat(self):
        reponse = self.client.get(reverse("catalogue:liste"), {"q": "introuvable"})
        self.assertContains(reponse, "Aucun parfum ne correspond")

    def test_valeurs_de_filtre_invalides_sont_ignorees(self):
        creer_parfum("Test")
        reponse = self.client.get(
            reverse("catalogue:liste"),
            {"genre": "nimporte", "prix_max": "abc", "contenance": "x", "tri": "zzz"},
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Test")

    def test_fiche_produit(self):
        parfum = creer_parfum("Fiche", notes_coeur="rose")
        reponse = self.client.get(parfum.get_absolute_url())
        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, "Pyramide olfactive")

    def test_fiche_d_un_parfum_masque_renvoie_404(self):
        parfum = creer_parfum("Cache", actif=False)
        reponse = self.client.get(parfum.get_absolute_url())
        self.assertEqual(reponse.status_code, 404)
