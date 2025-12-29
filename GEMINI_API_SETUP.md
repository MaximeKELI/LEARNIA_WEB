# Configuration de la Clé API Gemini

## ⚠️ Important : Votre clé API a été compromise

Votre clé API Gemini a été signalée comme compromise. Vous devez créer une nouvelle clé API.

## 🔑 Obtenir une Nouvelle Clé API

1. Allez sur [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key" ou "Get API Key"
4. Copiez la nouvelle clé API

## 🔒 Configuration Sécurisée

### Option 1 : Variable d'environnement (Recommandé)

**Linux/Mac :**
```bash
export GEMINI_API_KEY='votre_nouvelle_cle_api'
```

**Windows (PowerShell) :**
```powershell
$env:GEMINI_API_KEY='votre_nouvelle_cle_api'
```

**Pour rendre permanent (Linux/Mac) :**
Ajoutez à votre `~/.bashrc` ou `~/.zshrc` :
```bash
export GEMINI_API_KEY='votre_nouvelle_cle_api'
```

### Option 2 : Fichier .env (Alternative)

Créez un fichier `.env` à la racine du projet :
```bash
GEMINI_API_KEY=votre_nouvelle_cle_api
```

Puis installez `python-dotenv` :
```bash
pip install python-dotenv
```

Et modifiez `learnia/settings.py` pour charger le .env :
```python
from dotenv import load_dotenv
load_dotenv()
```

## ✅ Vérification

Après avoir configuré la clé, testez avec :
```bash
python3 manage.py runserver
```

Puis testez l'upload d'un devoir dans l'interface OCR.

## 🚨 Sécurité

- **NE COMMITEZ JAMAIS** votre clé API dans Git
- Le fichier `.env` est déjà dans `.gitignore`
- Utilisez toujours des variables d'environnement en production
- Régénérez votre clé si elle est compromise

## 📝 Note

Le code a été mis à jour pour utiliser `os.getenv('GEMINI_API_KEY')` au lieu d'une valeur en dur.
Si la variable d'environnement n'est pas définie, Gemini ne sera pas disponible mais l'application continuera de fonctionner avec les systèmes de fallback.

