# Guide des Tests Unitaires - Learnia

Ce document décrit les tests unitaires disponibles pour l'application Learnia.

## 📁 Structure des Tests

### Tests Backend (`accounts/tests.py`, `qcm/tests.py`, etc.)
Tests pour les fonctionnalités backend de chaque application :
- **Modèles** : Création, validation, méthodes
- **Vues** : Réponses HTTP, redirections, authentification
- **Services** : Logique métier
- **Formulaires** : Validation des données

### Tests Frontend (`frontend_tests.py`)
Tests pour l'interface utilisateur :
- **Templates** : Structure HTML, éléments présents
- **Navigation** : Liens, menus, redirections
- **Formulaires** : Champs, validation CSRF
- **Responsive** : Bootstrap, meta tags

### Tests Base de Données (`database_tests.py`)
Tests pour l'intégrité de la base de données :
- **Contraintes** : Unicité, unique_together
- **Relations** : ForeignKey, relations inverses
- **Transactions** : Rollback, atomicité
- **Intégrité** : Valeurs par défaut, contraintes

## 🚀 Exécution des Tests

### Tous les tests
```bash
python manage.py test
```

### Tests d'une application spécifique
```bash
python manage.py test accounts
python manage.py test qcm
python manage.py test flashcards
```

### Tests frontend
```bash
python manage.py test frontend_tests
```

### Tests base de données
```bash
python manage.py test database_tests
```

### Tests avec couverture de code
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML dans htmlcov/
```

### Tests spécifiques
```bash
python manage.py test accounts.tests.UserModelTest
python manage.py test accounts.tests.UserModelTest.test_create_user
```

## 📊 Types de Tests

### 1. Tests de Modèles
Vérifient que les modèles fonctionnent correctement :
- Création d'objets
- Méthodes `__str__`
- Relations entre modèles
- Contraintes de base de données

**Exemple** :
```python
def test_create_user(self):
    user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )
    self.assertEqual(user.username, 'testuser')
```

### 2. Tests de Vues
Vérifient que les vues répondent correctement :
- Codes de statut HTTP
- Templates utilisés
- Redirections
- Authentification requise

**Exemple** :
```python
def test_login_get(self):
    response = self.client.get(reverse('accounts:login'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'accounts/login.html')
```

### 3. Tests de Services
Vérifient la logique métier :
- Génération de QCM
- Réponses du tuteur
- Calculs de scores

**Exemple** :
```python
def test_generate_questions(self):
    generator = QCMGenerator()
    questions = generator.generate_questions(texte, nombre_questions=3)
    self.assertGreater(len(questions), 0)
```

### 4. Tests Frontend
Vérifient l'interface utilisateur :
- Présence d'éléments HTML
- Liens fonctionnels
- Formulaires complets
- Responsive design

**Exemple** :
```python
def test_home_template(self):
    response = self.client.get(reverse('home'))
    self.assertContains(response, 'Learnia')
    self.assertContains(response, 'Tuteur Intelligent')
```

### 5. Tests Base de Données
Vérifient l'intégrité des données :
- Contraintes d'unicité
- Relations ForeignKey
- Suppression en cascade
- Transactions

**Exemple** :
```python
def test_matiere_code_unique(self):
    Matiere.objects.create(code='MATH', ...)
    with self.assertRaises(IntegrityError):
        Matiere.objects.create(code='MATH', ...)
```

## 📝 Écrire de Nouveaux Tests

### Structure d'un test
```python
from django.test import TestCase
from .models import MonModele

class MonModeleTest(TestCase):
    def setUp(self):
        # Configuration initiale pour chaque test
        pass
    
    def test_ma_fonctionnalite(self):
        # Code du test
        # Assertions
        pass
```

### Méthodes utiles
- `self.assertEqual(a, b)` : Vérifie l'égalité
- `self.assertTrue(x)` : Vérifie que x est True
- `self.assertContains(response, text)` : Vérifie la présence dans la réponse
- `self.assertTemplateUsed(response, template)` : Vérifie le template utilisé
- `self.assertRaises(Error)` : Vérifie qu'une erreur est levée

### Client de test
```python
client = Client()
# GET request
response = client.get('/url/')
# POST request
response = client.post('/url/', {'data': 'value'})
# Login
client.login(username='user', password='pass')
```

## 🎯 Coverage Cible

Objectif : **> 80% de couverture de code**

- Modèles : 100%
- Vues principales : > 90%
- Services : > 80%
- Templates : > 70%

## 🔍 Debugging des Tests

### Mode verbose
```bash
python manage.py test --verbosity=2
```

### Arrêter après la première erreur
```bash
python manage.py test --failfast
```

### Garder la base de test
```bash
python manage.py test --keepdb
```

### Tests avec PDB (débugger)
```python
import pdb
def test_something(self):
    pdb.set_trace()  # Arrête l'exécution ici
    # ...
```

## 📋 Checklist des Tests

Pour chaque nouvelle fonctionnalité, ajouter :

- [ ] Test de création du modèle
- [ ] Test des méthodes du modèle
- [ ] Test de la vue GET
- [ ] Test de la vue POST (données valides)
- [ ] Test de la vue POST (données invalides)
- [ ] Test d'authentification requise
- [ ] Test de redirection
- [ ] Test du template utilisé
- [ ] Test des contraintes de base de données
- [ ] Test des relations entre modèles

## 🐛 Problèmes Courants

### Erreur : "No such table"
```bash
python manage.py migrate
python manage.py test
```

### Erreur : "TemplateDoesNotExist"
Vérifier que les templates sont dans le bon répertoire.

### Erreur : "CSRF verification failed"
Utiliser `self.client.post()` avec les bonnes données.

## 📚 Ressources

- [Documentation Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Django TestCase](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.TestCase)
- [Coverage.py](https://coverage.readthedocs.io/)

