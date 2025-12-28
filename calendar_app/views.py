from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models as db_models
from datetime import datetime, timedelta
from .models import EvenementScolaire


@login_required
def calendar_view(request):
    """Vue calendrier"""
    # Récupérer le mois/année depuis les paramètres
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Événements personnels
    evenements = EvenementScolaire.objects.filter(
        db_models.Q(user=request.user) | db_models.Q(public=True)
    ).filter(
        date_debut__year=year,
        date_debut__month=month
    )
    
    # Événements à venir (7 prochains jours)
    date_aujourdhui = timezone.now().date()
    prochains_evenements = EvenementScolaire.objects.filter(
        db_models.Q(user=request.user) | db_models.Q(public=True)
    ).filter(
        date_debut__gte=date_aujourdhui
    ).order_by('date_debut')[:10]
    
    # Statistiques
    evenements_ce_mois = evenements.count()
    evenements_ce_mois_user = evenements.filter(user=request.user).count()
    
    return render(request, 'calendar_app/calendar.html', {
        'year': year,
        'month': month,
        'evenements': evenements,
        'prochains_evenements': prochains_evenements,
        'evenements_ce_mois': evenements_ce_mois,
        'evenements_ce_mois_user': evenements_ce_mois_user,
    })


@login_required
def event_create(request):
    """Créer un événement"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description', '')
        type_evenement = request.POST.get('type_evenement', 'rappel')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        matiere_id = request.POST.get('matiere_id')
        couleur = request.POST.get('couleur', '#007bff')
        rappel_jours = int(request.POST.get('rappel_jours', 1))
        public = request.POST.get('public') == 'on'
        
        from accounts.models import Matiere
        matiere = Matiere.objects.get(id=matiere_id) if matiere_id else None
        
        evenement = EvenementScolaire.objects.create(
            user=request.user,
            titre=titre,
            description=description,
            type_evenement=type_evenement,
            date_debut=date_debut,
            date_fin=date_fin if date_fin else None,
            heure_debut=heure_debut if heure_debut else None,
            heure_fin=heure_fin if heure_fin else None,
            matiere=matiere,
            couleur=couleur,
            rappel_jours=rappel_jours,
            public=public
        )
        
        messages.success(request, 'Événement créé avec succès.')
        return redirect('calendar:view')
    
    from accounts.models import Matiere
    matieres = Matiere.objects.all()
    return render(request, 'calendar_app/form.html', {
        'matieres': matieres,
        'action': 'Créer',
    })


@login_required
def event_edit(request, event_id):
    """Modifier un événement"""
    evenement = get_object_or_404(EvenementScolaire, id=event_id, user=request.user)
    
    if request.method == 'POST':
        evenement.titre = request.POST.get('titre')
        evenement.description = request.POST.get('description', '')
        evenement.type_evenement = request.POST.get('type_evenement')
        evenement.date_debut = request.POST.get('date_debut')
        evenement.date_fin = request.POST.get('date_fin') or None
        evenement.heure_debut = request.POST.get('heure_debut') or None
        evenement.heure_fin = request.POST.get('heure_fin') or None
        matiere_id = request.POST.get('matiere_id')
        evenement.couleur = request.POST.get('couleur', '#007bff')
        evenement.rappel_jours = int(request.POST.get('rappel_jours', 1))
        evenement.public = request.POST.get('public') == 'on'
        
        from accounts.models import Matiere
        evenement.matiere = Matiere.objects.get(id=matiere_id) if matiere_id else None
        
        evenement.save()
        messages.success(request, 'Événement modifié avec succès.')
        return redirect('calendar:view')
    
    from accounts.models import Matiere
    matieres = Matiere.objects.all()
    return render(request, 'calendar_app/form.html', {
        'evenement': evenement,
        'matieres': matieres,
        'action': 'Modifier',
    })


@login_required
def event_delete(request, event_id):
    """Supprimer un événement"""
    evenement = get_object_or_404(EvenementScolaire, id=event_id, user=request.user)
    
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, 'Événement supprimé avec succès.')
        return redirect('calendar:view')
    
    return render(request, 'calendar_app/delete.html', {'evenement': evenement})

