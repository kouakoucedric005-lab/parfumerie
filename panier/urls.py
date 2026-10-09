from django.urls import path

from . import views

app_name = "panier"

urlpatterns = [
    path("", views.detail, name="detail"),
    path("ajouter/", views.ajouter, name="ajouter"),
    path("modifier/", views.modifier, name="modifier"),
    path("retirer/", views.retirer, name="retirer"),
]
