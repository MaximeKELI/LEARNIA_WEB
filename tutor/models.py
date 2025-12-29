from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Chapitre

User = get_user_model()


class Conversation(models.Model):
    """Conversations avec le tuteur intelligent"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    titre = models.CharField(max_length=200)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.titre}"


class Message(models.Model):
    """Messages dans une conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=[('user', 'Élève'), ('assistant', 'Tuteur')])
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.contenu[:50]}"



