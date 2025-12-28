from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
from .models import Deck, Flashcard, Revision
from accounts.models import Chapitre


@login_required
def flashcards_index(request):
    """Page principale des flashcards"""
    decks = Deck.objects.filter(user=request.user)
    return render(request, 'flashcards/index.html', {'decks': decks})


@login_required
def deck_detail(request, deck_id):
    """Détails d'un deck"""
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    flashcards = deck.flashcards.all()
    return render(request, 'flashcards/deck_detail.html', {
        'deck': deck,
        'flashcards': flashcards,
    })


@login_required
def create_deck(request):
    """Crée un nouveau deck"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        chapitre_id = request.POST.get('chapitre_id')
        
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        deck = Deck.objects.create(
            user=request.user,
            titre=titre,
            description=description,
            chapitre=chapitre
        )
        
        return redirect('flashcards:deck_detail', deck_id=deck.id)
    
    chapitres = Chapitre.objects.all()
    return render(request, 'flashcards/create_deck.html', {'chapitres': chapitres})


@login_required
def add_flashcard(request, deck_id):
    """Ajoute une flashcard à un deck"""
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    if request.method == 'POST':
        recto = request.POST.get('recto')
        verso = request.POST.get('verso')
        
        Flashcard.objects.create(
            deck=deck,
            recto=recto,
            verso=verso
        )
        
        # Ajouter des points XP via la gamification
        try:
            from gamification.services import GamificationService
            GamificationService.ajouter_xp_flashcard(request.user)
        except:
            pass
        
        return redirect('flashcards:deck_detail', deck_id=deck.id)
    
    return render(request, 'flashcards/add_flashcard.html', {'deck': deck})


@login_required
def review_deck(request, deck_id):
    """Révision d'un deck avec système Leitner"""
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    # Obtenir les cartes à réviser (prochaine_revision <= maintenant)
    flashcards = deck.flashcards.filter(prochaine_revision__lte=timezone.now())[:10]
    
    if not flashcards.exists():
        # Si aucune carte à réviser, prendre les plus anciennes
        flashcards = deck.flashcards.all()[:10]
    
    return render(request, 'flashcards/review.html', {
        'deck': deck,
        'flashcards': flashcards,
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_revision(request, flashcard_id):
    """Marque une révision comme réussie ou échouée"""
    flashcard = get_object_or_404(Flashcard, id=flashcard_id, deck__user=request.user)
    data = json.loads(request.body)
    reussie = data.get('reussie', False)
    temps_reponse = data.get('temps_reponse', 0)
    
    # Enregistrer la révision
    Revision.objects.create(
        user=request.user,
        flashcard=flashcard,
        reussie=reussie,
        temps_reponse=temps_reponse
    )
    
    # Mettre à jour la flashcard
    if reussie:
        flashcard.marquer_success()
    else:
        flashcard.marquer_echec()
    
    return JsonResponse({'success': True})

