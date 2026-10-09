from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("panier/", include("panier.urls")),
    path("", include("catalogue.urls")),
]

if settings.DEBUG:
    # En développement, Django sert lui-même les images envoyées via l'administration.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
