"""
Tests d'intégration pour vérifier que les fonctionnalités travaillent ensemble
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre
from qcm.models import QCM, Question, Choix, ResultatQCM
from flashcards.models import Deck, Flashcard
from gamification.models import UserProgress, Badge, UserBadge
from gamification.services import GamificationService

User = get_user_model()


class IntegrationGamificationTest(TestCase):
    """Tests d'intégration de la gamification avec les autres modules"""
    
    def setUp(self):
        self.client = Client()
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
        
        # Créer des badges
        Badge.objects.create(
            nom='Premier Pas',
            description='Premier QCM',
            condition_type='qcm_first',
            points_xp=10
        )
        Badge.objects.create(
            nom='Collectionneur',
            description='10 flashcards',
            condition_type='flashcard_10',
            points_xp=20
        )
    
    def test_qcm_complete_triggers_gamification(self):
        """Test qu'un QCM complété déclenche la gamification"""
        self.client.login(username='testuser', password='testpass123')
        
        # Créer un QCM
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        question = Question.objects.create(
            qcm=qcm,
            texte='Question ?',
            numero=1
        )
        choix = Choix.objects.create(
            question=question,
            texte='Réponse',
            est_correct=True
        )
        
        # Soumettre le QCM
        url = reverse('qcm:submit', kwargs={'qcm_id': qcm.id})
        import json
        data = {
            'reponses': {
                str(question.id): str(choix.id)
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Vérifier que le résultat est créé
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ResultatQCM.objects.filter(qcm=qcm).exists())
        
        # Vérifier que l'XP a été ajoutée
        progress = UserProgress.objects.get(user=self.user)
        self.assertGreater(progress.points_xp, 0)
        self.assertEqual(progress.qcm_completes, 1)
        
        # Vérifier que le badge a été attribué
        self.assertTrue(UserBadge.objects.filter(
            user=self.user,
            badge__condition_type='qcm_first'
        ).exists())
    
    def test_flashcard_creation_triggers_gamification(self):
        """Test que la création d'une flashcard déclenche la gamification"""
        self.client.login(username='testuser', password='testpass123')
        
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        
        # Créer 10 flashcards
        for i in range(10):
            url = reverse('flashcards:add_flashcard', kwargs={'deck_id': deck.id})
            data = {
                'recto': f'Question {i}',
                'verso': f'Réponse {i}'
            }
            self.client.post(url, data)
        
        # Vérifier que l'XP a été ajoutée
        progress = UserProgress.objects.get(user=self.user)
        self.assertEqual(progress.flashcards_creees, 10)
        self.assertGreater(progress.points_xp, 0)
        
        # Vérifier que le badge a été attribué
        self.assertTrue(UserBadge.objects.filter(
            user=self.user,
            badge__condition_type='flashcard_10'
        ).exists())
    
    def test_tutor_message_triggers_gamification(self):
        """Test qu'une question au tuteur déclenche la gamification"""
        self.client.login(username='testuser', password='testpass123')
        
        # Envoyer un message
        url = reverse('tutor:send_message')
        import json
        data = {
            'message': 'Bonjour'
        }
        self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Vérifier que l'XP a été ajoutée
        progress = UserProgress.objects.get(user=self.user)
        self.assertEqual(progress.questions_tuteur, 1)
        self.assertGreater(progress.points_xp, 0)


class IntegrationWorkflowTest(TestCase):
    """Tests de workflows complets utilisateur"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            niveau_etude='6e'
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
            contenu='Contenu du chapitre'
        )
    
    def test_complete_study_session(self):
        """Test une session d'étude complète"""
        self.client.login(username='testuser', password='testpass123')
        
        # 1. Créer une note
        from notes.models import Note
        url = reverse('notes:create')
        data = {
            'titre': 'Notes équations',
            'contenu': 'Les équations sont importantes',
            'chapitre_id': self.chapitre.id
        }
        self.client.post(url, data)
        self.assertTrue(Note.objects.filter(titre='Notes équations').exists())
        
        # 2. Créer un deck de flashcards
        deck_url = reverse('flashcards:create_deck')
        deck_data = {
            'titre': 'Deck équations',
            'chapitre_id': self.chapitre.id
        }
        response = self.client.post(deck_url, deck_data)
        deck = Deck.objects.get(titre='Deck équations')
        
        # 3. Ajouter des flashcards
        for i in range(3):
            flashcard_url = reverse('flashcards:add_flashcard', kwargs={'deck_id': deck.id})
            flashcard_data = {
                'recto': f'Question {i}',
                'verso': f'Réponse {i}'
            }
            self.client.post(flashcard_url, flashcard_data)
        
        # 4. Créer un QCM
        qcm_url = reverse('qcm:generate')
        qcm_data = {
            'titre': 'QCM équations',
            'texte_source': 'Les équations sont des égalités mathématiques.',
            'chapitre_id': self.chapitre.id
        }
        response = self.client.post(qcm_url, qcm_data)
        qcm = QCM.objects.get(titre='QCM équations')
        
        # 5. Vérifier que tout est créé
        self.assertTrue(Note.objects.filter(user=self.user).exists())
        self.assertTrue(Deck.objects.filter(user=self.user).exists())
        self.assertTrue(QCM.objects.filter(user=self.user).exists())
        self.assertEqual(deck.flashcards.count(), 3)
        self.assertGreater(qcm.questions.count(), 0)
        
        # 6. Vérifier la gamification
        progress = UserProgress.objects.get(user=self.user)
        self.assertGreater(progress.points_xp, 0)
        self.assertEqual(progress.flashcards_creees, 3)
    
    def test_calendar_integration(self):
        """Test l'intégration du calendrier avec les examens"""
        self.client.login(username='testuser', password='testpass123')
        
        # Créer un événement examen
        from calendar_app.models import EvenementScolaire
        from datetime import date, timedelta
        
        url = reverse('calendar:create')
        tomorrow = date.today() + timedelta(days=1)
        data = {
            'titre': 'Examen de Math',
            'type_evenement': 'examen',
            'date_debut': tomorrow.strftime('%Y-%m-%d'),
            'matiere_id': self.matiere.id,
            'couleur': '#ff0000',
            'rappel_jours': '1'
        }
        self.client.post(url, data)
        
        # Vérifier que l'événement est créé
        self.assertTrue(EvenementScolaire.objects.filter(
            user=self.user,
            titre='Examen de Math'
        ).exists())
        
        # Vérifier l'association avec la matière
        event = EvenementScolaire.objects.get(titre='Examen de Math')
        self.assertEqual(event.matiere, self.matiere)

