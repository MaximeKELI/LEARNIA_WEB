from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import UserProgress, UserBadge, Badge
from .services import GamificationService

User = get_user_model()


@login_required
def gamification_dashboard(request):
    """Tableau de bord de gamification"""
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    badges_obtenus = UserBadge.objects.filter(user=request.user).select_related('badge')
    badges_disponibles = Badge.objects.exclude(
        id__in=badges_obtenus.values_list('badge_id', flat=True)
    )
    
    # Progression vers le prochain niveau
    xp_actuel = progress.points_xp
    xp_niveau_actuel = (progress.niveau - 1) * 100
    xp_prochain_niveau = progress.niveau * 100
    xp_progression = xp_actuel - xp_niveau_actuel
    xp_needed = xp_prochain_niveau - xp_actuel
    pourcentage = (xp_progression / (xp_prochain_niveau - xp_niveau_actuel)) * 100
    
    # Classement
    leaderboard = GamificationService.get_leaderboard(limit=10)
    user_position = None
    for i, entry in enumerate(leaderboard, 1):
        if entry['user'].id == request.user.id:
            user_position = i
            break
    
    return render(request, 'gamification/dashboard.html', {
        'progress': progress,
        'badges_obtenus': badges_obtenus,
        'badges_disponibles': badges_disponibles,
        'pourcentage': round(pourcentage, 2),
        'xp_needed': xp_needed,
        'leaderboard': leaderboard,
        'user_position': user_position,
    })


@login_required
def badges_list(request):
    """Liste de tous les badges"""
    badges = Badge.objects.all()
    badges_obtenus_ids = UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True)
    
    badges_data = []
    for badge in badges:
        obtenu = badge.id in badges_obtenus_ids
        badges_data.append({
            'badge': badge,
            'obtenu': obtenu,
        })
    
    return render(request, 'gamification/badges.html', {
        'badges_data': badges_data,
    })

