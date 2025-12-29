# Tests d'Authentification - Learnia

## ✅ Vérifications Effectuées

### 1. **Formulaire d'Inscription (Register)**
- ✅ Formulaire personnalisé avec champs : username, email, password1, password2, niveau_etude, classe, ecole
- ✅ Validation des mots de passe (cohérence, complexité)
- ✅ Validation de l'email
- ✅ Affichage des erreurs de formulaire
- ✅ Messages de succès après inscription
- ✅ Redirection automatique vers la page d'accueil après inscription
- ✅ Connexion automatique après inscription
- ✅ Styles Bootstrap appliqués aux champs

### 2. **Formulaire de Connexion (Login)**
- ✅ Formulaire Django standard avec username et password
- ✅ Gestion du paramètre `next` pour redirection après connexion
- ✅ Messages d'erreur en cas d'échec
- ✅ Protection CSRF
- ✅ Redirection des utilisateurs déjà connectés
- ✅ Lien vers l'inscription
- ✅ Styles Bootstrap appliqués

### 3. **Profil Utilisateur (Profile)**
- ✅ Affichage et modification des informations du profil
- ✅ Upload d'avatar (image)
- ✅ Messages de succès après modification
- ✅ Protection par `@login_required`
- ✅ Affichage de l'avatar actuel s'il existe
- ✅ Gestion du formulaire avec fichiers (enctype)

### 4. **URLs et Redirections**
- ✅ `/accounts/login/` → Page de connexion
- ✅ `/accounts/logout/` → Déconnexion puis redirection vers home
- ✅ `/accounts/register/` → Page d'inscription
- ✅ `/accounts/profile/` → Page de profil (protégée)
- ✅ `LOGIN_URL = 'accounts:login'` configuré
- ✅ `LOGIN_REDIRECT_URL = 'home'` configuré
- ✅ `LOGOUT_REDIRECT_URL = 'home'` configuré

### 5. **Templates**
- ✅ Templates indépendants de crispy_forms (fonctionnent sans dépendance)
- ✅ Affichage des erreurs de formulaire
- ✅ Messages de succès/erreur avec Bootstrap alerts
- ✅ Liens entre login et register
- ✅ Responsive design avec Bootstrap
- ✅ Icônes Bootstrap Icons

### 6. **Sécurité**
- ✅ Protection CSRF sur tous les formulaires
- ✅ Validation des mots de passe (longueur, complexité)
- ✅ Validation de l'email
- ✅ Protection des pages sensibles avec `@login_required`
- ✅ Hashage des mots de passe (géré par Django)

## 🔍 Tests à Effectuer Manuellement

### Test d'Inscription
1. Aller sur `/accounts/register/`
2. Remplir le formulaire :
   - Username : `testuser`
   - Email : `test@example.com`
   - Niveau : `6e`
   - Classe : `6ème A` (optionnel)
   - École : `École Test` (optionnel)
   - Mot de passe : `testpass123`
   - Confirmation : `testpass123`
3. Cliquer sur "S'inscrire"
4. **Résultat attendu** : Redirection vers la page d'accueil, message de succès, utilisateur connecté

### Test de Connexion
1. Aller sur `/accounts/login/`
2. Entrer :
   - Username : `testuser`
   - Mot de passe : `testpass123`
3. Cliquer sur "Se connecter"
4. **Résultat attendu** : Redirection vers la page d'accueil, utilisateur connecté

### Test de Connexion avec Erreur
1. Aller sur `/accounts/login/`
2. Entrer un mauvais username ou mot de passe
3. Cliquer sur "Se connecter"
4. **Résultat attendu** : Message d'erreur affiché, reste sur la page de connexion

### Test de Déconnexion
1. Se connecter
2. Cliquer sur "Déconnexion" dans le menu
3. **Résultat attendu** : Déconnexion, redirection vers la page d'accueil

### Test d'Accès Protégé
1. Se déconnecter
2. Aller sur `/accounts/profile/` directement
3. **Résultat attendu** : Redirection vers `/accounts/login/?next=/accounts/profile/`

### Test de Modification de Profil
1. Se connecter
2. Aller sur `/accounts/profile/`
3. Modifier les informations (prénom, nom, email, etc.)
4. Uploader un avatar (optionnel)
5. Cliquer sur "Enregistrer"
6. **Résultat attendu** : Message de succès, informations mises à jour

### Test de Validation
1. Essayer de s'inscrire avec :
   - Mots de passe différents → Erreur attendue
   - Email invalide → Erreur attendue
   - Username déjà utilisé → Erreur attendue
   - Mot de passe trop court → Erreur attendue

## 📝 Notes Importantes

- Les templates fonctionnent **sans crispy_forms** (pas de dépendance)
- Tous les champs ont les classes Bootstrap appropriées
- Les messages d'erreur sont affichés de manière claire
- L'avatar est géré avec upload de fichier
- La date de naissance utilise un input type="date"

## 🐛 Problèmes Potentiels et Solutions

### Si l'inscription ne fonctionne pas :
1. Vérifier que la base de données est migrée : `python manage.py migrate`
2. Vérifier les logs Django pour les erreurs
3. Vérifier que le modèle User est bien configuré

### Si la connexion ne fonctionne pas :
1. Vérifier que l'utilisateur existe dans la base
2. Vérifier que le mot de passe est correct
3. Vérifier les settings Django (AUTH_USER_MODEL)

### Si les redirections ne fonctionnent pas :
1. Vérifier LOGIN_REDIRECT_URL dans settings.py
2. Vérifier que la vue 'home' existe dans urls.py
3. Vérifier que le paramètre `next` est géré

## ✅ Conclusion

Tous les fichiers d'authentification ont été vérifiés et corrigés. Les fonctionnalités sont prêtes à être testées. Les templates sont indépendants et fonctionnent sans dépendances supplémentaires.


