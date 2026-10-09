from django.urls import path

from . import views, cms_views

app_name = "catalogue"

urlpatterns = [
    # Site Public
    path("", views.accueil, name="accueil"),
    path("parfums/", views.liste, name="liste"),
    path("parfums/<slug:slug>/", views.detail, name="detail"),

    # CMS / Gestion du Catalogue
    path("cms/", cms_views.cms_dashboard, name="cms_dashboard"),
    path("cms/parfums/", cms_views.cms_parfum_liste, name="cms_parfum_liste"),
    path("cms/parfums/nouveau/", cms_views.cms_parfum_ajouter, name="cms_parfum_ajouter"),
    path("cms/parfums/<int:pk>/editer/", cms_views.cms_parfum_editer, name="cms_parfum_editer"),
    path("cms/parfums/<int:pk>/image/", cms_views.cms_parfum_image, name="cms_parfum_image"),
    path("cms/parfums/<int:pk>/supprimer/", cms_views.cms_parfum_supprimer, name="cms_parfum_supprimer"),
    path("cms/collections/", cms_views.cms_collections, name="cms_collections"),
]
