from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Badge(models.Model):
    """Badge disponible dans le système"""
    nom = models.CharField(max_length=100)
    description = models.TextField()
    icone = models.CharField(max_length=50, default='🏆')
    couleur = models.CharField(max_length=20, default='gold')
    condition_type = models.CharField(
        max_length=50,
        choices=[
            ('qcm_first', 'Premier QCM complété'),
            ('qcm_perfect', 'QCM parfait (100%)'),
            ('qcm_10', '10 QCM complétés'),
            ('qcm_50', '50 QCM complétés'),
            ('flashcard_10', '10 Flashcards créées'),
            ('flashcard_50', '50 Flashcards créées'),
            ('flashcard_perfect', 'Session flashcards parfaite'),
            ('study_streak_3', '3 jours consécutifs'),
            ('study_streak_7', '7 jours consécutifs'),
            ('study_streak_30', '30 jours consécutifs'),
            ('tutor_10', '10 questions au tuteur'),
            ('profile_complete', 'Profil complet'),
            ('first_resume', 'Premier résumé créé'),
        ]
    )
    points_xp = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['points_xp']

    def __str__(self):
        return self.nom


class UserBadge(models.Model):
    """Badge obtenu par un utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges_obtenus')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='utilisateurs')
    obtenu_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-obtenu_le']

    def __str__(self):
        return f"{self.user.username} - {self.badge.nom}"


class UserProgress(models.Model):
    """Progression et points XP de l'utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='progress')
    points_xp = models.IntegerField(default=0)
    niveau = models.IntegerField(default=1)
    jours_streak = models.IntegerField(default=0)
    dernier_activite = models.DateField(null=True, blank=True)
    qcm_completes = models.IntegerField(default=0)
    flashcards_creees = models.IntegerField(default=0)
    questions_tuteur = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Niveau {self.niveau} ({self.points_xp} XP)"

    def ajouter_xp(self, points):
        """Ajoute des points XP et met à jour le niveau"""
        self.points_xp += points
        # Calcul du niveau (100 XP par niveau)
        self.niveau = (self.points_xp // 100) + 1
        self.save()

    def verifier_badges(self):
        """Vérifie et attribue les badges automatiquement"""
        badges_obtenus = UserBadge.objects.filter(user=self.user).values_list('badge_id', flat=True)
        
        # Vérifier chaque badge disponible
        for badge in Badge.objects.exclude(id__in=badages_obtenus):
            attribue = False
            
            if badge.condition_type == 'qcm_first' and self.qcm_completes >= 1:
                attribue = True
            elif badge.condition_type == 'qcm_10' and self.qcm_completes >= 10:
                attribue = True
            elif badge.condition_type == 'qcm_50' and self.qcm_completes >= 50:
                attribue = True
            elif badge.condition_type == 'flashcard_10' and self.flashcards_creees >= 10:
                attribue = True
            elif badge.condition_type == 'flashcard_50' and self.flashcards_creees >= 50:
                attribue = True
            elif badge.condition_type == 'study_streak_3' and self.jours_streak >= 3:
                attribue = True
            elif badge.condition_type == 'study_streak_7' and self.jours_streak >= 7:
                attribue = True
            elif badge.condition_type == 'study_streak_30' and self.jours_streak >= 30:
                attribue = True
            elif badge.condition_type == 'tutor_10' and self.questions_tuteur >= 10:
                attribue = True
            
            if attribue:
                UserBadge.objects.create(user=self.user, badge=badge)
                self.ajouter_xp(badge.points_xp)


class Leaderboard(models.Model):
    """Classement des utilisateurs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classements')
    position = models.IntegerField()
    score = models.IntegerField()
    periode = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Quotidien'),
            ('weekly', 'Hebdomadaire'),
            ('monthly', 'Mensuel'),
            ('all_time', 'Tous les temps'),
        ]
    )
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['periode', 'position']
        unique_together = ['user', 'periode', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.position}ème ({self.periode})"


