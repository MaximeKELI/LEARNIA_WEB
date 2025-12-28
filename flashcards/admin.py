from django.contrib import admin
from .models import Deck, Flashcard, Revision


class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1
    fields = ['recto', 'verso', 'niveau', 'prochaine_revision']
    readonly_fields = ['niveau', 'prochaine_revision']


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'nombre_flashcards', 'created_at']
    list_filter = ['created_at', 'chapitre__matiere']
    search_fields = ['titre', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [FlashcardInline]
    list_select_related = ['user', 'chapitre']
    
    def nombre_flashcards(self, obj):
        return obj.flashcards.count()
    nombre_flashcards.short_description = 'Flashcards'


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['recto_court', 'deck', 'niveau', 'nombre_revisions', 'nombre_success', 'prochaine_revision']
    list_filter = ['niveau', 'deck', 'prochaine_revision']
    search_fields = ['recto', 'verso', 'deck__titre']
    readonly_fields = ['niveau', 'nombre_revisions', 'nombre_success', 'prochaine_revision', 'created_at', 'updated_at']
    date_hierarchy = 'prochaine_revision'
    list_select_related = ['deck', 'deck__user']
    
    def recto_court(self, obj):
        return obj.recto[:50] + '...' if len(obj.recto) > 50 else obj.recto
    recto_court.short_description = 'Recto'
    
    def taux_reussite(self, obj):
        if obj.nombre_revisions > 0:
            return f"{(obj.nombre_success / obj.nombre_revisions * 100):.1f}%"
        return "N/A"
    taux_reussite.short_description = 'Taux de réussite'


@admin.register(Revision)
class RevisionAdmin(admin.ModelAdmin):
    list_display = ['user', 'flashcard_court', 'reussie', 'temps_reponse', 'created_at']
    list_filter = ['reussie', 'created_at']
    search_fields = ['flashcard__recto', 'flashcard__verso', 'user__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_select_related = ['user', 'flashcard']
    
    def flashcard_court(self, obj):
        return obj.flashcard.recto[:50] + '...' if len(obj.flashcard.recto) > 50 else obj.flashcard.recto
    flashcard_court.short_description = 'Flashcard'

