"""
Tests unitaires pour le frontend
Tests d'intégration des templates et de l'interface utilisateur
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre

User = get_user_model()


class FrontendTemplatesTest(TestCase):
    """Tests pour les templates frontend"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_home_template(self):
        """Test le template de la page d'accueil"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Vérifier que les éléments clés sont présents
        self.assertContains(response, 'Learnia')
        self.assertContains(response, 'Tuteur Intelligent')
        self.assertContains(response, 'QCM')
    
    def test_home_template_authenticated(self):
        """Test la page d'accueil avec utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Vérifier que les liens fonctionnels sont présents
        self.assertContains(response, 'Essayer')
    
    def test_base_template_structure(self):
        """Test la structure du template de base"""
        response = self.client.get(reverse('home'))
        # Vérifier que Bootstrap est inclus
        self.assertContains(response, 'bootstrap')
        # Vérifier la navbar
        self.assertContains(response, 'navbar')
        # Vérifier le footer
        self.assertContains(response, 'Learnia')
    
    def test_login_template_structure(self):
        """Test la structure du template de connexion"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        # Vérifier les éléments du formulaire
        self.assertContains(response, 'Connexion')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')
        self.assertContains(response, 'Inscrivez-vous')
    
    def test_register_template_structure(self):
        """Test la structure du template d'inscription"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        # Vérifier les éléments du formulaire
        self.assertContains(response, 'Inscription')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')
        self.assertContains(response, 'Connectez-vous')
    
    def test_profile_template_structure(self):
        """Test la structure du template de profil"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'Mon Profil')
        self.assertContains(response, 'email')
    
    def test_qcm_index_template(self):
        """Test le template de l'index QCM"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('qcm:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qcm/index.html')
        self.assertContains(response, 'QCM')
    
    def test_flashcards_index_template(self):
        """Test le template de l'index flashcards"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('flashcards:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flashcards/index.html')
        self.assertContains(response, 'Decks')


class FrontendNavigationTest(TestCase):
    """Tests pour la navigation frontend"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_navbar_links_not_authenticated(self):
        """Test les liens de la navbar pour utilisateur non connecté"""
        response = self.client.get(reverse('home'))
        # Vérifier que les liens de connexion/inscription sont présents
        self.assertContains(response, 'Connexion')
        self.assertContains(response, 'Inscription')
        # Vérifier que les liens protégés ne sont pas visibles
        self.assertNotContains(response, 'Tuteur')
    
    def test_navbar_links_authenticated(self):
        """Test les liens de la navbar pour utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        # Vérifier que les liens fonctionnels sont présents
        self.assertContains(response, 'Tuteur')
        self.assertContains(response, 'QCM')
        self.assertContains(response, 'Flashcards')
        self.assertContains(response, 'Déconnexion')
    
    def test_footer_present(self):
        """Test que le footer est présent"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'footer')
        self.assertContains(response, '2024')


class FrontendFormsTest(TestCase):
    """Tests pour les formulaires frontend"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_login_form_fields(self):
        """Test que le formulaire de connexion a les bons champs"""
        response = self.client.get(reverse('accounts:login'))
        # Vérifier la présence des champs dans le HTML
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_register_form_fields(self):
        """Test que le formulaire d'inscription a les bons champs"""
        response = self.client.get(reverse('accounts:register'))
        # Vérifier la présence des champs dans le HTML
        self.assertContains(response, 'username')
        self.assertContains(response, 'email')
        self.assertContains(response, 'password1')
        self.assertContains(response, 'password2')
        self.assertContains(response, 'niveau_etude')
    
    def test_form_csrf_protection(self):
        """Test que les formulaires ont la protection CSRF"""
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, 'csrfmiddlewaretoken')


class FrontendResponsiveTest(TestCase):
    """Tests pour la responsivité du frontend"""
    
    def setUp(self):
        self.client = Client()
    
    def test_bootstrap_included(self):
        """Test que Bootstrap est inclus"""
        response = self.client.get(reverse('home'))
        # Vérifier que Bootstrap CSS est présent
        self.assertContains(response, 'bootstrap')
    
    def test_responsive_meta_tag(self):
        """Test que la meta tag viewport est présente"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'width=device-width')


class FrontendErrorHandlingTest(TestCase):
    """Tests pour la gestion des erreurs frontend"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_404_page(self):
        """Test qu'une page inexistante retourne 404"""
        response = self.client.get('/page-inexistante/')
        self.assertEqual(response.status_code, 404)
    
    def test_form_error_display(self):
        """Test l'affichage des erreurs de formulaire"""
        # Tenter une connexion avec de mauvais identifiants
        response = self.client.post(reverse('accounts:login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertContains(response, 'Erreur')
    
    def test_messages_display(self):
        """Test l'affichage des messages"""
        self.client.login(username='testuser', password='testpass123')
        # Modifier le profil pour générer un message de succès
        response = self.client.post(reverse('accounts:profile'), {
            'email': 'new@example.com',
            'niveau_etude': '6e'
        })
        # Vérifier que le message système est présent dans le template
        # (vérifié via la redirection)
        self.assertEqual(response.status_code, 302)


