from django.contrib import admin
from .models import Performance, Activite


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'matiere', 'score_moyen', 'nombre_qcm', 'nombre_flashcards']
    list_filter = ['matiere']


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_activite', 'description', 'duree_minutes', 'created_at']
    list_filter = ['type_activite', 'created_at']

