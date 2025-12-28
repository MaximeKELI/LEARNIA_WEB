from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'longueur_original', 'longueur_resume', 'points_cles_count', 'created_at']
    list_filter = ['created_at', 'chapitre__matiere']
    search_fields = ['titre', 'texte_original', 'resume_texte', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'points_cles']
    date_hierarchy = 'created_at'
    list_select_related = ['user', 'chapitre']
    fieldsets = (
        ('Informations', {
            'fields': ('user', 'chapitre', 'titre')
        }),
        ('Contenu', {
            'fields': ('texte_original', 'resume_texte', 'points_cles')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def longueur_original(self, obj):
        return f"{len(obj.texte_original)} caractères"
    longueur_original.short_description = 'Texte original'
    
    def longueur_resume(self, obj):
        return f"{len(obj.resume_texte)} caractères"
    longueur_resume.short_description = 'Résumé'
    
    def points_cles_count(self, obj):
        return len(obj.points_cles) if obj.points_cles else 0
    points_cles_count.short_description = 'Points clés'

