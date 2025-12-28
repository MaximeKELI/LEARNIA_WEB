from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Matiere, Chapitre
from django.utils import timezone

User = get_user_model()


class Examen(models.Model):
    """Examens planifiés"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='examens')
    nom = models.CharField(max_length=200)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    date_examen = models.DateTimeField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_examen']

    def __str__(self):
        return f"{self.nom} - {self.matiere.nom}"


class RevisionPlanifiee(models.Model):
    """Révisions planifiées"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revisions_planifiees')
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    date_revision = models.DateTimeField()
    duree_prevue_minutes = models.IntegerField(default=30)
    type_revision = models.CharField(
        max_length=50,
        choices=[
            ('lecture', 'Lecture'),
            ('qcm', 'QCM'),
            ('flashcard', 'Flashcards'),
            ('resume', 'Résumé'),
        ],
        default='lecture'
    )
    terminee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_revision']

    def __str__(self):
        return f"{self.chapitre.titre} - {self.date_revision.strftime('%d/%m/%Y')}"


class Rappel(models.Model):
    """Rappels pour les révisions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rappels')
    titre = models.CharField(max_length=200)
    message = models.TextField()
    date_rappel = models.DateTimeField()
    envoye = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_rappel']

    def __str__(self):
        return f"{self.titre} - {self.date_rappel.strftime('%d/%m/%Y %H:%M')}"

