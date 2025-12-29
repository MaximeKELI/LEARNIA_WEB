from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Devoir
from .services import OCRService


@login_required
def ocr_index(request):
    """Page principale OCR"""
    devoirs = Devoir.objects.filter(user=request.user)[:10]
    return render(request, 'ocr/index.html', {'devoirs': devoirs})


@login_required
def upload_devoir(request):
    """Upload un devoir manuscrit"""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        matiere = request.POST.get('matiere', '')
        
        # Créer le devoir
        devoir = Devoir.objects.create(
            user=request.user,
            image=image,
            matiere=matiere
        )
        
        # Extraire le texte
        service = OCRService()
        texte = service.extract_text(devoir.image.path)
        texte_corrige = service.correct_text(texte)
        
        devoir.texte_reconnu = texte_corrige
        
        # Analyser et noter (simulation)
        analyse = service.analyze_homework(texte_corrige)
        devoir.note = analyse['note']
        devoir.commentaires = analyse['commentaires']
        
        devoir.save()
        
        return redirect('ocr:devoir_detail', devoir_id=devoir.id)
    
    return render(request, 'ocr/upload.html')


@login_required
def devoir_detail(request, devoir_id):
    """Détails d'un devoir"""
    devoir = Devoir.objects.get(id=devoir_id, user=request.user)
    return render(request, 'ocr/devoir_detail.html', {'devoir': devoir})


