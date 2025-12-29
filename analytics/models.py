from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Matiere

User = get_user_model()


class Performance(models.Model):
    """Performances de l'élève"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performances')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='performances')
    score_moyen = models.FloatField(default=0.0)
    nombre_qcm = models.IntegerField(default=0)
    nombre_flashcards = models.IntegerField(default=0)
    temps_etude_minutes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'matiere']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.matiere.nom}"


class Activite(models.Model):
    """Historique des activités"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activites')
    type_activite = models.CharField(
        max_length=50,
        choices=[
            ('qcm', 'QCM'),
            ('flashcard', 'Flashcard'),
            ('tuteur', 'Tuteur'),
            ('resume', 'Résumé'),
            ('traduction', 'Traduction'),
        ]
    )
    description = models.CharField(max_length=200)
    duree_minutes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.type_activite}"



