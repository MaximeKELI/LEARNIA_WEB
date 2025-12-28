from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note, NoteVersion


@login_required
def notes_list(request):
    """Liste des notes"""
    notes = Note.objects.filter(user=request.user)
    
    # Filtres
    recherche = request.GET.get('q', '')
    favori_filter = request.GET.get('favori', '')
    tag_filter = request.GET.get('tag', '')
    
    if recherche:
        notes = notes.filter(
            Q(titre__icontains=recherche) | 
            Q(contenu__icontains=recherche) |
            Q(tags__icontains=recherche)
        )
    
    if favori_filter == 'true':
        notes = notes.filter(favori=True)
    
    if tag_filter:
        notes = notes.filter(tags__icontains=tag_filter)
    
    # Statistiques
    total_notes = Note.objects.filter(user=request.user).count()
    notes_favorites = Note.objects.filter(user=request.user, favori=True).count()
    
    # Tags utilisés
    all_tags = []
    for note in Note.objects.filter(user=request.user):
        all_tags.extend(note.get_tags_list())
    tags_uniques = sorted(set(all_tags))
    
    return render(request, 'notes/list.html', {
        'notes': notes,
        'total_notes': total_notes,
        'notes_favorites': notes_favorites,
        'tags': tags_uniques,
        'recherche': recherche,
        'tag_filter': tag_filter,
    })


@login_required
def note_detail(request, note_id):
    """Détail d'une note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    versions = note.versions.all()[:5]  # Dernières 5 versions
    
    return render(request, 'notes/detail.html', {
        'note': note,
        'versions': versions,
    })


@login_required
def note_create(request):
    """Créer une nouvelle note"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        chapitre_id = request.POST.get('chapitre_id')
        tags = request.POST.get('tags', '')
        favori = request.POST.get('favori') == 'on'
        
        from accounts.models import Chapitre
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        note = Note.objects.create(
            user=request.user,
            titre=titre,
            contenu=contenu,
            chapitre=chapitre,
            tags=tags,
            favori=favori
        )
        
        # Sauvegarder la version initiale
        NoteVersion.objects.create(note=note, contenu=contenu)
        
        messages.success(request, 'Note créée avec succès.')
        return redirect('notes:detail', note_id=note.id)
    
    from accounts.models import Chapitre
    chapitres = Chapitre.objects.all()
    return render(request, 'notes/form.html', {
        'chapitres': chapitres,
        'action': 'Créer',
    })


@login_required
def note_edit(request, note_id):
    """Modifier une note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        note.titre = request.POST.get('titre')
        note.contenu = request.POST.get('contenu')
        chapitre_id = request.POST.get('chapitre_id')
        note.tags = request.POST.get('tags', '')
        note.favori = request.POST.get('favori') == 'on'
        
        from accounts.models import Chapitre
        note.chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        
        # Sauvegarder la version précédente
        NoteVersion.objects.create(note=note, contenu=note.contenu)
        
        note.save()
        messages.success(request, 'Note modifiée avec succès.')
        return redirect('notes:detail', note_id=note.id)
    
    from accounts.models import Chapitre
    chapitres = Chapitre.objects.all()
    return render(request, 'notes/form.html', {
        'note': note,
        'chapitres': chapitres,
        'action': 'Modifier',
    })


@login_required
def note_delete(request, note_id):
    """Supprimer une note"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note supprimée avec succès.')
        return redirect('notes:list')
    
    return render(request, 'notes/delete.html', {'note': note})


@login_required
def note_toggle_favorite(request, note_id):
    """Basculer le statut favori"""
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.favori = not note.favori
    note.save()
    
    return redirect('notes:list')

