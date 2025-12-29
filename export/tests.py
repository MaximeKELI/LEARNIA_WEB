"""
Tests unitaires pour l'application export
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Permission
from accounts.models import Matiere, Chapitre, User
from qcm.models import QCM, ResultatQCM
from .services import CSVExporter, CSVImporter
from .pdf_services import PDFExporter

User = get_user_model()


class CSVExporterTest(TestCase):
    """Tests pour l'export CSV"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.user.is_staff = True
        self.user.save()
        
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
    
    def test_export_users_csv(self):
        """Test l'export des utilisateurs"""
        response = CSVExporter.export_users()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('users_', response['Content-Disposition'])
        # Vérifier le contenu CSV
        content = response.content.decode('utf-8')
        self.assertIn('Username', content)
        self.assertIn('testuser', content)
    
    def test_export_statistics_csv(self):
        """Test l'export des statistiques"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        ResultatQCM.objects.create(
            user=self.user,
            qcm=qcm,
            score=8,
            total=10,
            pourcentage=80.0
        )
        
        response = CSVExporter.export_statistics()
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Utilisateur', content)
        self.assertIn('testuser', content)
    
    def test_export_data_science_csv(self):
        """Test l'export data science"""
        response = CSVExporter.export_for_data_science()
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('user_id', content)
        self.assertIn('username', content)


class CSVImporterTest(TestCase):
    """Tests pour l'import CSV"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.user.is_staff = True
        self.user.save()
    
    def test_import_users_csv(self):
        """Test l'import d'utilisateurs"""
        import io
        csv_content = """Username,Email,Prénom,Nom,Niveau d'étude,Classe,École
newuser,newuser@example.com,John,Doe,6e,6ème A,École Test"""
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'test.csv'
        
        imported, errors = CSVImporter.import_users(csv_file)
        self.assertEqual(imported, 1)
        self.assertEqual(len(errors), 0)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_import_users_csv_update(self):
        """Test la mise à jour d'utilisateur existant"""
        User.objects.create_user(
            username='existinguser',
            email='old@example.com',
            password='pass'
        )
        
        import io
        csv_content = """Username,Email,Prénom,Nom,Niveau d'étude,Classe,École
existinguser,newemail@example.com,John,Doe,6e,6ème A,École Test"""
        csv_file = io.BytesIO(csv_content.encode('utf-8'))
        csv_file.name = 'test.csv'
        
        imported, errors = CSVImporter.import_users(csv_file)
        user = User.objects.get(username='existinguser')
        self.assertEqual(user.email, 'newemail@example.com')


class PDFExporterTest(TestCase):
    """Tests pour l'export PDF"""
    
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
    
    def test_export_statistics_pdf(self):
        """Test l'export PDF des statistiques"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        ResultatQCM.objects.create(
            user=self.user,
            qcm=qcm,
            score=8,
            total=10,
            pourcentage=80.0
        )
        
        response = PDFExporter.export_statistics_pdf()
        self.assertIsNotNone(response)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('statistics_', response['Content-Disposition'])
    
    def test_export_user_report_pdf(self):
        """Test l'export d'un rapport utilisateur"""
        response = PDFExporter.export_user_report(self.user.id)
        self.assertIsNotNone(response)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_export_user_report_invalid_user(self):
        """Test avec un utilisateur invalide"""
        response = PDFExporter.export_user_report(99999)
        self.assertIsNone(response)
    
    def test_export_data_science_pdf(self):
        """Test l'export du rapport data science"""
        response = PDFExporter.export_data_science_report()
        self.assertIsNotNone(response)
        self.assertEqual(response['Content-Type'], 'application/pdf')


class ExportViewsTest(TestCase):
    """Tests pour les vues d'export"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.user.is_staff = True
        self.user.save()
    
    def test_export_dashboard_requires_staff(self):
        """Test que le dashboard nécessite staff"""
        normal_user = User.objects.create_user(
            username='normal',
            password='pass',
            email='normal@example.com'
        )
        self.client.login(username='normal', password='pass')
        url = reverse('export:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirige vers login
    
    def test_export_dashboard_staff(self):
        """Test l'accès au dashboard pour staff"""
        self.client.login(username='admin', password='admin123')
        url = reverse('export:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'export/dashboard.html')
    
    def test_export_users_csv_staff(self):
        """Test l'export CSV utilisateurs"""
        self.client.login(username='admin', password='admin123')
        url = reverse('export:export_users_csv')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')


