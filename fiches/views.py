from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from .models import FicheRevision
from .services import FichePDFGenerator
from accounts.models import Chapitre
from flashcards.models import Deck


@login_required
def fiches_list(request):
    """Liste des fiches"""
    fiches = FicheRevision.objects.filter(user=request.user)
    return render(request, 'fiches/list.html', {'fiches': fiches})


@login_required
def fiche_create(request):
    """Créer une fiche"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        chapitre_id = request.POST.get('chapitre_id')
        couleur_titre = request.POST.get('couleur_titre', '#007bff')
        police = request.POST.get('police', 'Arial')
        
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        fiche = FicheRevision.objects.create(
            user=request.user,
            titre=titre,
            contenu=contenu,
            chapitre=chapitre,
            couleur_titre=couleur_titre,
            police=police
        )
        
        messages.success(request, 'Fiche créée avec succès.')
        return redirect('fiches:list')
    
    chapitres = Chapitre.objects.all()
    return render(request, 'fiches/form.html', {
        'chapitres': chapitres,
        'action': 'Créer',
    })


@login_required
def fiche_from_chapitre(request, chapitre_id):
    """Générer une fiche depuis un chapitre"""
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre', f"Fiche - {chapitre.titre}")
        
        buffer = FichePDFGenerator.generate_from_chapitre(chapitre, request.user, titre)
        
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="fiche_{chapitre.titre.replace(' ', '_')}_{datetime.now().strftime("%Y%m%d")}.pdf"'
        return response
    
    return render(request, 'fiches/from_chapitre.html', {'chapitre': chapitre})


@login_required
def fiche_from_deck(request, deck_id):
    """Générer une fiche depuis un deck"""
    deck = get_object_or_404(Deck, id=deck_id, user=request.user)
    
    buffer = FichePDFGenerator.generate_from_flashcards(deck, request.user)
    
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_flashcards_{deck.titre.replace(' ', '_')}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    return response


@login_required
def fiche_download(request, fiche_id):
    """Télécharger une fiche en PDF"""
    from datetime import datetime
    fiche = get_object_or_404(FicheRevision, id=fiche_id, user=request.user)
    
    buffer = FichePDFGenerator.generate_fiche(fiche)
    
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_{fiche.titre.replace(' ', '_')}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    return response


@login_required
def fiche_delete(request, fiche_id):
    """Supprimer une fiche"""
    fiche = get_object_or_404(FicheRevision, id=fiche_id, user=request.user)
    
    if request.method == 'POST':
        fiche.delete()
        messages.success(request, 'Fiche supprimée avec succès.')
        return redirect('fiches:list')
    
    return render(request, 'fiches/delete.html', {'fiche': fiche})

