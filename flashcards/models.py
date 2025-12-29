from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class Deck(models.Model):
    """Deck de flashcards"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    titre = models.CharField(max_length=200)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.titre


class Flashcard(models.Model):
    """Flashcard individuelle"""
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    recto = models.TextField()
    verso = models.TextField()
    niveau = models.IntegerField(default=0, help_text="Niveau Leitner (0-4)")
    prochaine_revision = models.DateTimeField(default=timezone.now)
    nombre_revisions = models.IntegerField(default=0)
    nombre_success = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['prochaine_revision']

    def __str__(self):
        return f"{self.recto[:50]}"

    def marquer_success(self):
        """Marque la carte comme réussie et augmente le niveau"""
        self.niveau = min(self.niveau + 1, 4)
        self.nombre_revisions += 1
        self.nombre_success += 1
        # Calculer la prochaine révision selon le système Leitner
        jours = [1, 2, 5, 10, 30][self.niveau]
        self.prochaine_revision = timezone.now() + timedelta(days=jours)
        self.save()

    def marquer_echec(self):
        """Marque la carte comme échouée et réinitialise le niveau"""
        self.niveau = 0
        self.nombre_revisions += 1
        self.prochaine_revision = timezone.now() + timedelta(days=1)
        self.save()


class Revision(models.Model):
    """Historique des révisions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revisions')
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE, related_name='revisions')
    reussie = models.BooleanField()
    temps_reponse = models.IntegerField(help_text="Temps de réponse en secondes", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.flashcard.recto[:30]} - {('✓' if self.reussie else '✗')}"



