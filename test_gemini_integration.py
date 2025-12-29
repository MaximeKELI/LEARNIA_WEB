"""
Script de test pour vérifier l'intégration Gemini
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnia.settings')
django.setup()

from learnia.gemini_service import GeminiService
from tutor.services import TuteurService
from qcm.services import QCMGenerator
from resume.services import ResumeService
from accounts.models import User, Matiere, Chapitre


def test_gemini_service():
    """Test du service Gemini de base"""
    print("\n" + "="*60)
    print("TEST 1: Service Gemini de base")
    print("="*60)
    
    # Vérifier la disponibilité
    is_available = GeminiService.is_available()
    print(f"✓ Gemini disponible: {is_available}")
    
    if not is_available:
        print("⚠ Gemini n'est pas disponible. Vérifiez la clé API dans settings.py")
        return False
    
    # Test simple
    print("\nTest de génération de texte...")
    response = GeminiService.generate_text(
        prompt="Dis bonjour en français et présente-toi comme un tuteur intelligent",
        temperature=0.7
    )
    
    if response:
        print(f"✓ Réponse reçue: {response[:150]}...")
        return True
    else:
        print("✗ Aucune réponse reçue")
        return False


def test_tuteur_service():
    """Test du service tuteur"""
    print("\n" + "="*60)
    print("TEST 2: Service Tuteur Intelligent")
    print("="*60)
    
    service = TuteurService()
    
    # Test 1: Question simple
    print("\nTest 1: Question simple")
    question = "Qu'est-ce que la photosynthèse ?"
    response = service.get_response(question)
    print(f"Question: {question}")
    print(f"Réponse: {response[:200]}...")
    
    if response and len(response) > 50:
        print("✓ Service tuteur fonctionne")
    else:
        print("✗ Réponse trop courte ou vide")
    
    # Test 2: Question avec contexte
    print("\nTest 2: Question avec contexte")
    try:
        # Créer un utilisateur de test si nécessaire
        user, _ = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com', 'niveau_etude': '3e'}
        )
        
        # Créer une matière et un chapitre de test
        matiere, _ = Matiere.objects.get_or_create(nom='Sciences')
        chapitre, _ = Chapitre.objects.get_or_create(
            titre='La Photosynthèse',
            matiere=matiere,
            defaults={'numero': 1, 'description': 'Chapitre sur la photosynthèse'}
        )
        
        question2 = "Explique-moi comment fonctionne la photosynthèse"
        response2 = service.get_response(question2, chapitre=chapitre, user=user)
        print(f"Question: {question2}")
        print(f"Réponse: {response2[:200]}...")
        
        if response2 and len(response2) > 50:
            print("✓ Service tuteur avec contexte fonctionne")
        else:
            print("✗ Réponse avec contexte insuffisante")
            
    except Exception as e:
        print(f"⚠ Erreur lors du test avec contexte: {e}")
    
    return True


def test_qcm_generator():
    """Test du générateur de QCM"""
    print("\n" + "="*60)
    print("TEST 3: Générateur de QCM")
    print("="*60)
    
    generator = QCMGenerator()
    
    texte = """
    La photosynthèse est le processus par lequel les plantes vertes utilisent la lumière du soleil,
    le dioxyde de carbone de l'air et l'eau du sol pour produire du glucose et de l'oxygène.
    Ce processus se déroule principalement dans les feuilles, dans des structures appelées chloroplastes.
    La chlorophylle, un pigment vert, capture l'énergie lumineuse nécessaire à cette réaction.
    L'équation générale de la photosynthèse est : 6CO2 + 6H2O + lumière → C6H12O6 + 6O2.
    """
    
    print("\nGénération de questions à partir du texte...")
    questions = generator.generate_questions(texte, nombre_questions=3)
    
    if questions and len(questions) > 0:
        print(f"✓ {len(questions)} question(s) générée(s)")
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}: {q.get('texte', 'N/A')[:80]}...")
            print(f"  Nombre de choix: {len(q.get('choix', []))}")
            correct_answers = [c for c in q.get('choix', []) if c.get('correct')]
            print(f"  Réponses correctes: {len(correct_answers)}")
        return True
    else:
        print("✗ Aucune question générée")
        return False


def test_resume_service():
    """Test du service de résumé"""
    print("\n" + "="*60)
    print("TEST 4: Service de Résumé")
    print("="*60)
    
    service = ResumeService()
    
    texte = """
    La photosynthèse est un processus biologique fondamental qui permet aux plantes vertes,
    aux algues et à certaines bactéries de convertir l'énergie lumineuse en énergie chimique.
    Ce processus se déroule en deux phases principales : la phase claire et la phase sombre.
    
    Dans la phase claire, qui se produit dans les thylakoïdes des chloroplastes, la lumière
    est captée par la chlorophylle et d'autres pigments photosynthétiques. Cette énergie
    lumineuse est utilisée pour diviser les molécules d'eau (photolyse), libérant de l'oxygène
    comme sous-produit et produisant de l'ATP et du NADPH.
    
    La phase sombre, également appelée cycle de Calvin, se produit dans le stroma des chloroplastes.
    Elle utilise l'ATP et le NADPH produits lors de la phase claire pour fixer le dioxyde de
    carbone et produire du glucose. Ce glucose peut ensuite être utilisé par la plante pour
    sa croissance et son développement, ou stocké sous forme d'amidon.
    
    La photosynthèse est essentielle à la vie sur Terre car elle produit l'oxygène que nous
    respirons et constitue la base de la chaîne alimentaire. Sans la photosynthèse, la vie
    telle que nous la connaissons ne serait pas possible.
    """
    
    print("\nGénération d'un résumé...")
    resume = service.generate_resume(texte, longueur_max=150)
    
    if resume:
        print(f"✓ Résumé généré ({len(resume)} caractères)")
        print(f"Résumé: {resume[:300]}{'...' if len(resume) > 300 else ''}")
        return True
    else:
        print("✗ Aucun résumé généré")
        return False
    
    # Test extraction de points clés
    print("\nExtraction de points clés...")
    points = service.extraire_points_cles(texte)
    
    if points:
        print(f"✓ {len(points)} point(s) clé(s) extrait(s)")
        for i, point in enumerate(points, 1):
            print(f"  {i}. {point[:80]}...")
    else:
        print("✗ Aucun point clé extrait")


def main():
    """Exécute tous les tests"""
    print("\n" + "="*60)
    print("TESTS D'INTÉGRATION GEMINI - LEARNIA")
    print("="*60)
    
    results = []
    
    # Test 1: Service Gemini de base
    results.append(("Service Gemini", test_gemini_service()))
    
    # Test 2: Service Tuteur
    results.append(("Service Tuteur", test_tuteur_service()))
    
    # Test 3: Générateur QCM
    results.append(("Générateur QCM", test_qcm_generator()))
    
    # Test 4: Service Résumé
    results.append(("Service Résumé", test_resume_service()))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    for name, result in results:
        status = "✓ RÉUSSI" if result else "✗ ÉCHOUÉ"
        print(f"{name}: {status}")
    
    total = len(results)
    reussis = sum(1 for _, r in results if r)
    print(f"\nTotal: {reussis}/{total} tests réussis")
    
    if reussis == total:
        print("\n🎉 Tous les tests sont passés avec succès !")
    else:
        print(f"\n⚠ {total - reussis} test(s) ont échoué")


if __name__ == '__main__':
    main()

