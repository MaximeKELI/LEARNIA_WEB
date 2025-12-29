from django.contrib import admin
from .models import FicheRevision


@admin.register(FicheRevision)
class FicheRevisionAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'created_at']
    list_filter = ['created_at']
    search_fields = ['titre', 'contenu', 'user__username']


