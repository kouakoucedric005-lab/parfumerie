# Ma Parfumerie : boutique de base (Django)

Premier jalon du site de vente de parfums décrit dans le document de conception :
catalogue avec filtres, fiche produit (pyramide olfactive), panier et administration.

## Lancer le site

Prérequis : Python 3.12 ou plus récent (3.10+ pour Django 5.2).

```bash
cd parfumerie
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations catalogue   # crée les fichiers de migration
python manage.py migrate                    # crée la base SQLite
python manage.py charger_demo               # (facultatif) parfums fictifs
python manage.py createsuperuser            # compte pour l'administration
python manage.py runserver
```

- Site : http://127.0.0.1:8000/
- Administration : http://127.0.0.1:8000/admin/ (ajout des parfums, contenances, prix, stocks, photos)
- Tests : `python manage.py test`

## Où se trouve quoi

| Dossier ou fichier | Rôle |
| --- | --- |
| `config/settings.py` | Réglages (nom du site `NOM_SITE`, devise `DEVISE`, quantité max par article) |
| `catalogue/models.py` | `Collection`, `Parfum`, `Variante` (contenance, prix, stock), `ImageParfum` |
| `catalogue/views.py` | Accueil, catalogue (filtres, tri, pagination), fiche produit |
| `panier/panier.py` | Panier conservé en session ; prix et stocks relus en base |
| `templates/` | Pages HTML (`base.html`, `catalogue/`, `panier/`, `404.html`) |
| `static/css/site.css` | Style : les variables en haut du fichier sont à remplacer par celles du designer |
| `static/js/site.js` | Menu mobile et mise à jour du prix selon la contenance (facultatif) |

## Ce que le designer peut modifier sans toucher à Python

Les couleurs, polices et espacements sont des variables CSS au début de `static/css/site.css`.
Les pages sont dans `templates/`. L'ordre des blocs, les textes et les classes CSS s'y modifient directement.

## Pas encore dans cette version

Commande et paiement en ligne, comptes clients, e-mails de commande, codes promo, avis clients,
pages d'information (livraison, FAQ, contact, mentions légales). Le bouton « Commander » du panier est
volontairement désactivé en attendant l'étape suivante.

## Mise en production (liste de départ)

- `DJANGO_DEBUG=0` et `DJANGO_SECRET_KEY` définie dans l'environnement : le site refuse de démarrer sans clé en production.
- `DJANGO_ALLOWED_HOSTS=exemple.com,www.exemple.com` (noms de domaine séparés par des virgules).
- Servir le site en HTTPS uniquement ; les cookies de session et CSRF passent alors en « secure » automatiquement.
- Changer l'adresse `/admin/` et protéger le compte administrateur par un mot de passe long.
- Remplacer SQLite par PostgreSQL, puis lancer `python manage.py collectstatic` et faire servir `staticfiles/` et `media/` par le serveur web.
- Ne jamais stocker de numéros de carte : le paiement passera par un prestataire externe.
