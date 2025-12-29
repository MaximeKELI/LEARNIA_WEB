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
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    
    reponses = data.get('reponses', {})
    
    if not reponses:
        return JsonResponse({'error': 'Aucune réponse fournie'}, status=400)
    
    score = 0
    total = qcm.questions.count()
    resultats_questions = []  # Pour stocker les détails de chaque question
    
    # Vérifier les réponses
    for key, choix_id in reponses.items():
        try:
            # Gérer deux formats possibles :
            # 1. Clé numérique directe : "1" -> 1
            # 2. Clé avec préfixe : "question_1" -> 1
            if isinstance(key, str) and key.startswith('question_'):
                question_id = int(key.replace('question_', ''))
            else:
                question_id = int(key)
            
            question = Question.objects.get(id=question_id, qcm=qcm)
            choix_selectionne = Choix.objects.get(id=int(choix_id), question=question)
            choix_correct = question.choix.filter(est_correct=True).first()
            
            est_correct = choix_selectionne.est_correct
            if est_correct:
                score += 1
            
            resultats_questions.append({
                'question_id': question_id,
                'question_texte': question.texte,
                'choix_selectionne_id': choix_selectionne.id,
                'choix_selectionne_texte': choix_selectionne.texte,
                'choix_correct_id': choix_correct.id if choix_correct else None,
                'choix_correct_texte': choix_correct.texte if choix_correct else '',
                'est_correct': est_correct
            })
        except (ValueError, Question.DoesNotExist, Choix.DoesNotExist) as e:
            # Ignorer les réponses invalides
            continue
    
    # Ajouter les questions sans réponse
    questions_avec_reponse = {r['question_id'] for r in resultats_questions}
    for question in qcm.questions.all():
        if question.id not in questions_avec_reponse:
            choix_correct = question.choix.filter(est_correct=True).first()
            resultats_questions.append({
                'question_id': question.id,
                'question_texte': question.texte,
                'choix_selectionne_id': None,
                'choix_selectionne_texte': None,
                'choix_correct_id': choix_correct.id if choix_correct else None,
                'choix_correct_texte': choix_correct.texte if choix_correct else '',
                'est_correct': False
            })
    
    pourcentage = (score / total * 100) if total > 0 else 0
    
    # Sauvegarder le résultat
    ResultatQCM.objects.create(
        user=request.user,
        qcm=qcm,
        score=score,
        total=total,
        pourcentage=pourcentage
    )
    
    # Ajouter des points XP via la gamification
    try:
        from gamification.services import GamificationService
        GamificationService.ajouter_xp_qcm(request.user, pourcentage)
    except:
        pass  # Si la gamification n'est pas disponible
    
    return JsonResponse({
        'score': score,
        'total': total,
        'pourcentage': round(pourcentage, 2),
        'message': f"Score : {score}/{total} ({round(pourcentage, 2)}%)",
        'resultats': resultats_questions
    })

