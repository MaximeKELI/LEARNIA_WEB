from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import QCM, Question, Choix, ResultatQCM
from .services import QCMGenerator
from accounts.models import Chapitre


@login_required
def qcm_index(request):
    """Page principale des QCM"""
    qcms = QCM.objects.filter(user=request.user)[:10]
    chapitres = Chapitre.objects.all()[:20]
    return render(request, 'qcm/index.html', {
        'qcms': qcms,
        'chapitres': chapitres,
    })


@login_required
def generate_qcm(request):
    """Génère un QCM à partir d'un texte"""
    if request.method == 'POST':
        texte = request.POST.get('texte_source', '')
        titre = request.POST.get('titre', 'Nouveau QCM')
        chapitre_id = request.POST.get('chapitre_id')
        
        if not texte:
            return redirect('qcm:index')
        
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        # Créer le QCM
        qcm = QCM.objects.create(
            user=request.user,
            titre=titre,
            chapitre=chapitre,
            texte_source=texte
        )
        
        # Générer les questions
        generator = QCMGenerator()
        questions_data = generator.generate_questions(texte, nombre_questions=5)
        
        # Créer les questions et choix
        for q_data in questions_data:
            question = Question.objects.create(
                qcm=qcm,
                texte=q_data['texte'],
                numero=q_data['numero']
            )
            
            for choix_data in q_data['choix']:
                Choix.objects.create(
                    question=question,
                    texte=choix_data['texte'],
                    est_correct=choix_data['correct']
                )
        
        return redirect('qcm:detail', qcm_id=qcm.id)
    
    chapitres = Chapitre.objects.all()
    return render(request, 'qcm/generate.html', {'chapitres': chapitres})


@login_required
def qcm_detail(request, qcm_id):
    """Détails d'un QCM"""
    qcm = get_object_or_404(QCM, id=qcm_id, user=request.user)
    questions = qcm.questions.all()
    return render(request, 'qcm/detail.html', {
        'qcm': qcm,
        'questions': questions,
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def submit_qcm(request, qcm_id):
    """Soumet les réponses d'un QCM"""
    qcm = get_object_or_404(QCM, id=qcm_id, user=request.user)
    data = json.loads(request.body)
    reponses = data.get('reponses', {})
    
    score = 0
    total = qcm.questions.count()
    
    # Vérifier les réponses
    for question_id, choix_id in reponses.items():
        question = Question.objects.get(id=question_id)
        choix = Choix.objects.get(id=choix_id)
        if choix.est_correct:
            score += 1
    
    pourcentage = (score / total * 100) if total > 0 else 0
    
    # Sauvegarder le résultat
    ResultatQCM.objects.create(
        user=request.user,
        qcm=qcm,
        score=score,
        total=total,
        pourcentage=pourcentage
    )
    
    return JsonResponse({
        'score': score,
        'total': total,
        'pourcentage': round(pourcentage, 2),
        'message': f"Score : {score}/{total} ({round(pourcentage, 2)}%)"
    })

