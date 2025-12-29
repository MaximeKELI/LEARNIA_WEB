from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Questionnaire, Filiere, Metier
from .services import OrientationService


@login_required
def orientation_index(request):
    """Page principale d'orientation"""
    questionnaires = Questionnaire.objects.filter(user=request.user)[:5]
    filieres = Filiere.objects.all()
    return render(request, 'orientation/index.html', {
        'questionnaires': questionnaires,
        'filieres': filieres,
    })


@login_required
def questionnaire(request):
    """Questionnaire d'orientation"""
    if request.method == 'POST':
        # Récupérer les réponses
        reponses = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                reponses[key] = value
        
        # Analyser les réponses
        service = OrientationService()
        analyse = service.analyser_questionnaire(reponses)
        
        # Créer le questionnaire
        questionnaire_obj = Questionnaire.objects.create(
            user=request.user,
            reponses=reponses,
            score_scientifique=analyse['scores']['scientifique'],
            score_litteraire=analyse['scores']['litteraire'],
            score_commercial=analyse['scores']['commercial'],
            score_technique=analyse['scores']['technique'],
            filiere_suggeree=analyse['filiere']['nom'],
            metiers_suggestes=analyse['filiere']['metiers']
        )
        
        return redirect('orientation:resultat', questionnaire_id=questionnaire_obj.id)
    
    return render(request, 'orientation/questionnaire.html')


@login_required
def resultat(request, questionnaire_id):
    """Résultat du questionnaire"""
    questionnaire_obj = Questionnaire.objects.get(id=questionnaire_id, user=request.user)
    return render(request, 'orientation/resultat.html', {
        'questionnaire': questionnaire_obj,
    })


@login_required
def filieres(request):
    """Liste des filières"""
    filieres = Filiere.objects.all()
    return render(request, 'orientation/filieres.html', {'filieres': filieres})


@login_required
def metiers(request):
    """Liste des métiers"""
    metiers = Metier.objects.all()
    return render(request, 'orientation/metiers.html', {'metiers': metiers})


