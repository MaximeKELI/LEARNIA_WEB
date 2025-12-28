from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'created_at']
    list_filter = ['created_at']
    search_fields = ['titre', 'texte_original']

