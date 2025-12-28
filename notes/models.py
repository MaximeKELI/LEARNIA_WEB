from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre

User = get_user_model()


class Note(models.Model):
    """Notes personnelles de l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    tags = models.CharField(max_length=500, blank=True, help_text="Tags séparés par des virgules")
    favori = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['favori']),
        ]

    def __str__(self):
        return self.titre
    
    def get_tags_list(self):
        """Retourne les tags sous forme de liste"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []


class NoteVersion(models.Model):
    """Historique des versions d'une note"""
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.note.titre} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

