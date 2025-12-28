from django.contrib import admin
from .models import Traduction, Dictionnaire


@admin.register(Traduction)
class TraductionAdmin(admin.ModelAdmin):
    list_display = ['user', 'langue_originale', 'langue_cible', 'created_at']
    list_filter = ['langue_originale', 'langue_cible', 'created_at']


@admin.register(Dictionnaire)
class DictionnaireAdmin(admin.ModelAdmin):
    list_display = ['mot_francais', 'mot_ewe', 'mot_kab', 'categorie']
    search_fields = ['mot_francais', 'mot_ewe', 'mot_kab']

