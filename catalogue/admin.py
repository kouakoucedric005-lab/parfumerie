from django.contrib import admin
from django.utils.html import format_html

from .models import Collection, ImageParfum, Parfum, Variante


# --- Personnalisation du titre du panneau d'administration ---
admin.site.site_header = "🌸 Parfumerie — Gestion Privée"
admin.site.site_title  = "Parfumerie Admin"
admin.site.index_title = "Tableau de bord"


class VarianteInline(admin.TabularInline):
    model = Variante
    extra = 1
    fields = ("contenance_ml", "prix", "stock")


class ImageParfumInline(admin.TabularInline):
    model = ImageParfum
    extra = 1
    fields = ("image", "legende", "ordre")
    readonly_fields = ("apercu",)

    def apercu(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:80px; border-radius:6px;">', obj.image.url)
        return "—"
    apercu.short_description = "Aperçu"


@admin.register(Parfum)
class ParfumAdmin(admin.ModelAdmin):
    list_display = (
        "apercu_miniature", "nom", "marque", "famille", "genre",
        "concentration", "nouveau", "meilleure_vente", "actif",
    )
    list_editable   = ("nouveau", "meilleure_vente", "actif")
    list_filter     = ("actif", "genre", "famille", "concentration", "collection")
    search_fields   = ("nom", "marque", "notes_tete", "notes_coeur", "notes_fond")
    prepopulated_fields = {"slug": ("nom",)}
    readonly_fields = ("apercu_image",)
    inlines = [VarianteInline, ImageParfumInline]

    fieldsets = (
        ("📋 Informations générales", {
            "fields": ("nom", "slug", "marque", "collection", "actif", "nouveau", "meilleure_vente"),
        }),
        ("🖼️ Image principale", {
            "fields": ("image", "image_url", "apercu_image"),
            "description": (
                "Uploadez une photo <strong>OU</strong> collez une URL externe. "
                "L'image uploadée est prioritaire sur l'URL."
            ),
        }),
        ("🌿 Caractéristiques olfactives", {
            "fields": ("famille", "genre", "concentration", "description"),
        }),
        ("🎵 Pyramide olfactive", {
            "fields": ("notes_tete", "notes_coeur", "notes_fond"),
            "classes": ("collapse",),
        }),
    )

    def apercu_miniature(self, obj):
        src = obj.image.url if obj.image else obj.image_url
        if src:
            return format_html(
                '<img src="{}" style="height:50px; width:50px; object-fit:cover; '
                'border-radius:6px; border:1px solid #e5e5e5;">',
                src,
            )
        return "—"
    apercu_miniature.short_description = "Photo"

    def apercu_image(self, obj):
        src = obj.image.url if obj.image else obj.image_url
        if src:
            return format_html(
                '<img src="{}" style="max-height:200px; border-radius:10px; '
                'border:1px solid #e5e5e5; margin-top:8px;">',
                src,
            )
        return "Aucune image pour le moment."
    apercu_image.short_description = "Aperçu actuel"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display  = ("nom", "ordre", "apercu_image")
    list_editable = ("ordre",)
    prepopulated_fields = {"slug": ("nom",)}
    readonly_fields = ("apercu_image",)

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;">', obj.image.url)
        return "—"
    apercu_image.short_description = "Image"
