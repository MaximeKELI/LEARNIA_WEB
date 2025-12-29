"""
Services pour la gamification
"""
from django.utils import timezone
from datetime import timedelta
from .models import UserProgress, UserBadge, Badge


class GamificationService:
    """Service pour gérer la gamification"""
    
    @staticmethod
    def mettre_a_jour_streak(user):
        """Met à jour la série de jours consécutifs"""
        progress, created = UserProgress.objects.get_or_create(user=user)
        today = timezone.now().date()
        
        if progress.dernier_activite:
            jours_diff = (today - progress.dernier_activite).days
            
            if jours_diff == 0:
                # Déjà mis à jour aujourd'hui
                return
            elif jours_diff == 1:
                # Jour consécutif
                progress.jours_streak += 1
                progress.ajouter_xp(5)  # Bonus streak
            else:
                # Série cassée
                progress.jours_streak = 1
        
        progress.dernier_activite = today
        progress.save()
        progress.verifier_badges()
    
    @staticmethod
    def ajouter_xp_qcm(user, score_percentage):
        """Ajoute des XP après un QCM"""
        progress, created = UserProgress.objects.get_or_create(user=user)
        progress.qcm_completes += 1
        
        # Points basés sur le score
        if score_percentage >= 100:
            points = 50  # QCM parfait
            # Vérifier badge QCM parfait
            badge = Badge.objects.filter(condition_type='qcm_perfect').first()
            if badge:
                UserBadge.objects.get_or_create(user=user, badge=badge)
        elif score_percentage >= 80:
            points = 30
        elif score_percentage >= 60:
            points = 20
        else:
            points = 10
        
        progress.ajouter_xp(points)
        progress.save()
        progress.verifier_badges()
        GamificationService.mettre_a_jour_streak(user)
    
    @staticmethod
    def ajouter_xp_flashcard(user):
        """Ajoute des XP après création d'une flashcard"""
        progress, created = UserProgress.objects.get_or_create(user=user)
        progress.flashcards_creees += 1
        progress.ajouter_xp(5)
        progress.save()
        progress.verifier_badges()
    
    @staticmethod
    def ajouter_xp_tuteur(user):
        """Ajoute des XP après une question au tuteur"""
        progress, created = UserProgress.objects.get_or_create(user=user)
        progress.questions_tuteur += 1
        progress.ajouter_xp(3)
        progress.save()
        progress.verifier_badges()
    
    @staticmethod
    def get_leaderboard(periode='all_time', limit=10):
        """Récupère le classement"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        progresses = UserProgress.objects.all().order_by('-points_xp')[:limit]
        
        leaderboard = []
        position = 1
        for progress in progresses:
            leaderboard.append({
                'position': position,
                'user': progress.user,
                'points_xp': progress.points_xp,
                'niveau': progress.niveau,
                'badges_count': UserBadge.objects.filter(user=progress.user).count()
            })
            position += 1
        
        return leaderboard


