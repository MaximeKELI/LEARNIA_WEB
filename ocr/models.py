from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Devoir(models.Model):
    """Devoir manuscrit soumis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devoirs')
    image = models.ImageField(upload_to='devoirs/')
    texte_reconnu = models.TextField(blank=True)
    matiere = models.CharField(max_length=100, blank=True)
    note = models.IntegerField(null=True, blank=True)
    commentaires = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.matiere} ({self.created_at.strftime('%d/%m/%Y')})"


