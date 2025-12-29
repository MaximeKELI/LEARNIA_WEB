#!/usr/bin/env python
"""
Script rapide pour vérifier l'intégrité du projet avant le déploiement
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnia.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.conf import settings

def check_templates():
    """Vérifie que tous les templates existent"""
    print("🔍 Vérification des templates...")
    
    templates_dir = Path(settings.BASE_DIR) / 'templates'
    all_templates = []
    
    # Liste tous les templates HTML
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), templates_dir)
                all_templates.append(rel_path.replace(os.sep, '/'))
    
    missing = []
    for template in all_templates:
        try:
            get_template(template)
        except TemplateDoesNotExist:
            missing.append(template)
    
    if missing:
        print(f"❌ {len(missing)} template(s) manquant(s):")
        for t in missing:
            print(f"   - {t}")
        return False
    else:
        print(f"✅ Tous les {len(all_templates)} templates sont présents")
        return True

def check_urls():
    """Vérifie que toutes les URLs principales sont valides"""
    print("\n🔍 Vérification des URLs...")
    
    urls_to_test = [
        'home',
        'accounts:login',
        'accounts:register',
        'tutor:index',
        'qcm:index',
        'flashcards:index',
        'planner:index',
        'gamification:dashboard',
        'notes:list',
        'calendar:view',
        'fiches:list',
    ]
    
    invalid = []
    for url_name in urls_to_test:
        try:
            reverse(url_name)
        except NoReverseMatch as e:
            invalid.append(f"{url_name}: {str(e)}")
    
    if invalid:
        print(f"❌ {len(invalid)} URL(s) invalide(s):")
        for u in invalid:
            print(f"   - {u}")
        return False
    else:
        print(f"✅ Toutes les {len(urls_to_test)} URLs principales sont valides")
        return True

def check_apps():
    """Vérifie que toutes les applications sont bien configurées"""
    print("\n🔍 Vérification des applications...")
    
    apps = [
        'accounts', 'tutor', 'qcm', 'flashcards', 'resume',
        'translation', 'analytics', 'planner', 'ocr', 'orientation',
        'export', 'gamification', 'notes', 'calendar_app', 'fiches'
    ]
    
    missing_apps = []
    for app in apps:
        try:
            __import__(app)
        except ImportError:
            missing_apps.append(app)
    
    if missing_apps:
        print(f"❌ {len(missing_apps)} application(s) manquante(s):")
        for app in missing_apps:
            print(f"   - {app}")
        return False
    else:
        print(f"✅ Toutes les {len(apps)} applications sont installées")
        return True

def check_models():
    """Vérifie que tous les modèles peuvent être importés"""
    print("\n🔍 Vérification des modèles...")
    
    models_to_check = [
        ('accounts.models', 'User'),
        ('accounts.models', 'Matiere'),
        ('accounts.models', 'Chapitre'),
        ('qcm.models', 'QCM'),
        ('flashcards.models', 'Deck'),
        ('gamification.models', 'Badge'),
        ('notes.models', 'Note'),
        ('calendar_app.models', 'EvenementScolaire'),
        ('fiches.models', 'FicheRevision'),
    ]
    
    invalid = []
    for module_name, model_name in models_to_check:
        try:
            module = __import__(module_name, fromlist=[model_name])
            getattr(module, model_name)
        except (ImportError, AttributeError) as e:
            invalid.append(f"{module_name}.{model_name}: {str(e)}")
    
    if invalid:
        print(f"❌ {len(invalid)} modèle(s) invalide(s):")
        for m in invalid:
            print(f"   - {m}")
        return False
    else:
        print(f"✅ Tous les {len(models_to_check)} modèles sont valides")
        return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("VÉRIFICATION D'INTÉGRITÉ - LEARNIA")
    print("=" * 60)
    
    results = []
    results.append(check_apps())
    results.append(check_models())
    results.append(check_templates())
    results.append(check_urls())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ TOUS LES TESTS SONT PASSÉS !")
        return 0
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        return 1

if __name__ == '__main__':
    from pathlib import Path
    sys.exit(main())



