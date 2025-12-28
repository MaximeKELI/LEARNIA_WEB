import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message
from .services import TuteurService
from accounts.models import Chapitre


@login_required
def tutor_index(request):
    """Page principale du tuteur"""
    conversations = Conversation.objects.filter(user=request.user)[:10]
    chapitres = Chapitre.objects.filter(matiere__niveau__in=['college', 'lycee'])[:20]
    return render(request, 'tutor/index.html', {
        'conversations': conversations,
        'chapitres': chapitres,
    })


@login_required
def conversation_detail(request, conversation_id):
    """Détails d'une conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()
    return render(request, 'tutor/conversation.html', {
        'conversation': conversation,
        'messages': messages,
    })


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """Envoyer un message au tuteur"""
    data = json.loads(request.body)
    message_text = data.get('message', '')
    conversation_id = data.get('conversation_id')
    chapitre_id = data.get('chapitre_id')

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    else:
        # Créer une nouvelle conversation
        titre = message_text[:50] if len(message_text) > 50 else message_text
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        conversation = Conversation.objects.create(
            user=request.user,
            titre=titre,
            chapitre=chapitre
        )

    # Sauvegarder le message de l'utilisateur
    Message.objects.create(
        conversation=conversation,
        role='user',
        contenu=message_text
    )

    # Générer la réponse du tuteur
    tuteur_service = TuteurService()
    response = tuteur_service.get_response(message_text, conversation.chapitre, request.user)

    # Sauvegarder la réponse
    Message.objects.create(
        conversation=conversation,
        role='assistant',
        contenu=response
    )

    return JsonResponse({
        'response': response,
        'conversation_id': conversation.id
    })


@login_required
def new_conversation(request):
    """Créer une nouvelle conversation"""
    if request.method == 'POST':
        titre = request.POST.get('titre', 'Nouvelle conversation')
        chapitre_id = request.POST.get('chapitre_id')
        chapitre = Chapitre.objects.get(id=chapitre_id) if chapitre_id else None
        conversation = Conversation.objects.create(
            user=request.user,
            titre=titre,
            chapitre=chapitre
        )
        return redirect('tutor:conversation_detail', conversation_id=conversation.id)
    return redirect('tutor:index')

