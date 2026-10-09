"""Réglages Django du site de vente de parfums.

Les valeurs sensibles (clé secrète, mode debug, hôtes autorisés) se lisent dans
les variables d'environnement : voir la section « Mise en production » du README.
"""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Sécurité -----------------------------------------------------------------

# DJANGO_DEBUG=1 (défaut) pour développer, DJANGO_DEBUG=0 en production.
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = "django-insecure-parfumerie-haute-couture-secret-key-2026-production"

_hotes = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]
ALLOWED_HOSTS = _hotes or [".onrender.com", "localhost", "127.0.0.1", "*"]

# Options de sécurité des en-têtes et cookies
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

if not DEBUG:
    # Les cookies de session et CSRF ne voyagent qu'en HTTPS.
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- Applications -------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalogue",
    "panier",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "config.security_middleware.SecurityHeadersMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "catalogue.context_processors.site",
                "panier.context_processors.panier",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Base de données ----------------------------------------------------------
# SQLite suffit pour développer. En production, préférer PostgreSQL.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Langue et heure ----------------------------------------------------------

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"  # À adapter au fuseau horaire de la boutique.
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques et images envoyées depuis l'administration ------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Réglages propres à la boutique -------------------------------------------

NOM_SITE = "Ma Parfumerie"  # À remplacer par le nom de la marque.
DEVISE = "€"  # Symbole affiché après les prix.
QUANTITE_MAX_PANIER = 10  # Quantité maximale d'un même article dans le panier.
