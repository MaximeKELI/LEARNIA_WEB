"""
Tests unitaires pour l'application tutor
Tests backend
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre
from .models import Conversation, Message
from .services import TuteurService
import json

User = get_user_model()


class TuteurServiceTest(TestCase):
    """Tests pour le service TuteurService"""
    
    def setUp(self):
        self.service = TuteurService()
    
    def test_get_response_bonjour(self):
        """Test la réponse à une salutation"""
        response = self.service.get_response('Bonjour', None, None)
        self.assertIn('Bonjour', response)
    
    def test_get_response_maths(self):
        """Test la réponse à une question de mathématiques"""
        response = self.service.get_response('Comment résoudre une équation ?', None, None)
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 0)
    
    def test_get_response_with_chapitre(self):
        """Test la réponse avec un chapitre"""
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        chapitre = Chapitre.objects.create(
            matiere=matiere,
            titre='Les équations',
            numero=1,
            contenu='Contenu sur les équations'
        )
        response = self.service.get_response('Explique-moi ce chapitre', chapitre, None)
        self.assertIsNotNone(response)
        self.assertIn('équations', response.lower())


class ConversationModelTest(TestCase):
    """Tests pour les modèles de conversation"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        self.chapitre = Chapitre.objects.create(
            matiere=self.matiere,
            titre='Les équations',
            numero=1,
            contenu='Contenu'
        )
    
    def test_create_conversation(self):
        """Test la création d'une conversation"""
        conversation = Conversation.objects.create(
            user=self.user,
            titre='Conversation Test',
            chapitre=self.chapitre
        )
        self.assertEqual(conversation.titre, 'Conversation Test')
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.chapitre, self.chapitre)
    
    def test_create_message(self):
        """Test la création d'un message"""
        conversation = Conversation.objects.create(
            user=self.user,
            titre='Conversation Test'
        )
        message = Message.objects.create(
            conversation=conversation,
            role='user',
            contenu='Bonjour'
        )
        self.assertEqual(message.role, 'user')
        self.assertEqual(message.contenu, 'Bonjour')
    
    def test_conversation_messages_relation(self):
        """Test la relation entre conversation et messages"""
        conversation = Conversation.objects.create(
            user=self.user,
            titre='Conversation Test'
        )
        Message.objects.create(
            conversation=conversation,
            role='user',
            contenu='Question'
        )
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            contenu='Réponse'
        )
        self.assertEqual(conversation.messages.count(), 2)


class TutorViewsTest(TestCase):
    """Tests pour les vues du tuteur"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_tutor_index_requires_login(self):
        """Test que l'index nécessite une connexion"""
        url = reverse('tutor:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_tutor_index_authenticated(self):
        """Test l'accès à l'index quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('tutor:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor/index.html')
    
    def test_send_message(self):
        """Test l'envoi d'un message"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('tutor:send_message')
        data = {
            'message': 'Bonjour, comment ça va ?'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('response', response_data)
        self.assertIn('conversation_id', response_data)


