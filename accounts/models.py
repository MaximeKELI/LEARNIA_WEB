from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé"""
    niveau_etude = models.CharField(
        max_length=50,
        choices=[
            ('primaire', 'Primaire'),
            ('6e', '6ème'),
            ('5e', '5ème'),
            ('4e', '4ème'),
            ('3e', '3ème'),
            ('2nde', '2nde'),
            ('1ere', '1ère'),
            ('terminale', 'Terminale'),
        ],
        default='6e'
    )
    classe = models.CharField(max_length=50, blank=True)
    ecole = models.CharField(max_length=200, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Matiere(models.Model):
    """Matières scolaires"""
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    niveau = models.CharField(
        max_length=50,
        choices=[
            ('primaire', 'Primaire'),
            ('college', 'Collège'),
            ('lycee', 'Lycée'),
        ]
    )
    description = models.TextField(blank=True)
    icone = models.CharField(max_length=50, default='📚')

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Chapitre(models.Model):
    """Chapitres de cours"""
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='chapitres')
    titre = models.CharField(max_length=200)
    numero = models.IntegerField()
    contenu = models.TextField()
    niveau = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['matiere', 'numero']
        unique_together = ['matiere', 'numero']

    def __str__(self):
        return f"{self.matiere.nom} - {self.titre}"



