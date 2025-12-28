from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
from .services import ResumeService
from accounts.models import Chapitre


@login_required
def resume_index(request):
    """Page principale des résumés"""
    resumes = Resume.objects.filter(user=request.user)[:10]
    return render(request, 'resume/index.html', {'resumes': resumes})


@login_required
def generate_resume(request):
    """Génère un résumé à partir d'un texte"""
    if request.method == 'POST':
        texte = request.POST.get('texte_original', '')
        titre = request.POST.get('titre', 'Nouveau résumé')
        chapitre_id = request.POST.get('chapitre_id')
        
        if not texte:
            return redirect('resume:index')
        
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        # Générer le résumé
        service = ResumeService()
        resume_texte = service.generate_resume(texte)
        points_cles = service.extraire_points_cles(texte)
        
        # Créer le résumé
        resume_obj = Resume.objects.create(
            user=request.user,
            titre=titre,
            chapitre=chapitre,
            texte_original=texte,
            resume_texte=resume_texte,
            points_cles=points_cles
        )
        
        return redirect('resume:detail', resume_id=resume_obj.id)
    
    chapitres = Chapitre.objects.all()
    return render(request, 'resume/generate.html', {'chapitres': chapitres})


@login_required
def resume_detail(request, resume_id):
    """Détails d'un résumé"""
    resume = Resume.objects.get(id=resume_id, user=request.user)
    return render(request, 'resume/detail.html', {'resume': resume})

