from django.contrib import admin
from django.utils.html import format_html
from .models import Examen, RevisionPlanifiee, Rappel


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ['nom', 'user', 'matiere', 'date_examen', 'jours_restants', 'created_at']
    list_filter = ['date_examen', 'matiere', 'created_at']
    search_fields = ['nom', 'description', 'user__username', 'matiere__nom']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date_examen'
    list_select_related = ['user', 'matiere']
    
    def jours_restants(self, obj):
        from django.utils import timezone
        delta = obj.date_examen.date() - timezone.now().date()
        jours = delta.days
        if jours < 0:
            return format_html('<span style="color: red;">Passé ({} jours)</span>', abs(jours))
        elif jours == 0:
            return format_html('<span style="color: orange; font-weight: bold;">Aujourd\'hui</span>')
        elif jours <= 7:
            return format_html('<span style="color: orange;">{} jours</span>', jours)
        else:
            return f"{jours} jours"
    jours_restants.short_description = 'Jours restants'


@admin.register(RevisionPlanifiee)
class RevisionPlanifieeAdmin(admin.ModelAdmin):
    list_display = ['chapitre', 'user', 'date_revision', 'type_revision', 'duree_prevue_minutes', 'terminee', 'created_at']
    list_filter = ['type_revision', 'terminee', 'date_revision', 'chapitre__matiere']
    search_fields = ['chapitre__titre', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date_revision'
    list_select_related = ['user', 'chapitre', 'chapitre__matiere']
    actions = ['marquer_comme_terminee', 'marquer_comme_non_terminee']
    
    def marquer_comme_terminee(self, request, queryset):
        queryset.update(terminee=True)
        self.message_user(request, f"{queryset.count()} révision(s) marquée(s) comme terminée(s).")
    marquer_comme_terminee.short_description = "Marquer comme terminée"
    
    def marquer_comme_non_terminee(self, request, queryset):
        queryset.update(terminee=False)
        self.message_user(request, f"{queryset.count()} révision(s) marquée(s) comme non terminée(s).")
    marquer_comme_non_terminee.short_description = "Marquer comme non terminée"


@admin.register(Rappel)
class RappelAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'date_rappel', 'envoye', 'created_at']
    list_filter = ['envoye', 'date_rappel', 'created_at']
    search_fields = ['titre', 'message', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'date_rappel'
    list_select_related = ['user']
    actions = ['marquer_comme_envoye', 'marquer_comme_non_envoye']
    
    def marquer_comme_envoye(self, request, queryset):
        queryset.update(envoye=True)
        self.message_user(request, f"{queryset.count()} rappel(s) marqué(s) comme envoyé(s).")
    marquer_comme_envoye.short_description = "Marquer comme envoyé"
    
    def marquer_comme_non_envoye(self, request, queryset):
        queryset.update(envoye=False)
        self.message_user(request, f"{queryset.count()} rappel(s) marqué(s) comme non envoyé(s).")
    marquer_comme_non_envoye.short_description = "Marquer comme non envoyé"

