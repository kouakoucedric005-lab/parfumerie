"""Le panier, conservé dans la session du visiteur (aucune table en base).

La session contient {identifiant de contenance: quantité}. Les prix et les stocks
sont relus en base à chaque affichage : un prix modifié dans l'administration
s'applique tout de suite, et le client ne peut pas modifier un prix lui-même.
"""
from dataclasses import dataclass
from decimal import Decimal

from django.conf import settings

from catalogue.models import Variante

CLE_SESSION = "panier"
QUANTITE_MAX = settings.QUANTITE_MAX_PANIER


@dataclass(frozen=True)
class LignePanier:
    variante: Variante
    quantite: int

    @property
    def parfum(self):
        return self.variante.parfum

    @property
    def prix_unitaire(self):
        return self.variante.prix

    @property
    def total(self):
        return self.variante.prix * self.quantite


def _entier(valeur):
    try:
        return int(valeur)
    except (TypeError, ValueError):
        return 0


class Panier:
    def __init__(self, request):
        self.session = request.session
        donnees = self.session.get(CLE_SESSION)
        self.donnees = donnees if isinstance(donnees, dict) else {}
        self._lignes = None

    def _sauver(self):
        self.session[CLE_SESSION] = self.donnees
        self.session.modified = True
        self._lignes = None

    def quantite_de(self, variante):
        return _entier(self.donnees.get(str(variante.pk), 0))

    @staticmethod
    def _borner(variante, quantite):
        """Garde la quantité entre 0, le stock disponible et le maximum autorisé."""
        return max(0, min(quantite, QUANTITE_MAX, variante.stock))

    def definir(self, variante, quantite):
        quantite = self._borner(variante, quantite)
        cle = str(variante.pk)
        if quantite:
            self.donnees[cle] = quantite
        else:
            self.donnees.pop(cle, None)
        self._sauver()

    def ajouter(self, variante, quantite=1):
        self.definir(variante, self.quantite_de(variante) + quantite)

    def retirer(self, variante):
        self.definir(variante, 0)

    def vider(self):
        self.donnees = {}
        self._sauver()

    def lignes(self):
        """Lignes du panier, dans l'ordre d'ajout, avec prix et stock actuels."""
        if self._lignes is None:
            ordre = {str(cle): rang for rang, cle in enumerate(self.donnees)}
            identifiants = [int(cle) for cle in ordre if cle.isdigit()]
            variantes = Variante.objects.filter(
                pk__in=identifiants, parfum__actif=True
            ).select_related("parfum")
            lignes = []
            for variante in sorted(variantes, key=lambda v: ordre[str(v.pk)]):
                quantite = self._borner(variante, _entier(self.donnees[str(variante.pk)]))
                if quantite:
                    lignes.append(LignePanier(variante=variante, quantite=quantite))
            self._lignes = lignes
        return self._lignes

    @property
    def sous_total(self):
        return sum((ligne.total for ligne in self.lignes()), Decimal("0"))

    def __len__(self):
        """Nombre total d'articles (sans interroger la base de données)."""
        return sum(_entier(q) for q in self.donnees.values())
