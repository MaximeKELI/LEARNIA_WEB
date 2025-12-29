# Guide de Démarrage Rapide - Learnia

## Installation Rapide

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

### 5. Accéder à l'application

- Application : http://127.0.0.1:8000/
- Admin : http://127.0.0.1:8000/admin/

## Premiers Pas

### Pour l'administrateur

1. Connectez-vous à l'admin Django
2. Ajoutez des matières (Mathématiques, Français, Sciences, etc.)
3. Créez des chapitres pour chaque matière
4. Ajoutez du contenu dans les chapitres

### Pour un élève

1. Créez un compte depuis la page d'accueil
2. Renseignez votre niveau d'étude et classe
3. Explorez les fonctionnalités :
   - Tuteur Intelligent : Posez des questions
   - QCM : Générez des quiz à partir de textes
   - Flashcards : Créez des cartes de mémorisation
   - Planificateur : Organisez vos révisions

## Notes Importantes

- **Mode hors ligne** : L'application fonctionne entièrement hors ligne
- **Base de données** : SQLite est utilisée par défaut (fichier `db.sqlite3`)
- **OCR** : La fonctionnalité OCR nécessite Tesseract (optionnel)
- **IA** : Les fonctionnalités IA sont simulées localement (mode démo)

## Dépannage

### Erreur "No module named 'django'"

```bash
pip install -r requirements.txt
```

### Erreur de migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### Erreur de permissions (Linux/Mac)

```bash
chmod +x manage.py
```



