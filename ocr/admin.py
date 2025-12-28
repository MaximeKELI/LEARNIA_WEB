from django.contrib import admin
from django.utils.html import format_html
from .models import Devoir


@admin.register(Devoir)
class DevoirAdmin(admin.ModelAdmin):
    list_display = ['user', 'matiere', 'note_avec_couleur', 'image_preview', 'texte_court', 'created_at']
    list_filter = ['matiere', 'created_at', 'note']
    search_fields = ['texte_reconnu', 'matiere', 'commentaires', 'user__username']
    readonly_fields = ['created_at', 'image_preview_large', 'texte_reconnu']
    date_hierarchy = 'created_at'
    list_select_related = ['user']
    fieldsets = (
        ('Informations', {
            'fields': ('user', 'matiere', 'note')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Texte reconnu', {
            'fields': ('texte_reconnu',)
        }),
        ('Correction', {
            'fields': ('commentaires',)
        }),
        ('Date', {
            'fields': ('created_at',)
        }),
    )
    
    def note_avec_couleur(self, obj):
        if obj.note is None:
            return "Non noté"
        if obj.note >= 16:
            color = 'green'
        elif obj.note >= 12:
            color = 'blue'
        elif obj.note >= 10:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {}; font-weight: bold;">{}/20</span>', color, obj.note)
    note_avec_couleur.short_description = 'Note'
    
    def texte_court(self, obj):
        return obj.texte_reconnu[:50] + '...' if obj.texte_reconnu and len(obj.texte_reconnu) > 50 else (obj.texte_reconnu or 'Aucun texte')
    texte_court.short_description = 'Texte'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Image'
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 400px; max-width: 100%;" />', obj.image.url)
        return "Pas d'image"
    image_preview_large.short_description = 'Aperçu'

