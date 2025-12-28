from django.contrib import admin
from .models import Performance, Activite


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'matiere', 'score_moyen', 'nombre_qcm', 'nombre_flashcards', 'temps_etude_heures', 'updated_at']
    list_filter = ['matiere', 'updated_at']
    search_fields = ['user__username', 'matiere__nom']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'updated_at'
    list_select_related = ['user', 'matiere']
    
    def temps_etude_heures(self, obj):
        return f"{obj.temps_etude_minutes / 60:.1f} h"
    temps_etude_heures.short_description = 'Temps d\'étude'


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_activite', 'description_court', 'duree_minutes', 'created_at']
    list_filter = ['type_activite', 'created_at']
    search_fields = ['description', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_select_related = ['user']
    
    def description_court(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_court.short_description = 'Description'

