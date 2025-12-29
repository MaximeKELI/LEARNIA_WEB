from django.contrib import admin
from .models import Note, NoteVersion


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'favori', 'created_at', 'updated_at']
    list_filter = ['favori', 'created_at', 'chapitre__matiere']
    search_fields = ['titre', 'contenu', 'tags', 'user__username']
    date_hierarchy = 'updated_at'


@admin.register(NoteVersion)
class NoteVersionAdmin(admin.ModelAdmin):
    list_display = ['note', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note__titre']


