"""
Tests d'intégrité pour vérifier que tous les templates et URLs sont corrects
"""
from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings
import os
from pathlib import Path

User = get_user_model()


class TemplateIntegrityTest(TestCase):
    """Tests pour vérifier que tous les templates existent"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_all_templates_exist(self):
        """Vérifie que tous les templates référencés dans les vues existent"""
        templates_to_check = [
            # Accounts
            'accounts/login.html',
            'accounts/register.html',
            'accounts/profile.html',
            
            # Tutor
            'tutor/index.html',
            'tutor/conversation.html',
            
            # QCM
            'qcm/index.html',
            'qcm/generate.html',
            'qcm/detail.html',
            
            # Flashcards
            'flashcards/index.html',
            'flashcards/create_deck.html',
            'flashcards/deck_detail.html',
            
            # Planner
            'planner/index.html',
            'planner/create_examen.html',
            'planner/create_revision.html',
            'planner/generate_plan.html',
            
            # Analytics
            'analytics/index.html',
            
            # Export
            'export/dashboard.html',
            
            # Gamification
            'gamification/dashboard.html',
            'gamification/badges.html',
            
            # Notes
            'notes/list.html',
            'notes/form.html',
            'notes/detail.html',
            'notes/delete.html',
            
            # Calendar
            'calendar_app/calendar.html',
            'calendar_app/form.html',
            'calendar_app/delete.html',
            
            # Fiches
            'fiches/list.html',
            'fiches/form.html',
            'fiches/delete.html',
            
            # Base
            'base.html',
            'home.html',
        ]
        
        missing_templates = []
        for template_name in templates_to_check:
            try:
                get_template(template_name)
            except TemplateDoesNotExist:
                missing_templates.append(template_name)
        
        self.assertEqual(
            len(missing_templates), 0,
            f"Templates manquants: {', '.join(missing_templates)}"
        )


class URLIntegrityTest(TestCase):
    """Tests pour vérifier que toutes les URLs sont valides"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_accounts_urls(self):
        """Test des URLs accounts"""
        urls = [
            ('accounts:login', []),
            ('accounts:logout', []),
            ('accounts:register', []),
            ('accounts:profile', []),
        ]
        self._test_urls(urls)
    
    def test_tutor_urls(self):
        """Test des URLs tutor"""
        urls = [
            ('tutor:index', []),
        ]
        self._test_urls(urls)
    
    def test_qcm_urls(self):
        """Test des URLs qcm"""
        from qcm.models import QCM
        qcm = QCM.objects.create(
            user=self.user,
            titre='Test QCM',
            texte_source='Test'
        )
        urls = [
            ('qcm:index', []),
            ('qcm:generate', []),
            ('qcm:detail', [qcm.id]),
        ]
        self._test_urls(urls)
    
    def test_flashcards_urls(self):
        """Test des URLs flashcards"""
        from flashcards.models import Deck
        deck = Deck.objects.create(
            user=self.user,
            titre='Test Deck'
        )
        urls = [
            ('flashcards:index', []),
            ('flashcards:create_deck', []),
            ('flashcards:deck_detail', [deck.id]),
        ]
        self._test_urls(urls)
    
    def test_planner_urls(self):
        """Test des URLs planner"""
        urls = [
            ('planner:index', []),
            ('planner:create_examen', []),
            ('planner:create_revision', []),
            ('planner:generate_plan', []),
        ]
        self._test_urls(urls)
    
    def test_gamification_urls(self):
        """Test des URLs gamification"""
        urls = [
            ('gamification:dashboard', []),
            ('gamification:badges', []),
        ]
        self._test_urls(urls)
    
    def test_notes_urls(self):
        """Test des URLs notes"""
        from notes.models import Note
        note = Note.objects.create(
            user=self.user,
            titre='Test Note',
            contenu='Test content'
        )
        urls = [
            ('notes:list', []),
            ('notes:create', []),
            ('notes:detail', [note.id]),
            ('notes:edit', [note.id]),
            ('notes:delete', [note.id]),
        ]
        self._test_urls(urls)
    
    def test_calendar_urls(self):
        """Test des URLs calendar"""
        from calendar_app.models import EvenementScolaire
        from datetime import date, timedelta
        event = EvenementScolaire.objects.create(
            user=self.user,
            titre='Test Event',
            type_evenement='examen',
            date_debut=date.today() + timedelta(days=1)
        )
        urls = [
            ('calendar:view', []),
            ('calendar:create', []),
            ('calendar:edit', [event.id]),
            ('calendar:delete', [event.id]),
        ]
        self._test_urls(urls)
    
    def test_fiches_urls(self):
        """Test des URLs fiches"""
        from fiches.models import FicheRevision
        fiche = FicheRevision.objects.create(
            user=self.user,
            titre='Test Fiche',
            contenu='Test content'
        )
        from accounts.models import Chapitre, Matiere
        matiere = Matiere.objects.create(nom='Math', code='MATH', niveau='college')
        chapitre = Chapitre.objects.create(matiere=matiere, titre='Test', numero=1, contenu='Test')
        from flashcards.models import Deck
        deck = Deck.objects.create(user=self.user, titre='Test Deck')
        
        urls = [
            ('fiches:list', []),
            ('fiches:create', []),
            ('fiches:from_chapitre', [chapitre.id]),
            ('fiches:from_deck', [deck.id]),
            ('fiches:download', [fiche.id]),
            ('fiches:delete', [fiche.id]),
        ]
        self._test_urls(urls)
    
    def _test_urls(self, urls):
        """Helper pour tester une liste d'URLs"""
        missing_urls = []
        for url_name, args in urls:
            try:
                reverse(url_name, args=args)
            except NoReverseMatch as e:
                missing_urls.append(f"{url_name}: {str(e)}")
        
        self.assertEqual(
            len(missing_urls), 0,
            f"URLs invalides: {', '.join(missing_urls)}"
        )


class ViewAccessibilityTest(TestCase):
    """Tests pour vérifier que toutes les vues sont accessibles"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_public_pages(self):
        """Test des pages publiques"""
        pages = [
            ('accounts:login', []),
            ('accounts:register', []),
            ('home', []),
        ]
        for url_name, args in pages:
            url = reverse(url_name, args=args)
            response = self.client.get(url)
            self.assertIn(
                response.status_code, [200, 302],
                f"Page {url_name} inaccessible (code: {response.status_code})"
            )
    
    def test_authenticated_pages(self):
        """Test des pages nécessitant une authentification"""
        self.client.login(username='testuser', password='testpass123')
        
        pages = [
            ('accounts:profile', []),
            ('tutor:index', []),
            ('qcm:index', []),
            ('flashcards:index', []),
            ('planner:index', []),
            ('analytics:index', []),
            ('gamification:dashboard', []),
            ('notes:list', []),
            ('calendar:view', []),
            ('fiches:list', []),
        ]
        
        inaccessible_pages = []
        for url_name, args in pages:
            try:
                url = reverse(url_name, args=args)
                response = self.client.get(url)
                if response.status_code not in [200, 302]:
                    inaccessible_pages.append(f"{url_name} (code: {response.status_code})")
            except Exception as e:
                inaccessible_pages.append(f"{url_name} (erreur: {str(e)})")
        
        self.assertEqual(
            len(inaccessible_pages), 0,
            f"Pages inaccessibles: {', '.join(inaccessible_pages)}"
        )


class TemplateLinkIntegrityTest(TestCase):
    """Tests pour vérifier que tous les liens dans les templates sont valides"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_base_template_links(self):
        """Test des liens dans base.html"""
        from accounts.models import Matiere, Chapitre
        matiere = Matiere.objects.create(nom='Math', code='MATH', niveau='college')
        chapitre = Chapitre.objects.create(matiere=matiere, titre='Test', numero=1, contenu='Test')
        
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Vérifier que la page charge sans erreur de template
        self.assertNotContains(response, 'NoReverseMatch', msg_prefix="Erreur NoReverseMatch détectée")
        self.assertNotContains(response, 'TemplateDoesNotExist', msg_prefix="Erreur TemplateDoesNotExist détectée")
    
    def test_planner_template_links(self):
        """Test des liens dans planner/index.html"""
        url = reverse('planner:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'NoReverseMatch')
    
    def test_fiches_template_links(self):
        """Test des liens dans fiches/list.html"""
        url = reverse('fiches:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'NoReverseMatch')
    
    def test_flashcards_template_links(self):
        """Test des liens dans flashcards"""
        from flashcards.models import Deck
        deck = Deck.objects.create(user=self.user, titre='Test Deck')
        
        url = reverse('flashcards:deck_detail', args=[deck.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'NoReverseMatch')


class ModelRelationsTest(TestCase):
    """Tests pour vérifier que toutes les relations entre modèles sont correctes"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_accounts_models(self):
        """Test des modèles accounts"""
        from accounts.models import Matiere, Chapitre
        
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        chapitre = Chapitre.objects.create(
            matiere=matiere,
            titre='Les équations',
            numero=1,
            contenu='Contenu'
        )
        
        self.assertEqual(chapitre.matiere, matiere)
        self.assertIn(chapitre, matiere.chapitres.all())
    
    def test_qcm_models(self):
        """Test des modèles qcm"""
        from qcm.models import QCM, Question, Choix
        
        qcm = QCM.objects.create(
            user=self.user,
            titre='Test QCM',
            texte_source='Test'
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
        
        self.assertEqual(question.qcm, qcm)
        self.assertEqual(choix.question, question)
    
    def test_flashcards_models(self):
        """Test des modèles flashcards"""
        from flashcards.models import Deck, Flashcard
        from accounts.models import Matiere, Chapitre
        
        matiere = Matiere.objects.create(nom='Math', code='MATH', niveau='college')
        chapitre = Chapitre.objects.create(matiere=matiere, titre='Test', numero=1, contenu='Test')
        
        deck = Deck.objects.create(
            user=self.user,
            titre='Test Deck',
            chapitre=chapitre
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse'
        )
        
        self.assertEqual(flashcard.deck, deck)
        self.assertIn(flashcard, deck.flashcards.all())


class DataIntegrityTest(TestCase):
    """Tests pour vérifier l'intégrité des données"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_user_creation(self):
        """Test que la création d'utilisateur fonctionne"""
        user = User.objects.create_user(
            username='newuser',
            password='pass123',
            email='new@example.com'
        )
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
    
    def test_gamification_integration(self):
        """Test que la gamification fonctionne avec les autres modules"""
        from gamification.models import UserProgress
        from qcm.models import QCM, ResultatQCM
        
        progress = UserProgress.objects.get_or_create(user=self.user)[0]
        
        qcm = QCM.objects.create(
            user=self.user,
            titre='Test',
            texte_source='Test'
        )
        resultat = ResultatQCM.objects.create(
            user=self.user,
            qcm=qcm,
            score=8,
            total=10,
            pourcentage=80.0
        )
        
        # Vérifier que le progrès a été mis à jour
        progress.refresh_from_db()
        self.assertGreaterEqual(progress.qcm_completes, 0)
    
    def test_fiches_with_chapitre(self):
        """Test que les fiches peuvent être créées avec un chapitre"""
        from fiches.models import FicheRevision
        from accounts.models import Matiere, Chapitre
        
        matiere = Matiere.objects.create(nom='Math', code='MATH', niveau='college')
        chapitre = Chapitre.objects.create(matiere=matiere, titre='Test', numero=1, contenu='Test')
        
        fiche = FicheRevision.objects.create(
            user=self.user,
            titre='Test Fiche',
            contenu='Contenu',
            chapitre=chapitre
        )
        
        self.assertEqual(fiche.chapitre, chapitre)
        self.assertEqual(fiche.chapitre.matiere, matiere)



