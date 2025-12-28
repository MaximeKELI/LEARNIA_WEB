from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Questionnaire(models.Model):
    """Questionnaire d'orientation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaires')
    reponses = models.JSONField(default=dict, help_text="Réponses au questionnaire")
    score_scientifique = models.IntegerField(default=0)
    score_litteraire = models.IntegerField(default=0)
    score_commercial = models.IntegerField(default=0)
    score_technique = models.IntegerField(default=0)
    filiere_suggeree = models.CharField(max_length=200, blank=True)
    metiers_suggestes = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.filiere_suggeree}"


class Filiere(models.Model):
    """Filières scolaires"""
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    type_filiere = models.CharField(
        max_length=50,
        choices=[
            ('scientifique', 'Scientifique'),
            ('litteraire', 'Littéraire'),
            ('commercial', 'Commercial'),
            ('technique', 'Technique'),
        ]
    )
    matieres_principales = models.JSONField(default=list)
    metiers = models.JSONField(default=list)

    def __str__(self):
        return self.nom


class Metier(models.Model):
    """Métiers"""
    nom = models.CharField(max_length=200)
    description = models.TextField()
    filieres = models.ManyToManyField(Filiere, related_name='metiers')
    competences = models.JSONField(default=list)
    formation_requise = models.TextField(blank=True)

    def __str__(self):
        return self.nom

