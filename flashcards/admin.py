from django.contrib import admin
from .models import Deck, Flashcard, Revision


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'created_at']
    list_filter = ['created_at']
    search_fields = ['titre', 'user__username']


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['recto', 'deck', 'niveau', 'prochaine_revision', 'nombre_revisions']
    list_filter = ['niveau', 'deck']
    search_fields = ['recto', 'verso']


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ['user', 'flashcard', 'reussie', 'created_at']
    list_filter = ['reussie', 'created_at']

