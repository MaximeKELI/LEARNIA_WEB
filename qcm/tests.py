"""
Tests unitaires pour l'application QCM
Tests backend et base de données
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Matiere, Chapitre
from .models import QCM, Question, Choix, ResultatQCM
from .services import QCMGenerator
import json

User = get_user_model()


class QCMModelTest(TestCase):
    """Tests pour les modèles QCM"""
    
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
    
    def test_create_qcm(self):
        """Test la création d'un QCM"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Mathématiques',
            chapitre=self.chapitre,
            texte_source='Texte source du QCM'
        )
        self.assertEqual(qcm.titre, 'QCM Mathématiques')
        self.assertEqual(qcm.user, self.user)
        self.assertEqual(qcm.chapitre, self.chapitre)
    
    def test_create_question(self):
        """Test la création d'une question"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        question = Question.objects.create(
            qcm=qcm,
            texte='Quelle est la réponse ?',
            numero=1
        )
        self.assertEqual(question.texte, 'Quelle est la réponse ?')
        self.assertEqual(question.numero, 1)
    
    def test_create_choix(self):
        """Test la création d'un choix"""
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
            texte='Réponse 1',
            est_correct=True
        )
        self.assertEqual(choix.texte, 'Réponse 1')
        self.assertTrue(choix.est_correct)
    
    def test_create_resultat(self):
        """Test la création d'un résultat"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        resultat = ResultatQCM.objects.create(
            user=self.user,
            qcm=qcm,
            score=8,
            total=10,
            pourcentage=80.0
        )
        self.assertEqual(resultat.score, 8)
        self.assertEqual(resultat.total, 10)
        self.assertEqual(resultat.pourcentage, 80.0)


class QCMGeneratorServiceTest(TestCase):
    """Tests pour le service QCMGenerator"""
    
    def setUp(self):
        self.generator = QCMGenerator()
        self.texte = """
        Les mathématiques sont une science qui étudie les nombres, les formes et les structures.
        Une équation est une égalité mathématique contenant une ou plusieurs inconnues.
        Pour résoudre une équation, on doit trouver la valeur de l'inconnue.
        """
    
    def test_generate_questions(self):
        """Test la génération de questions"""
        questions = self.generator.generate_questions(self.texte, nombre_questions=3)
        self.assertGreater(len(questions), 0)
        self.assertLessEqual(len(questions), 3)
    
    def test_question_structure(self):
        """Test la structure des questions générées"""
        questions = self.generator.generate_questions(self.texte, nombre_questions=1)
        if questions:
            question = questions[0]
            self.assertIn('numero', question)
            self.assertIn('texte', question)
            self.assertIn('choix', question)
            self.assertIsInstance(question['choix'], list)
    
    def test_extract_key_phrases(self):
        """Test l'extraction des phrases clés"""
        phrases = self.generator._extract_key_phrases(self.texte)
        self.assertGreater(len(phrases), 0)


class QCMViewsTest(TestCase):
    """Tests pour les vues QCM"""
    
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
    
    def test_qcm_index_requires_login(self):
        """Test que l'index QCM nécessite une connexion"""
        url = reverse('qcm:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_qcm_index_authenticated(self):
        """Test l'accès à l'index QCM quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('qcm:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qcm/index.html')
    
    def test_generate_qcm_get(self):
        """Test l'affichage du formulaire de génération"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('qcm:generate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qcm/generate.html')
    
    def test_generate_qcm_post(self):
        """Test la génération d'un QCM"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('qcm:generate')
        data = {
            'titre': 'QCM Test',
            'texte_source': 'Les mathématiques sont importantes. Une équation est une égalité.',
            'chapitre_id': self.chapitre.id
        }
        response = self.client.post(url, data)
        # Doit rediriger après génération
        self.assertEqual(response.status_code, 302)
        # Vérifier que le QCM est créé
        self.assertTrue(QCM.objects.filter(titre='QCM Test').exists())
    
    def test_submit_qcm(self):
        """Test la soumission d'un QCM"""
        self.client.login(username='testuser', password='testpass123')
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
        choix_correct = Choix.objects.create(
            question=question,
            texte='Réponse correcte',
            est_correct=True
        )
        choix_incorrect = Choix.objects.create(
            question=question,
            texte='Réponse incorrecte',
            est_correct=False
        )
        
        url = reverse('qcm:submit', kwargs={'qcm_id': qcm.id})
        data = {
            'reponses': {
                str(question.id): str(choix_correct.id)
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        # Vérifier que le résultat est créé
        self.assertTrue(ResultatQCM.objects.filter(qcm=qcm).exists())



