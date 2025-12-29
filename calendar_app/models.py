from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Matiere

User = get_user_model()


class EvenementScolaire(models.Model):
    """Événements du calendrier scolaire"""
    TYPE_EVENEMENT = [
        ('examen', 'Examen'),
        ('vacances', 'Vacances'),
        ('fete', 'Fête'),
        ('reunion', 'Réunion'),
        ('activite', 'Activité'),
        ('rappel', 'Rappel'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='evenements_personnels')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    type_evenement = models.CharField(max_length=20, choices=TYPE_EVENEMENT, default='rappel')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, blank=True)
    couleur = models.CharField(max_length=20, default='#007bff')
    rappel_jours = models.IntegerField(default=1, help_text="Nombre de jours avant pour le rappel")
    public = models.BooleanField(default=False, help_text="Visible par tous les utilisateurs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_debut']
        indexes = [
            models.Index(fields=['date_debut']),
            models.Index(fields=['user', 'date_debut']),
        ]

    def __str__(self):
        return f"{self.titre} - {self.date_debut}"


