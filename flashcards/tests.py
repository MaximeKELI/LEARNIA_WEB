"""
Tests unitaires pour l'application flashcards
Tests backend et base de données
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import Matiere, Chapitre
from .models import Deck, Flashcard, Revision

User = get_user_model()


class FlashcardModelTest(TestCase):
    """Tests pour les modèles flashcards"""
    
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
    
    def test_create_deck(self):
        """Test la création d'un deck"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Mathématiques',
            chapitre=self.chapitre,
            description='Deck pour réviser les équations'
        )
        self.assertEqual(deck.titre, 'Deck Mathématiques')
        self.assertEqual(deck.user, self.user)
        self.assertEqual(deck.chapitre, self.chapitre)
    
    def test_create_flashcard(self):
        """Test la création d'une flashcard"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test',
            description='Description'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse'
        )
        self.assertEqual(flashcard.recto, 'Question')
        self.assertEqual(flashcard.verso, 'Réponse')
        self.assertEqual(flashcard.niveau, 0)
    
    def test_flashcard_marquer_success(self):
        """Test la méthode marquer_success"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse',
            niveau=0
        )
        initial_niveau = flashcard.niveau
        flashcard.marquer_success()
        self.assertEqual(flashcard.niveau, initial_niveau + 1)
        self.assertEqual(flashcard.nombre_revisions, 1)
        self.assertEqual(flashcard.nombre_success, 1)
    
    def test_flashcard_marquer_echec(self):
        """Test la méthode marquer_echec"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse',
            niveau=2
        )
        flashcard.marquer_echec()
        self.assertEqual(flashcard.niveau, 0)
        self.assertEqual(flashcard.nombre_revisions, 1)
    
    def test_flashcard_prochaine_revision(self):
        """Test le calcul de la prochaine révision"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse',
            niveau=1
        )
        flashcard.marquer_success()
        # Niveau 1 -> 2 jours
        expected_date = timezone.now() + timedelta(days=2)
        self.assertAlmostEqual(
            flashcard.prochaine_revision.timestamp(),
            expected_date.timestamp(),
            delta=60  # Tolérance de 60 secondes
        )
    
    def test_create_revision(self):
        """Test la création d'une révision"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse'
        )
        revision = Revision.objects.create(
            user=self.user,
            flashcard=flashcard,
            reussie=True,
            temps_reponse=30
        )
        self.assertTrue(revision.reussie)
        self.assertEqual(revision.temps_reponse, 30)


class FlashcardsViewsTest(TestCase):
    """Tests pour les vues flashcards"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_flashcards_index_requires_login(self):
        """Test que l'index nécessite une connexion"""
        url = reverse('flashcards:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_flashcards_index_authenticated(self):
        """Test l'accès à l'index quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('flashcards:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/index.html')
    
    def test_create_deck(self):
        """Test la création d'un deck"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('flashcards:create_deck')
        data = {
            'titre': 'Nouveau Deck',
            'description': 'Description du deck'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Deck.objects.filter(titre='Nouveau Deck').exists())
    
    def test_add_flashcard(self):
        """Test l'ajout d'une flashcard"""
        self.client.login(username='testuser', password='testpass123')
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        url = reverse('flashcards:add_flashcard', kwargs={'deck_id': deck.id})
        data = {
            'recto': 'Question ?',
            'verso': 'Réponse'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Flashcard.objects.filter(recto='Question ?').exists())


