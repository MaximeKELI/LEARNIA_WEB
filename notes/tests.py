"""
Tests unitaires pour l'application notes
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre
from .models import Note, NoteVersion

User = get_user_model()


class NoteModelTest(TestCase):
    """Tests pour le modèle Note"""
    
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
    
    def test_create_note(self):
        """Test la création d'une note"""
        note = Note.objects.create(
            user=self.user,
            titre='Ma note',
            contenu='Contenu de la note',
            chapitre=self.chapitre
        )
        self.assertEqual(note.titre, 'Ma note')
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.chapitre, self.chapitre)
        self.assertFalse(note.favori)
    
    def test_note_get_tags_list(self):
        """Test la méthode get_tags_list"""
        note = Note.objects.create(
            user=self.user,
            titre='Note avec tags',
            contenu='Contenu',
            tags='important, révision, formule'
        )
        tags = note.get_tags_list()
        self.assertEqual(len(tags), 3)
        self.assertIn('important', tags)
        self.assertIn('révision', tags)
        self.assertIn('formule', tags)
    
    def test_note_tags_empty(self):
        """Test get_tags_list avec tags vides"""
        note = Note.objects.create(
            user=self.user,
            titre='Note sans tags',
            contenu='Contenu'
        )
        tags = note.get_tags_list()
        self.assertEqual(len(tags), 0)
    
    def test_create_note_version(self):
        """Test la création d'une version de note"""
        note = Note.objects.create(
            user=self.user,
            titre='Note',
            contenu='Version 1'
        )
        version = NoteVersion.objects.create(
            note=note,
            contenu='Version 1'
        )
        self.assertEqual(version.note, note)
        self.assertEqual(version.contenu, 'Version 1')


class NotesViewsTest(TestCase):
    """Tests pour les vues notes"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_notes_list_requires_login(self):
        """Test que la liste nécessite une connexion"""
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_notes_list_authenticated(self):
        """Test l'accès à la liste quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('notes:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/list.html')
    
    def test_note_create_get(self):
        """Test l'affichage du formulaire de création"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('notes:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/form.html')
    
    def test_note_create_post(self):
        """Test la création d'une note"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('notes:create')
        data = {
            'titre': 'Ma nouvelle note',
            'contenu': 'Contenu de la note',
            'tags': 'important, test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirection
        self.assertTrue(Note.objects.filter(titre='Ma nouvelle note').exists())
    
    def test_note_detail(self):
        """Test le détail d'une note"""
        self.client.login(username='testuser', password='testpass123')
        note = Note.objects.create(
            user=self.user,
            titre='Note test',
            contenu='Contenu'
        )
        url = reverse('notes:detail', kwargs={'note_id': note.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Note test')
    
    def test_note_search(self):
        """Test la recherche dans les notes"""
        self.client.login(username='testuser', password='testpass123')
        Note.objects.create(
            user=self.user,
            titre='Note importante',
            contenu='Contenu sur les équations'
        )
        Note.objects.create(
            user=self.user,
            titre='Autre note',
            contenu='Autre contenu'
        )
        url = reverse('notes:list') + '?q=équations'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Note importante')
        self.assertNotContains(response, 'Autre note')
    
    def test_note_toggle_favorite(self):
        """Test le basculement du statut favori"""
        self.client.login(username='testuser', password='testpass123')
        note = Note.objects.create(
            user=self.user,
            titre='Note',
            contenu='Contenu',
            favori=False
        )
        url = reverse('notes:toggle_favorite', kwargs={'note_id': note.id})
        response = self.client.get(url)
        note.refresh_from_db()
        self.assertTrue(note.favori)

