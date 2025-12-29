# 🔐 Informations Superutilisateur

## Superutilisateur créé avec succès !

### Identifiants par défaut

**Nom d'utilisateur:** `admin`  
**Email:** `admin@learnia.tg`  
**Mot de passe:** `admin123`

### Accès à l'interface d'administration

URL: **http://127.0.0.1:8000/admin/**

### ⚠️ Important - Sécurité

**Changez le mot de passe immédiatement après la première connexion !**

Pour changer le mot de passe :
1. Connectez-vous à l'admin
2. Allez dans "Users" → "admin"
3. Cliquez sur "Change password"
4. Entrez un nouveau mot de passe sécurisé

### Créer un autre superutilisateur

#### Méthode 1 : Script interactif
```bash
python create_superuser.py
```

#### Méthode 2 : Commande Django
```bash
python manage.py createsuperuser
```

#### Méthode 3 : Script avec arguments
```bash
python create_superuser.py username email password
```

### Fonctionnalités de l'admin

Une fois connecté, vous pouvez :
- ✅ Gérer tous les utilisateurs
- ✅ Gérer les matières et chapitres
- ✅ Gérer les QCM, flashcards, etc.
- ✅ Voir toutes les statistiques
- ✅ Gérer les badges et la gamification
- ✅ Exporter les données

---

**Note:** Gardez ces identifiants en sécurité et ne les partagez pas publiquement.

