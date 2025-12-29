from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre

User = get_user_model()


class FicheRevision(models.Model):
    """Fiches de révision générées"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fiches')
    titre = models.CharField(max_length=200)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True)
    contenu = models.TextField(help_text="Contenu de la fiche formaté")
    couleur_titre = models.CharField(max_length=20, default='#007bff')
    police = models.CharField(max_length=50, default='Arial')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titre


