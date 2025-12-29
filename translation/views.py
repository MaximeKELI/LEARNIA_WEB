from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Traduction
from .services import TranslationService


@login_required
def translation_index(request):
    """Page principale de traduction"""
    traductions = Traduction.objects.filter(user=request.user)[:10]
    return render(request, 'translation/index.html', {'traductions': traductions})


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def translate_text(request):
    """Traduit un texte"""
    data = json.loads(request.body)
    texte = data.get('texte', '')
    langue_cible = data.get('langue_cible', 'ewe')
    langue_originale = data.get('langue_originale', 'fr')
    
    if not texte:
        return JsonResponse({'error': 'Texte requis'}, status=400)
    
    service = TranslationService()
    texte_traduit = service.translate(texte, langue_cible)
    
    # Sauvegarder la traduction
    Traduction.objects.create(
        user=request.user,
        texte_original=texte,
        langue_originale=langue_originale,
        langue_cible=langue_cible,
        texte_traduit=texte_traduit
    )
    
    return JsonResponse({
        'texte_traduit': texte_traduit,
        'langue_cible': langue_cible
    })


@login_required
def dictionary(request):
    """Dictionnaire"""
    service = TranslationService()
    mots = list(service.DICTIONNAIRE.keys())
    return render(request, 'translation/dictionary.html', {'mots': mots})


