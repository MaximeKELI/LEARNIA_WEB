from django.contrib import admin
from .models import Questionnaire, Filiere, Metier


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'filiere_suggeree', 'created_at']
    list_filter = ['filiere_suggeree', 'created_at']


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'type_filiere']
    list_filter = ['type_filiere']


@admin.register(Metier)
class MetierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'formation_requise']
    filter_horizontal = ['filieres']

