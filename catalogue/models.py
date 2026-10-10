"""Modèles du catalogue : collections, parfums, contenances (variantes) et photos."""
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Min
from django.urls import reverse
from django.utils.text import slugify


class Famille(models.TextChoices):
    FLORAL = "floral", "Floral"
    BOISE = "boise", "Boisé"
    AMBRE = "ambre", "Ambré"
    FRAIS = "frais", "Frais"
    GOURMAND = "gourmand", "Gourmand"


class Genre(models.TextChoices):
    FEMME = "femme", "Femme"
    HOMME = "homme", "Homme"
    MIXTE = "mixte", "Mixte"


class Concentration(models.TextChoices):
    EAU_DE_TOILETTE = "eau_de_toilette", "Eau de toilette"
    EAU_DE_PARFUM = "eau_de_parfum", "Eau de parfum"
    EXTRAIT = "extrait", "Extrait de parfum"


def _slug_unique(modele, texte, pk=None):
    """Fabrique un slug à partir du texte, en ajoutant -2, -3... s'il existe déjà."""
    base = slugify(texte) or "parfum"
    slug, n = base, 2
    while modele.objects.filter(slug=slug).exclude(pk=pk).exists():
        slug = f"{base}-{n}"
        n += 1
    return slug


class Collection(models.Model):
    nom = models.CharField("nom", max_length=80)
    slug = models.SlugField("adresse", max_length=100, unique=True, blank=True)
    description = models.TextField("description", blank=True)
    image = models.ImageField("visuel", upload_to="collections/", blank=True)
    ordre = models.PositiveSmallIntegerField("ordre d'affichage", default=0)

    class Meta:
        ordering = ["ordre", "nom"]
        verbose_name = "collection"
        verbose_name_plural = "collections"

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _slug_unique(Collection, self.nom, self.pk)
        super().save(*args, **kwargs)


class ParfumQuerySet(models.QuerySet):
    def visibles(self):
        """Parfums affichés sur le site (case « actif » cochée)."""
        return self.filter(actif=True)

    def avec_prix(self):
        """Ajoute `prix_a_partir_de` : le prix de la contenance la moins chère."""
        return self.annotate(prix_a_partir_de=Min("variantes__prix"))


class Parfum(models.Model):
    nom = models.CharField("nom", max_length=120)
    slug = models.SlugField("adresse", max_length=140, unique=True, blank=True)
    marque = models.CharField("marque", max_length=80)
    description = models.TextField("description", blank=True)
    famille = models.CharField("famille olfactive", max_length=20, choices=Famille.choices)
    genre = models.CharField("genre", max_length=10, choices=Genre.choices)
    concentration = models.CharField(
        "concentration", max_length=20, choices=Concentration.choices
    )
    notes_tete = models.CharField(
        "notes de tête", max_length=200, blank=True, help_text="Séparées par des virgules."
    )
    notes_coeur = models.CharField(
        "notes de cœur", max_length=200, blank=True, help_text="Séparées par des virgules."
    )
    notes_fond = models.CharField(
        "notes de fond", max_length=200, blank=True, help_text="Séparées par des virgules."
    )
    image = models.ImageField("photo principale", upload_to="parfums/", blank=True)
    image_url = models.URLField(
        "URL image externe", max_length=500, blank=True,
        help_text="URL d'une image externe (Unsplash, CDN…) utilisée si aucun fichier n'est uploadé."
    )
    collection = models.ForeignKey(
        Collection,
        verbose_name="collection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parfums",
    )
    nouveau = models.BooleanField("nouveauté", default=False)
    meilleure_vente = models.BooleanField("meilleure vente", default=False)
    actif = models.BooleanField(
        "affiché sur le site", default=True, help_text="Décochez pour masquer le parfum."
    )
    cree_le = models.DateTimeField("créé le", auto_now_add=True)

    objects = ParfumQuerySet.as_manager()

    class Meta:
        ordering = ["-cree_le"]
        verbose_name = "parfum"
        verbose_name_plural = "parfums"

    def __str__(self):
        return f"{self.nom} ({self.marque})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = _slug_unique(Parfum, self.nom, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalogue:detail", args=[self.slug])

    @staticmethod
    def _decouper(texte):
        return [note.strip() for note in texte.split(",") if note.strip()]

    @property
    def notes_tete_liste(self):
        return self._decouper(self.notes_tete)

    @property
    def notes_coeur_liste(self):
        return self._decouper(self.notes_coeur)

    @property
    def notes_fond_liste(self):
        return self._decouper(self.notes_fond)

    @property
    def variante_par_defaut(self):
        """Première contenance en stock (la plus petite), pour l'ajout rapide."""
        for variante in self.variantes.all():
            if variante.stock > 0:
                return variante
        return None


class Variante(models.Model):
    """Une contenance d'un parfum, avec son prix et son stock."""

    parfum = models.ForeignKey(
        Parfum, verbose_name="parfum", on_delete=models.CASCADE, related_name="variantes"
    )
    contenance_ml = models.PositiveSmallIntegerField("contenance (ml)")
    prix = models.DecimalField(
        "prix", max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField("stock", default=0)

    class Meta:
        ordering = ["contenance_ml"]
        verbose_name = "contenance"
        verbose_name_plural = "contenances"
        constraints = [
            models.UniqueConstraint(
                fields=["parfum", "contenance_ml"], name="contenance_unique_par_parfum"
            )
        ]

    def __str__(self):
        return f"{self.parfum.nom} - {self.contenance_ml} ml"

    @property
    def en_stock(self):
        return self.stock > 0


class ImageParfum(models.Model):
    """Photo supplémentaire d'un parfum (flacon, packaging, ambiance)."""

    parfum = models.ForeignKey(
        Parfum, verbose_name="parfum", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField("photo", upload_to="parfums/")
    legende = models.CharField("légende", max_length=120, blank=True)
    ordre = models.PositiveSmallIntegerField("ordre", default=0)

    class Meta:
        ordering = ["ordre", "id"]
        verbose_name = "photo"
        verbose_name_plural = "photos"

    def __str__(self):
        return self.legende or f"Photo de {self.parfum.nom}"
