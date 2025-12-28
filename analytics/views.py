from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import Performance, Activite
from qcm.models import ResultatQCM
from flashcards.models import Revision
from accounts.models import Matiere


@login_required
def analytics_index(request):
    """Page principale des analyses"""
    performances = Performance.objects.filter(user=request.user)
    
    # Statistiques générales
    total_qcm = ResultatQCM.objects.filter(user=request.user).count()
    score_moyen_qcm = ResultatQCM.objects.filter(user=request.user).aggregate(
        avg_score=models.Avg('pourcentage')
    )['avg_score'] or 0
    
    total_flashcards = Revision.objects.filter(user=request.user).count()
    flashcards_reussies = Revision.objects.filter(user=request.user, reussie=True).count()
    taux_reussite = (flashcards_reussies / total_flashcards * 100) if total_flashcards > 0 else 0
    
    activites_recentes = Activite.objects.filter(user=request.user)[:10]
    
    # Données pour graphiques (évolution temporelle)
    resultats_par_mois = []
    for i in range(6):  # 6 derniers mois
        mois = timezone.now().replace(day=1) - timedelta(days=30*i)
        resultats_mois = ResultatQCM.objects.filter(
            user=request.user,
            created_at__year=mois.year,
            created_at__month=mois.month
        )
        if resultats_mois.exists():
            score_moyen = sum(r.pourcentage for r in resultats_mois) / resultats_mois.count()
            resultats_par_mois.append({
                'mois': mois.strftime('%Y-%m'),
                'score': round(score_moyen, 2),
                'nombre': resultats_mois.count()
            })
    
    resultats_par_mois.reverse()
    
    # Gamification stats
    from gamification.models import UserProgress
    progress = None
    try:
        progress = UserProgress.objects.get(user=request.user)
    except:
        pass
    
    return render(request, 'analytics/index.html', {
        'performances': performances,
        'total_qcm': total_qcm,
        'score_moyen_qcm': round(score_moyen_qcm, 2),
        'total_flashcards': total_flashcards,
        'taux_reussite': round(taux_reussite, 2),
        'activites_recentes': activites_recentes,
        'resultats_par_mois': resultats_par_mois,
        'progress': progress,
    })


@login_required
def performance_detail(request, matiere_id):
    """Détails des performances par matière"""
    
    matiere = Matiere.objects.get(id=matiere_id)
    
    # Résultats QCM pour cette matière
    resultats_qcm = ResultatQCM.objects.filter(
        user=request.user,
        qcm__chapitre__matiere=matiere
    ).order_by('-created_at')[:20]
    
    # Révisions flashcards
    revisions = Revision.objects.filter(
        user=request.user,
        flashcard__deck__chapitre__matiere=matiere
    ).order_by('-created_at')[:20]
    
    return render(request, 'analytics/performance_detail.html', {
        'matiere': matiere,
        'resultats_qcm': resultats_qcm,
        'revisions': revisions,
    })

