from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre

User = get_user_model()


class Resume(models.Model):
    """Résumé automatique d'un cours"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True)
    titre = models.CharField(max_length=200)
    texte_original = models.TextField()
    resume_texte = models.TextField()
    points_cles = models.JSONField(default=list, help_text="Liste des points clés extraits")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titre



