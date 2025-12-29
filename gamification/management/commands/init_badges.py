"""
Commande pour initialiser les badges par défaut
Usage: python manage.py init_badges
"""
from django.core.management.base import BaseCommand
from gamification.models import Badge


class Command(BaseCommand):
    help = 'Initialise les badges par défaut du système'

    def handle(self, *args, **options):
        badges_data = [
            {
                'nom': 'Premier Pas',
                'description': 'Complétez votre premier QCM',
                'icone': '🎯',
                'condition_type': 'qcm_first',
                'points_xp': 10,
            },
            {
                'nom': 'Parfait !',
                'description': 'Obtenez 100% à un QCM',
                'icone': '💯',
                'condition_type': 'qcm_perfect',
                'points_xp': 50,
            },
            {
                'nom': 'Débutant',
                'description': 'Complétez 10 QCM',
                'icone': '📚',
                'condition_type': 'qcm_10',
                'points_xp': 25,
            },
            {
                'nom': 'Expert QCM',
                'description': 'Complétez 50 QCM',
                'icone': '🏆',
                'condition_type': 'qcm_50',
                'points_xp': 100,
            },
            {
                'nom': 'Collectionneur',
                'description': 'Créez 10 flashcards',
                'icone': '🃏',
                'condition_type': 'flashcard_10',
                'points_xp': 20,
            },
            {
                'nom': 'Maître des Flashcards',
                'description': 'Créez 50 flashcards',
                'icone': '👑',
                'condition_type': 'flashcard_50',
                'points_xp': 75,
            },
            {
                'nom': 'Questionneur',
                'description': 'Posez 10 questions au tuteur',
                'icone': '🤔',
                'condition_type': 'tutor_10',
                'points_xp': 30,
            },
            {
                'nom': 'Série de 3',
                'description': 'Étudiez 3 jours consécutifs',
                'icone': '🔥',
                'condition_type': 'study_streak_3',
                'points_xp': 15,
            },
            {
                'nom': 'Série de 7',
                'description': 'Étudiez 7 jours consécutifs',
                'icone': '⚡',
                'condition_type': 'study_streak_7',
                'points_xp': 50,
            },
            {
                'nom': 'Légende',
                'description': 'Étudiez 30 jours consécutifs',
                'icone': '🌟',
                'condition_type': 'study_streak_30',
                'points_xp': 200,
            },
            {
                'nom': 'Profil Complet',
                'description': 'Complétez votre profil',
                'icone': '👤',
                'condition_type': 'profile_complete',
                'points_xp': 10,
            },
            {
                'nom': 'Résumé',
                'description': 'Créez votre premier résumé',
                'icone': '📝',
                'condition_type': 'first_resume',
                'points_xp': 15,
            },
        ]
        
        created = 0
        for badge_data in badges_data:
            badge, created_badge = Badge.objects.get_or_create(
                condition_type=badge_data['condition_type'],
                defaults=badge_data
            )
            if created_badge:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Badge créé: {badge.nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Badge existant: {badge.nom}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ {created} nouveau(x) badge(s) créé(s)')
        )


