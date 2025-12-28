"""
Tests unitaires pour l'application accounts
Tests de base de données et backend
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User, Matiere, Chapitre
from datetime import date

User = get_user_model()


class UserModelTest(TestCase):
    """Tests pour le modèle User"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'niveau_etude': '6e',
            'classe': '6ème A',
            'ecole': 'École Test'
        }
    
    def test_create_user(self):
        """Test la création d'un utilisateur"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.niveau_etude, '6e')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_str(self):
        """Test la méthode __str__ du modèle User"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_user_fields(self):
        """Test que tous les champs sont présents"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNotNone(user.date_joined)
        self.assertIsNotNone(user.created_at)
        self.assertEqual(user.classe, '6ème A')
        self.assertEqual(user.ecole, 'École Test')
    
    def test_user_date_naissance(self):
        """Test le champ date de naissance"""
        user = User.objects.create_user(**self.user_data)
        user.date_naissance = date(2010, 1, 1)
        user.save()
        self.assertEqual(user.date_naissance, date(2010, 1, 1))
    
    def test_user_avatar(self):
        """Test l'upload d'un avatar"""
        user = User.objects.create_user(**self.user_data)
        avatar = SimpleUploadedFile(
            "avatar.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        user.avatar = avatar
        user.save()
        self.assertIsNotNone(user.avatar)


class MatiereModelTest(TestCase):
    """Tests pour le modèle Matiere"""
    
    def setUp(self):
        self.matiere_data = {
            'nom': 'Mathématiques',
            'code': 'MATH',
            'niveau': 'college',
            'description': 'Cours de mathématiques',
            'icone': '📐'
        }
    
    def test_create_matiere(self):
        """Test la création d'une matière"""
        matiere = Matiere.objects.create(**self.matiere_data)
        self.assertEqual(matiere.nom, 'Mathématiques')
        self.assertEqual(matiere.code, 'MATH')
        self.assertEqual(matiere.niveau, 'college')
    
    def test_matiere_str(self):
        """Test la méthode __str__"""
        matiere = Matiere.objects.create(**self.matiere_data)
        self.assertEqual(str(matiere), 'Mathématiques')
    
    def test_matiere_code_unique(self):
        """Test que le code est unique"""
        Matiere.objects.create(**self.matiere_data)
        with self.assertRaises(Exception):
            Matiere.objects.create(
                nom='Autre Maths',
                code='MATH',  # Même code
                niveau='lycee'
            )
    
    def test_matiere_default_icon(self):
        """Test l'icône par défaut"""
        matiere = Matiere.objects.create(
            nom='Français',
            code='FR',
            niveau='college'
        )
        self.assertEqual(matiere.icone, '📚')


class ChapitreModelTest(TestCase):
    """Tests pour le modèle Chapitre"""
    
    def setUp(self):
        self.matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        self.chapitre_data = {
            'matiere': self.matiere,
            'titre': 'Les équations',
            'numero': 1,
            'contenu': 'Contenu du chapitre sur les équations',
            'niveau': '6e'
        }
    
    def test_create_chapitre(self):
        """Test la création d'un chapitre"""
        chapitre = Chapitre.objects.create(**self.chapitre_data)
        self.assertEqual(chapitre.titre, 'Les équations')
        self.assertEqual(chapitre.numero, 1)
        self.assertEqual(chapitre.matiere, self.matiere)
    
    def test_chapitre_str(self):
        """Test la méthode __str__"""
        chapitre = Chapitre.objects.create(**self.chapitre_data)
        self.assertEqual(str(chapitre), 'Mathématiques - Les équations')
    
    def test_chapitre_unique_together(self):
        """Test la contrainte unique_together"""
        Chapitre.objects.create(**self.chapitre_data)
        # Ne peut pas créer un autre chapitre avec le même numéro et matière
        with self.assertRaises(Exception):
            Chapitre.objects.create(
                matiere=self.matiere,
                titre='Autre titre',
                numero=1,  # Même numéro
                contenu='Contenu'
            )
    
    def test_chapitre_foreign_key(self):
        """Test la relation ForeignKey vers Matiere"""
        chapitre = Chapitre.objects.create(**self.chapitre_data)
        self.assertEqual(chapitre.matiere.nom, 'Mathématiques')
        # Test la relation inverse
        self.assertIn(chapitre, self.matiere.chapitres.all())


class AccountsViewsTest(TestCase):
    """Tests pour les vues de l'application accounts"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:profile')
    
    def test_register_get(self):
        """Test l'affichage du formulaire d'inscription"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inscription')
        self.assertTemplateUsed(response, 'accounts/register.html')
    
    def test_register_post_valid(self):
        """Test l'inscription avec des données valides"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'niveau_etude': '6e',
            'classe': '6ème A',
            'ecole': 'École Test'
        }
        response = self.client.post(self.register_url, data)
        # Doit rediriger vers home après inscription réussie
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'utilisateur est créé
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_post_invalid(self):
        """Test l'inscription avec des données invalides"""
        data = {
            'username': 'newuser',
            'email': 'invalid-email',  # Email invalide
            'password1': 'testpass123',
            'password2': 'different',  # Mots de passe différents
            'niveau_etude': '6e'
        }
        response = self.client.post(self.register_url, data)
        # Doit rester sur la page avec des erreurs
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', None)
    
    def test_login_get(self):
        """Test l'affichage du formulaire de connexion"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connexion')
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_login_post_valid(self):
        """Test la connexion avec des identifiants valides"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        # Doit rediriger après connexion
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)
    
    def test_login_post_invalid(self):
        """Test la connexion avec des identifiants invalides"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        # Doit rester sur la page avec une erreur
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Erreur', status_code=200)
    
    def test_profile_requires_login(self):
        """Test que le profil nécessite une connexion"""
        response = self.client.get(self.profile_url)
        # Doit rediriger vers la page de connexion
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_profile_authenticated(self):
        """Test l'accès au profil quand connecté"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mon Profil')
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_profile_update(self):
        """Test la mise à jour du profil"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newemail@example.com',
            'niveau_etude': '5e',
            'classe': '5ème B',
            'ecole': 'Nouvelle École'
        }
        response = self.client.post(self.profile_url, data)
        # Doit rediriger après mise à jour
        self.assertEqual(response.status_code, 302)
        # Vérifier que les données sont mises à jour
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.email, 'newemail@example.com')


class AccountsFormsTest(TestCase):
    """Tests pour les formulaires de l'application accounts"""
    
    def test_registration_form_valid(self):
        """Test le formulaire d'inscription avec données valides"""
        from .forms import UserRegistrationForm
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'niveau_etude': '6e',
            'classe': '6ème A',
            'ecole': 'École Test'
        }
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_password_mismatch(self):
        """Test le formulaire avec mots de passe différents"""
        from .forms import UserRegistrationForm
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'different',
            'niveau_etude': '6e'
        }
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
    
    def test_registration_form_save(self):
        """Test la sauvegarde via le formulaire"""
        from .forms import UserRegistrationForm
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'niveau_etude': '6e',
            'classe': '6ème A'
        }
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

