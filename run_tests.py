#!/usr/bin/env python
"""
Script pour exécuter tous les tests unitaires
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'learnia.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    print("=" * 70)
    print("EXÉCUTION DES TESTS UNITAIRES - LEARNIA")
    print("=" * 70)
    
    # Liste des applications à tester
    apps_to_test = [
        'accounts',
        'qcm',
        'flashcards',
        'tutor',
    ]
    
    # Tests spécifiques
    specific_tests = [
        'frontend_tests',
        'database_tests',
    ]
    
    all_tests = apps_to_test + specific_tests
    
    failures = test_runner.run_tests(all_tests)
    
    if failures:
        sys.exit(1)
    else:
        print("\n" + "=" * 70)
        print("✅ TOUS LES TESTS SONT PASSÉS !")
        print("=" * 70)

