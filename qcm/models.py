from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre

User = get_user_model()


class QCM(models.Model):
    """Quiz QCM généré"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qcms')
    titre = models.CharField(max_length=200)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True)
    texte_source = models.TextField(help_text="Texte à partir duquel générer les questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.titre


class Question(models.Model):
    """Questions d'un QCM"""
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()
    numero = models.IntegerField()

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Q{self.numero}: {self.texte[:50]}"


class Choix(models.Model):
    """Choix de réponse pour une question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choix')
    texte = models.CharField(max_length=500)
    est_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texte} ({'✓' if self.est_correct else ''})"


class ResultatQCM(models.Model):
    """Résultats d'un QCM complété"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultats_qcm')
    qcm = models.ForeignKey(QCM, on_delete=models.CASCADE, related_name='resultats')
    score = models.IntegerField()
    total = models.IntegerField()
    pourcentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.qcm.titre} ({self.pourcentage}%)"


