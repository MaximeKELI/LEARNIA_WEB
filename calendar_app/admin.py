from django.contrib import admin
from .models import EvenementScolaire


@admin.register(EvenementScolaire)
class EvenementScolaireAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_evenement', 'date_debut', 'user', 'public', 'created_at']
    list_filter = ['type_evenement', 'public', 'date_debut']
    search_fields = ['titre', 'description', 'user__username']
    date_hierarchy = 'date_debut'


