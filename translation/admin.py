from django.contrib import admin
from .models import Traduction, Dictionnaire


@admin.register(Traduction)
class TraductionAdmin(admin.ModelAdmin):
    list_display = ['user', 'texte_original_court', 'langue_originale', 'langue_cible', 'created_at']
    list_filter = ['langue_originale', 'langue_cible', 'created_at']
    search_fields = ['texte_original', 'texte_traduit', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_select_related = ['user']
    
    def texte_original_court(self, obj):
        return obj.texte_original[:50] + '...' if len(obj.texte_original) > 50 else obj.texte_original
    texte_original_court.short_description = 'Texte original'


@admin.register(Dictionnaire)
class DictionnaireAdmin(admin.ModelAdmin):
    list_display = ['mot_francais', 'mot_ewe', 'mot_kab', 'categorie']
    list_filter = ['categorie']
    search_fields = ['mot_francais', 'mot_ewe', 'mot_kab', 'definition']
    fieldsets = (
        ('Mots', {
            'fields': ('mot_francais', 'mot_ewe', 'mot_kab')
        }),
        ('Informations', {
            'fields': ('definition', 'categorie')
        }),
    )

