from django.test import TestCase
from django.urls import reverse

from catalogue.tests import creer_parfum


class PanierTests(TestCase):
    def setUp(self):
        self.parfum = creer_parfum("Panier", prix="80.00", stock=5)
        self.variante = self.parfum.variantes.get()

    def ajouter(self, quantite=1, **extra):
        donnees = {"variante": self.variante.pk, "quantite": quantite}
        donnees.update(extra)
        return self.client.post(reverse("panier:ajouter"), donnees)

    def test_panier_vide_au_depart(self):
        reponse = self.client.get(reverse("panier:detail"))
        self.assertContains(reponse, "Votre panier est vide")

    def test_ajouter_un_article(self):
        reponse = self.ajouter(2)
        self.assertRedirects(reponse, reverse("panier:detail"))
        page = self.client.get(reverse("panier:detail"))
        self.assertContains(page, "160,00")  # 2 x 80,00 (format français)

    def test_la_quantite_est_limitee_au_stock(self):
        self.ajouter(5)
        self.ajouter(3)
        page = self.client.get(reverse("panier:detail"))
        self.assertContains(page, "400,00")  # 5 x 80,00, pas plus que le stock

    def test_article_epuise_refuse(self):
        self.variante.stock = 0
        self.variante.save()
        self.ajouter(1)
        page = self.client.get(reverse("panier:detail"))
        self.assertContains(page, "Votre panier est vide")

    def test_modifier_la_quantite(self):
        self.ajouter(1)
        self.client.post(
            reverse("panier:modifier"), {"variante": self.variante.pk, "quantite": 3}
        )
        page = self.client.get(reverse("panier:detail"))
        self.assertContains(page, "240,00")

    def test_retirer_un_article(self):
        self.ajouter(1)
        self.client.post(reverse("panier:retirer"), {"variante": self.variante.pk})
        page = self.client.get(reverse("panier:detail"))
        self.assertContains(page, "Votre panier est vide")

    def test_la_redirection_externe_est_refusee(self):
        reponse = self.ajouter(1, next="https://exemple.invalid/piege")
        self.assertRedirects(reponse, reverse("panier:detail"))

    def test_la_redirection_interne_est_acceptee(self):
        reponse = self.ajouter(1, next=reverse("catalogue:liste"))
        self.assertRedirects(reponse, reverse("catalogue:liste"))

    def test_ajouter_exige_une_requete_post(self):
        reponse = self.client.get(reverse("panier:ajouter"))
        self.assertEqual(reponse.status_code, 405)
