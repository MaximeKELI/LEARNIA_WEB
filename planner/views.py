from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Examen, RevisionPlanifiee, Rappel
from accounts.models import Matiere, Chapitre


@login_required
def planner_index(request):
    """Page principale du planificateur"""
    examens = Examen.objects.filter(user=request.user, date_examen__gte=timezone.now())[:10]
    revisions = RevisionPlanifiee.objects.filter(
        user=request.user,
        date_revision__gte=timezone.now(),
        terminee=False
    )[:10]
    rappels = Rappel.objects.filter(
        user=request.user,
        date_rappel__gte=timezone.now(),
        envoye=False
    )[:5]
    
    return render(request, 'planner/index.html', {
        'examens': examens,
        'revisions': revisions,
        'rappels': rappels,
    })


@login_required
def create_examen(request):
    """Crée un examen"""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        matiere_id = request.POST.get('matiere_id')
        date_examen = request.POST.get('date_examen')
        description = request.POST.get('description', '')
        
        matiere = Matiere.objects.get(id=matiere_id)
        
        Examen.objects.create(
            user=request.user,
            nom=nom,
            matiere=matiere,
            date_examen=date_examen,
            description=description
        )
        
        return redirect('planner:index')
    
    matieres = Matiere.objects.all()
    return render(request, 'planner/create_examen.html', {'matieres': matieres})


@login_required
def create_revision(request):
    """Crée une révision planifiée"""
    if request.method == 'POST':
        chapitre_id = request.POST.get('chapitre_id')
        date_revision = request.POST.get('date_revision')
        duree = request.POST.get('duree_prevue_minutes', 30)
        type_revision = request.POST.get('type_revision', 'lecture')
        
        chapitre = Chapitre.objects.get(id=chapitre_id)
        
        RevisionPlanifiee.objects.create(
            user=request.user,
            chapitre=chapitre,
            date_revision=date_revision,
            duree_prevue_minutes=duree,
            type_revision=type_revision
        )
        
        return redirect('planner:index')
    
    chapitres = Chapitre.objects.all()
    return render(request, 'planner/create_revision.html', {'chapitres': chapitres})


@login_required
def mark_revision_done(request, revision_id):
    """Marque une révision comme terminée"""
    revision = get_object_or_404(RevisionPlanifiee, id=revision_id, user=request.user)
    revision.terminee = True
    revision.save()
    return redirect('planner:index')


@login_required
def generate_plan(request):
    """Génère un plan de révision intelligent"""
    if request.method == 'POST':
        examen_id = request.POST.get('examen_id')
        examen = get_object_or_404(Examen, id=examen_id, user=request.user)
        
        # Générer un plan de révision basé sur la date de l'examen
        jours_avant_examen = (examen.date_examen.date() - timezone.now().date()).days
        
        if jours_avant_examen > 0:
            # Créer des révisions espacées
            chapitres = Chapitre.objects.filter(matiere=examen.matiere)
            nombre_chapitres = chapitres.count()
            
            if nombre_chapitres > 0:
                jours_par_chapitre = max(1, jours_avant_examen // nombre_chapitres)
                
                for i, chapitre in enumerate(chapitres):
                    date_revision = timezone.now() + timedelta(days=i * jours_par_chapitre)
                    
                    RevisionPlanifiee.objects.get_or_create(
                        user=request.user,
                        chapitre=chapitre,
                        date_revision=date_revision,
                        defaults={
                            'duree_prevue_minutes': 45,
                            'type_revision': 'qcm'
                        }
                    )
        
        return redirect('planner:index')
    
    examens = Examen.objects.filter(user=request.user, date_examen__gte=timezone.now())
    return render(request, 'planner/generate_plan.html', {'examens': examens})



