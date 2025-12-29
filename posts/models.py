from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    """Posts/annonces créés par les administrateurs"""
    TYPE_CHOICES = [
        ('annonce', 'Annonce'),
        ('info', 'Information'),
        ('actualite', 'Actualité'),
        ('alerte', 'Alerte'),
        ('evenement', 'Événement'),
    ]
    
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', limit_choices_to={'is_staff': True})
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    type_post = models.CharField(max_length=50, choices=TYPE_CHOICES, default='annonce')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    publique = models.BooleanField(default=True, help_text="Visible par tous les utilisateurs")
    prioritaire = models.BooleanField(default=False, help_text="Afficher en haut de la liste")
    date_publication = models.DateTimeField(default=timezone.now)
    date_expiration = models.DateTimeField(null=True, blank=True, help_text="Date après laquelle le post ne sera plus affiché")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-prioritaire', '-date_publication']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.titre
    
    def is_active(self):
        """Vérifie si le post est actif (pas expiré)"""
        if self.date_expiration:
            return timezone.now() < self.date_expiration
        return True
    
    def get_type_badge_class(self):
        """Retourne la classe Bootstrap pour le badge selon le type"""
        classes = {
            'annonce': 'bg-primary',
            'info': 'bg-info',
            'actualite': 'bg-success',
            'alerte': 'bg-danger',
            'evenement': 'bg-warning',
        }
        return classes.get(self.type_post, 'bg-secondary')



