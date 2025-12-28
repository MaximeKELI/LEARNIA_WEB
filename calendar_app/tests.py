"""
Tests unitaires pour l'application calendar_app
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import Matiere
from .models import EvenementScolaire

User = get_user_model()


class EvenementScolaireModelTest(TestCase):
    """Tests pour le modèle EvenementScolaire"""
    
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
    
    def test_create_evenement(self):
        """Test la création d'un événement"""
        evenement = EvenementScolaire.objects.create(
            user=self.user,
            titre='Examen de Math',
            description='Examen sur les équations',
            type_evenement='examen',
            date_debut=date.today() + timedelta(days=7),
            matiere=self.matiere,
            couleur='#ff0000',
            rappel_jours=1
        )
        self.assertEqual(evenement.titre, 'Examen de Math')
        self.assertEqual(evenement.type_evenement, 'examen')
        self.assertEqual(evenement.user, self.user)
        self.assertFalse(evenement.public)
    
    def test_evenement_public(self):
        """Test un événement public"""
        evenement = EvenementScolaire.objects.create(
            user=self.user,
            titre='Vacances',
            type_evenement='vacances',
            date_debut=date.today(),
            public=True
        )
        self.assertTrue(evenement.public)
    
    def test_evenement_with_dates(self):
        """Test un événement avec dates de début et fin"""
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=7)
        evenement = EvenementScolaire.objects.create(
            user=self.user,
            titre='Vacances',
            type_evenement='vacances',
            date_debut=date_debut,
            date_fin=date_fin
        )
        self.assertEqual(evenement.date_debut, date_debut)
        self.assertEqual(evenement.date_fin, date_fin)


class CalendarViewsTest(TestCase):
    """Tests pour les vues du calendrier"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_calendar_view_requires_login(self):
        """Test que le calendrier nécessite une connexion"""
        url = reverse('calendar:view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_calendar_view_authenticated(self):
        """Test l'accès au calendrier quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('calendar:view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/calendar.html')
    
    def test_event_create_get(self):
        """Test l'affichage du formulaire de création"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('calendar:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendar_app/form.html')
    
    def test_event_create_post(self):
        """Test la création d'un événement"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('calendar:create')
        tomorrow = date.today() + timedelta(days=1)
        data = {
            'titre': 'Examen',
            'description': 'Examen important',
            'type_evenement': 'examen',
            'date_debut': tomorrow.strftime('%Y-%m-%d'),
            'couleur': '#ff0000',
            'rappel_jours': '1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EvenementScolaire.objects.filter(titre='Examen').exists())
    
    def test_event_edit(self):
        """Test la modification d'un événement"""
        self.client.login(username='testuser', password='testpass123')
        evenement = EvenementScolaire.objects.create(
            user=self.user,
            titre='Ancien titre',
            type_evenement='examen',
            date_debut=date.today() + timedelta(days=7)
        )
        url = reverse('calendar:edit', kwargs={'event_id': evenement.id})
        tomorrow = date.today() + timedelta(days=1)
        data = {
            'titre': 'Nouveau titre',
            'description': 'Description mise à jour',
            'type_evenement': 'examen',
            'date_debut': tomorrow.strftime('%Y-%m-%d'),
            'couleur': '#0000ff',
            'rappel_jours': '2'
        }
        response = self.client.post(url, data)
        evenement.refresh_from_db()
        self.assertEqual(evenement.titre, 'Nouveau titre')
    
    def test_event_delete(self):
        """Test la suppression d'un événement"""
        self.client.login(username='testuser', password='testpass123')
        evenement = EvenementScolaire.objects.create(
            user=self.user,
            titre='À supprimer',
            type_evenement='rappel',
            date_debut=date.today()
        )
        url = reverse('calendar:delete', kwargs={'event_id': evenement.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(EvenementScolaire.objects.filter(id=evenement.id).exists())

