"""
Tests unitaires pour l'application gamification
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Badge, UserBadge, UserProgress, Leaderboard
from .services import GamificationService

User = get_user_model()


class GamificationModelsTest(TestCase):
    """Tests pour les modèles de gamification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_create_badge(self):
        """Test la création d'un badge"""
        badge = Badge.objects.create(
            nom='Premier Pas',
            description='Complétez votre premier QCM',
            icone='🎯',
            condition_type='qcm_first',
            points_xp=10
        )
        self.assertEqual(badge.nom, 'Premier Pas')
        self.assertEqual(badge.condition_type, 'qcm_first')
        self.assertEqual(badge.points_xp, 10)
    
    def test_create_user_progress(self):
        """Test la création d'une progression utilisateur"""
        progress, created = UserProgress.objects.get_or_create(user=self.user)
        self.assertTrue(created)
        self.assertEqual(progress.points_xp, 0)
        self.assertEqual(progress.niveau, 1)
        self.assertEqual(progress.jours_streak, 0)
    
    def test_user_progress_ajouter_xp(self):
        """Test l'ajout de points XP"""
        progress = UserProgress.objects.create(user=self.user)
        progress.ajouter_xp(50)
        self.assertEqual(progress.points_xp, 50)
        self.assertEqual(progress.niveau, 1)  # Toujours niveau 1 car < 100
    
    def test_user_progress_niveau_upgrade(self):
        """Test le passage de niveau"""
        progress = UserProgress.objects.create(user=self.user)
        progress.ajouter_xp(100)
        self.assertEqual(progress.niveau, 2)  # Niveau 2 car >= 100 XP
        progress.ajouter_xp(100)
        self.assertEqual(progress.niveau, 3)  # Niveau 3 car >= 200 XP
    
    def test_create_user_badge(self):
        """Test l'attribution d'un badge"""
        badge = Badge.objects.create(
            nom='Test Badge',
            description='Test',
            condition_type='qcm_first',
            points_xp=10
        )
        user_badge = UserBadge.objects.create(
            user=self.user,
            badge=badge
        )
        self.assertEqual(user_badge.user, self.user)
        self.assertEqual(user_badge.badge, badge)
    
    def test_user_badge_unique_together(self):
        """Test qu'un utilisateur ne peut pas avoir le même badge deux fois"""
        badge = Badge.objects.create(
            nom='Test Badge',
            description='Test',
            condition_type='qcm_first',
            points_xp=10
        )
        UserBadge.objects.create(user=self.user, badge=badge)
        # Tenter de créer un doublon
        with self.assertRaises(Exception):
            UserBadge.objects.create(user=self.user, badge=badge)


class GamificationServiceTest(TestCase):
    """Tests pour les services de gamification"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.service = GamificationService()
    
    def test_mettre_a_jour_streak(self):
        """Test la mise à jour de la série"""
        progress, _ = UserProgress.objects.get_or_create(user=self.user)
        self.service.mettre_a_jour_streak(self.user)
        progress.refresh_from_db()
        self.assertEqual(progress.jours_streak, 1)
    
    def test_ajouter_xp_qcm_perfect(self):
        """Test l'ajout d'XP pour un QCM parfait"""
        progress, _ = UserProgress.objects.get_or_create(user=self.user)
        initial_xp = progress.points_xp
        self.service.ajouter_xp_qcm(self.user, 100)
        progress.refresh_from_db()
        self.assertGreater(progress.points_xp, initial_xp)
        self.assertEqual(progress.qcm_completes, 1)
    
    def test_ajouter_xp_qcm_bon_score(self):
        """Test l'ajout d'XP pour un bon score"""
        progress, _ = UserProgress.objects.get_or_create(user=self.user)
        initial_xp = progress.points_xp
        self.service.ajouter_xp_qcm(self.user, 85)
        progress.refresh_from_db()
        self.assertGreater(progress.points_xp, initial_xp)
    
    def test_ajouter_xp_flashcard(self):
        """Test l'ajout d'XP pour une flashcard"""
        progress, _ = UserProgress.objects.get_or_create(user=self.user)
        initial_count = progress.flashcards_creees
        self.service.ajouter_xp_flashcard(self.user)
        progress.refresh_from_db()
        self.assertEqual(progress.flashcards_creees, initial_count + 1)
    
    def test_ajouter_xp_tuteur(self):
        """Test l'ajout d'XP pour le tuteur"""
        progress, _ = UserProgress.objects.get_or_create(user=self.user)
        initial_count = progress.questions_tuteur
        self.service.ajouter_xp_tuteur(self.user)
        progress.refresh_from_db()
        self.assertEqual(progress.questions_tuteur, initial_count + 1)
    
    def test_get_leaderboard(self):
        """Test la récupération du classement"""
        # Créer plusieurs utilisateurs avec différents scores
        user2 = User.objects.create_user(username='user2', password='pass')
        user3 = User.objects.create_user(username='user3', password='pass')
        
        progress1 = UserProgress.objects.create(user=self.user, points_xp=100)
        progress2 = UserProgress.objects.create(user=user2, points_xp=200)
        progress3 = UserProgress.objects.create(user=user3, points_xp=50)
        
        leaderboard = self.service.get_leaderboard(limit=10)
        self.assertEqual(len(leaderboard), 3)
        # Vérifier que le classement est par ordre décroissant de XP
        self.assertEqual(leaderboard[0]['points_xp'], 200)
        self.assertEqual(leaderboard[1]['points_xp'], 100)
        self.assertEqual(leaderboard[2]['points_xp'], 50)


class GamificationViewsTest(TestCase):
    """Tests pour les vues de gamification"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
    
    def test_gamification_dashboard_requires_login(self):
        """Test que le dashboard nécessite une connexion"""
        url = reverse('gamification:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_gamification_dashboard_authenticated(self):
        """Test l'accès au dashboard quand connecté"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('gamification:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/dashboard.html')
        self.assertContains(response, 'Progression')
    
    def test_badges_list_authenticated(self):
        """Test la liste des badges"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('gamification:badges')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gamification/badges.html')

