from django.contrib import admin
from .models import Questionnaire, Filiere, Metier


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'filiere_suggeree', 'score_scientifique', 'score_litteraire', 'score_commercial', 'score_technique', 'created_at']
    list_filter = ['filiere_suggeree', 'created_at']
    search_fields = ['user__username', 'filiere_suggeree']
    readonly_fields = ['created_at', 'updated_at', 'reponses', 'metiers_suggestes']
    date_hierarchy = 'created_at'
    list_select_related = ['user']
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Résultats', {
            'fields': ('score_scientifique', 'score_litteraire', 'score_commercial', 'score_technique', 'filiere_suggeree', 'metiers_suggestes')
        }),
        ('Détails', {
            'fields': ('reponses',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'type_filiere', 'nombre_metiers']
    list_filter = ['type_filiere']
    search_fields = ['nom', 'code', 'description']
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'code', 'type_filiere')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Détails', {
            'fields': ('matieres_principales', 'metiers')
        }),
    )
    
    def nombre_metiers(self, obj):
        return len(obj.metiers) if obj.metiers else 0
    nombre_metiers.short_description = 'Métiers'


@admin.register(Metier)
class MetierAdmin(admin.ModelAdmin):
    list_display = ['nom', 'nombre_filieres', 'formation_requise_court']
    search_fields = ['nom', 'description', 'formation_requise']
    filter_horizontal = ['filieres']
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'description')
        }),
        ('Formation', {
            'fields': ('formation_requise', 'competences')
        }),
        ('Filieres', {
            'fields': ('filieres',)
        }),
    )
    
    def nombre_filieres(self, obj):
        return obj.filieres.count()
    nombre_filieres.short_description = 'Filières'
    
    def formation_requise_court(self, obj):
        return obj.formation_requise[:50] + '...' if len(obj.formation_requise) > 50 else obj.formation_requise
    formation_requise_court.short_description = 'Formation'

