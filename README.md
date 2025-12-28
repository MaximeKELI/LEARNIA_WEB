# Learnia - Plateforme Éducative Togolaise

Learnia est une application web éducative complète développée en Django, conçue spécialement pour les élèves togolais du primaire à la terminale. L'application intègre plusieurs fonctionnalités basées sur l'intelligence artificielle et fonctionne entièrement en mode hors ligne avec une base de données SQLite locale.

## 🎯 Fonctionnalités

### 🎓 Modules Éducatifs

#### 1. **Tuteur Intelligent (Chatbot éducatif)**
- Pose de questions sur les cours
- Explications simples et adaptées
- Réponses générées par IA (simulation)
- Mode hors ligne avec fallback local

#### 2. **Générateur de QCM**
- Génération automatique de questions à partir d'un texte
- Interface de quiz interactive
- Corrections automatiques
- Historique des résultats

#### 3. **Mémorisation Intelligente (Système Leitner)**
- Système de flashcards adaptatif
- Révision basée sur la performance
- Intervalles de révision optimisés
- Suivi de progression

#### 4. **Résumé Automatique des Leçons**
- Extraction des points clés
- Résumés structurés
- Sauvegarde des résumés
- Association aux chapitres

#### 5. **Traduction en Langues Locales**
- Traduction français → éwé
- Traduction français → kabiyè
- Dictionnaire local intégré
- Historique des traductions

#### 6. **Analyse des Performances**
- Historique des résultats
- Graphiques de progression
- Statistiques par matière
- Suggestions d'amélioration

#### 7. **Planificateur de Révision Intelligent**
- Planning personnalisé
- Gestion des matières et examens
- Rappels automatiques
- Génération de plans de révision

#### 8. **Reconnaissance de Devoirs Manuscrits (OCR)**
- Capture photo des devoirs
- Reconnaissance de texte (Tesseract)
- Correction automatique (simulation)
- Historique des devoirs

#### 9. **Orientation Scolaire**
- Questionnaire d'orientation
- Suggestions de filières
- Conseils de métiers
- Informations sur les parcours

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Configuration de la base de données

```bash
python manage.py migrate
```

### Création d'un superutilisateur

```bash
python manage.py createsuperuser
```

### Lancement du serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

## 📁 Structure du Projet

```
learnia_web/
├── accounts/          # Gestion des utilisateurs
├── tutor/            # Tuteur intelligent
├── qcm/              # Générateur de QCM
├── flashcards/       # Système de flashcards
├── resume/           # Résumé automatique
├── translation/      # Traduction
├── analytics/        # Analyses de performance
├── planner/          # Planificateur
├── ocr/              # Reconnaissance de texte
├── orientation/      # Orientation scolaire
├── templates/        # Templates HTML
├── static/           # Fichiers statiques (CSS, JS)
├── learnia/          # Configuration Django
└── manage.py         # Script de gestion Django
```

## 🗄️ Base de Données

L'application utilise SQLite par défaut (fichier `db.sqlite3`). La structure inclut :

- **Comptes utilisateurs** : Profils élèves avec niveaux d'étude
- **Matieres et Chapitres** : Organisation du contenu éducatif
- **Conversations** : Historique des interactions avec le tuteur
- **QCM et Questions** : Quiz et résultats
- **Flashcards** : Cartes de mémorisation avec système Leitner
- **Résumés** : Résumés générés automatiquement
- **Traductions** : Historique des traductions
- **Performances** : Statistiques et analyses
- **Planification** : Examens et révisions planifiées
- **Devoirs** : Devoirs manuscrits avec OCR
- **Orientation** : Questionnaires et suggestions

## 🎨 Technologies Utilisées

- **Backend** : Django 4.2+
- **Frontend** : Bootstrap 5, HTML5, CSS3
- **Base de données** : SQLite
- **OCR** : Tesseract (pytesseract)
- **Traitement de texte** : NLTK, regex
- **Graphiques** : Matplotlib (pour futures visualisations)

## 📝 Configuration

### Variables d'environnement

Le fichier `learnia/settings.py` contient la configuration principale. Pour la production, vous devrez :

1. Changer `SECRET_KEY`
2. Mettre `DEBUG = False`
3. Configurer `ALLOWED_HOSTS`
4. Configurer un serveur web (nginx + gunicorn)

### OCR (Optionnel)

Pour utiliser la fonctionnalité OCR, installez Tesseract :

**Ubuntu/Debian** :
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

**macOS** :
```bash
brew install tesseract tesseract-lang
```

## 🚀 Utilisation

### Première utilisation

1. Créez un compte élève
2. Renseignez votre niveau d'étude et classe
3. Explorez les différentes fonctionnalités

### Créer un QCM

1. Allez dans "QCM" → "Créer un QCM"
2. Collez le texte de votre cours
3. Le système génère automatiquement des questions
4. Répondez et consultez vos résultats

### Utiliser les Flashcards

1. Créez un deck de flashcards
2. Ajoutez des cartes (recto/verso)
3. Utilisez la fonction de révision
4. Le système Leitner adapte les intervalles de révision

### Tuteur Intelligent

1. Créez une conversation
2. Posez vos questions sur un cours
3. Recevez des explications adaptées
4. Consultez l'historique de vos conversations

## 🔒 Sécurité

- Authentification utilisateur Django
- Protection CSRF activée
- Sessions sécurisées
- Validation des formulaires

## 📊 Admin Django

Accédez à l'interface d'administration :
- URL : `/admin/`
- Utilisez le superutilisateur créé précédemment

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Faire un commit de vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est développé pour l'éducation au Togo.

## 👥 Équipe

Développé avec ❤️ pour les élèves togolais.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue.

## 🔮 Évolutions Futures

- Intégration d'un vrai modèle IA (Hugging Face, OpenAI, etc.)
- Application mobile (React Native)
- Synchronisation cloud
- Contenu multilingue élargi
- Intégration avec des plateformes éducatives existantes
