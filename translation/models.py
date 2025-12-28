from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

LANGUAGES = [
    ('ewe', 'Éwé'),
    ('kab', 'Kabiyè'),
    ('fr', 'Français'),
]


class Traduction(models.Model):
    """Traduction de texte"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='traductions')
    texte_original = models.TextField()
    langue_originale = models.CharField(max_length=3, choices=LANGUAGES, default='fr')
    langue_cible = models.CharField(max_length=3, choices=LANGUAGES)
    texte_traduit = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.langue_originale} → {self.langue_cible}"


class Dictionnaire(models.Model):
    """Dictionnaire local pour les traductions"""
    mot_francais = models.CharField(max_length=200)
    mot_ewe = models.CharField(max_length=200, blank=True)
    mot_kab = models.CharField(max_length=200, blank=True)
    definition = models.TextField(blank=True)
    categorie = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['mot_francais']

    def __str__(self):
        return self.mot_francais

