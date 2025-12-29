"""
Tests unitaires pour l'application fiches
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre
from flashcards.models import Deck
from .models import FicheRevision
from .services import FichePDFGenerator

User = get_user_model()


class FicheRevisionModelTest(TestCase):
    """Tests pour le modèle FicheRevision"""
    
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
            contenu='Contenu du chapitre'
        )
    
    def test_create_fiche(self):
        """Test la création d'une fiche"""
        fiche = FicheRevision.objects.create(
            user=self.user,
            titre='Ma fiche',
            contenu='Contenu de la fiche',
            chapitre=self.chapitre,
            couleur_titre='#ff0000',
            police='Arial'
        )
        self.assertEqual(fiche.titre, 'Ma fiche')
        self.assertEqual(fiche.user, self.user)
        self.assertEqual(fiche.chapitre, self.chapitre)
        self.assertEqual(fiche.couleur_titre, '#ff0000')
        self.assertEqual(fiche.police, 'Arial')


class FichePDFGeneratorTest(TestCase):
    """Tests pour le générateur de PDF"""
    
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
            contenu='Contenu du chapitre sur les équations linéaires.'
        )
    
    def test_generate_fiche(self):
        """Test la génération d'un PDF pour une fiche"""
        fiche = FicheRevision.objects.create(
            user=self.user,
            titre='Test Fiche',
            contenu='## Titre\n\nContenu de test.',
            chapitre=self.chapitre
        )
        
        buffer = FichePDFGenerator.generate_fiche(fiche)
        self.assertIsNotNone(buffer)
        self.assertGreater(len(buffer.getvalue()), 0)
    
    def test_generate_from_chapitre(self):
        """Test la génération depuis un chapitre"""
        buffer = FichePDFGenerator.generate_from_chapitre(self.chapitre, self.user)
        self.assertIsNotNone(buffer)
        self.assertGreater(len(buffer.getvalue()), 0)
    
    def test_generate_from_flashcards(self):
        """Test la génération depuis un deck"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        from flashcards.models import Flashcard
        Flashcard.objects.create(
            deck=deck,
            recto='Question ?',
            verso='Réponse'
        )
        
        buffer = FichePDFGenerator.generate_from_flashcards(deck, self.user)
        self.assertIsNotNone(buffer)
        self.assertGreater(len(buffer.getvalue()), 0)


class FichesViewsTest(TestCase):
    """Tests pour les vues fiches"""
    
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
    
    def test_fiches_list_requires_login(self):
        """Test que la liste nécessite une connexion"""
        url = reverse('fiches:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_fiches_list_authenticated(self):
        """Test l'accès à la liste quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('fiches:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fiches/list.html')
    
    def test_fiche_create_get(self):
        """Test l'affichage du formulaire"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('fiches:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fiches/form.html')
    
    def test_fiche_create_post(self):
        """Test la création d'une fiche"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('fiches:create')
        data = {
            'titre': 'Ma fiche',
            'contenu': '## Titre\n\nContenu.',
            'chapitre_id': self.chapitre.id,
            'couleur_titre': '#ff0000',
            'police': 'Arial'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FicheRevision.objects.filter(titre='Ma fiche').exists())
    
    def test_fiche_download(self):
        """Test le téléchargement d'une fiche"""
        self.client.login(username='testuser', password='testpass123')
        fiche = FicheRevision.objects.create(
            user=self.user,
            titre='Fiche test',
            contenu='Contenu'
        )
        url = reverse('fiches:download', kwargs={'fiche_id': fiche.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_fiche_from_chapitre(self):
        """Test la génération depuis un chapitre"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('fiches:from_chapitre', kwargs={'chapitre_id': self.chapitre.id})
        data = {
            'titre': 'Fiche générée'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')


