from django.contrib import admin

from .models import Collection, ImageParfum, Parfum, Variante


class VarianteInline(admin.TabularInline):
    model = Variante
    extra = 1


class ImageParfumInline(admin.TabularInline):
    model = ImageParfum
    extra = 0


@admin.register(Parfum)
class ParfumAdmin(admin.ModelAdmin):
    list_display = (
        "nom", "marque", "famille", "genre", "concentration",
        "nouveau", "meilleure_vente", "actif",
    )
    list_editable = ("nouveau", "meilleure_vente", "actif")
    list_filter = ("actif", "genre", "famille", "concentration", "collection")
    search_fields = ("nom", "marque", "notes_tete", "notes_coeur", "notes_fond")
    prepopulated_fields = {"slug": ("nom",)}
    inlines = [VarianteInline, ImageParfumInline]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("nom", "ordre")
    list_editable = ("ordre",)
    prepopulated_fields = {"slug": ("nom",)}
