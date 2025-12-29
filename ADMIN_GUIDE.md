# Guide d'Administration - Learnia

Ce guide décrit toutes les fonctionnalités disponibles dans l'interface d'administration Django pour gérer l'application Learnia.

## Accès à l'Administration

1. Créer un superutilisateur : `python manage.py createsuperuser`
2. Accéder à : `http://127.0.0.1:8000/admin/`
3. Se connecter avec les identifiants du superutilisateur

## Modules Disponibles

### 👥 **Accounts (Comptes)**

#### Utilisateurs (User)
- **Gestion complète** : Créer, modifier, supprimer des comptes élèves
- **Champs visibles** : Username, email, niveau d'étude, classe, école, date de naissance, avatar
- **Filtres** : Par niveau d'étude, date d'inscription, statut staff/actif
- **Recherche** : Par username, email, nom, prénom, classe, école
- **Actions** : Activer/désactiver, changer mot de passe, permissions

#### Matières (Matiere)
- **Liste** : Nom, code, niveau, icône, nombre de chapitres
- **Filtres** : Par niveau (Primaire, Collège, Lycée)
- **Recherche** : Par nom, code, description
- **Actions** : Créer, modifier, supprimer des matières

#### Chapitres (Chapitre)
- **Liste** : Titre, matière, numéro, niveau, date de création
- **Filtres** : Par matière, niveau, date de création
- **Recherche** : Par titre, contenu, matière
- **Fonctionnalités** : Affichage de la matière avec sélection optimisée

---

### 🤖 **Tutor (Tuteur Intelligent)**

#### Conversations (Conversation)
- **Liste** : Titre, utilisateur, chapitre, nombre de messages, dates
- **Filtres** : Par date, matière du chapitre
- **Recherche** : Par titre, username
- **Inlines** : Affiche tous les messages de la conversation
- **Informations** : Dates de création et mise à jour

#### Messages (Message)
- **Liste** : Conversation, rôle (user/assistant), aperçu du contenu, date
- **Filtres** : Par rôle, date
- **Recherche** : Par contenu, titre de conversation
- **Fonctionnalités** : Aperçu du contenu tronqué à 100 caractères

---

### ❓ **QCM (Générateur de Quiz)**

#### QCM
- **Liste** : Titre, utilisateur, chapitre, nombre de questions, date
- **Filtres** : Par date, matière
- **Recherche** : Par titre, username, texte source
- **Inlines** : Questions directement visibles et modifiables
- **Champs** : Texte source visible pour référence

#### Questions (Question)
- **Liste** : Numéro, QCM, texte (tronqué), nombre de choix, bonne réponse
- **Filtres** : Par QCM, matière
- **Recherche** : Par texte, titre du QCM
- **Inlines** : Choix de réponse directement modifiables
- **Fonctionnalités** : Affiche automatiquement la bonne réponse

#### Choix (Choix)
- **Liste** : Question, texte (tronqué), statut correct/incorrect
- **Filtres** : Par statut (correct/incorrect), QCM
- **Recherche** : Par texte, texte de la question

#### Résultats QCM (ResultatQCM)
- **Liste** : Utilisateur, QCM, score, total, pourcentage, date
- **Filtres** : Par date, matière
- **Recherche** : Par username, titre du QCM
- **Hiérarchie de dates** : Navigation par date
- **Optimisation** : Utilise `select_related` pour de meilleures performances

---

### 📚 **Flashcards (Mémorisation)**

#### Decks (Deck)
- **Liste** : Titre, utilisateur, chapitre, nombre de flashcards, date
- **Filtres** : Par date, matière
- **Recherche** : Par titre, description, username
- **Inlines** : Flashcards directement visibles et modifiables
- **Actions** : Créer, modifier, supprimer des decks

#### Flashcards (Flashcard)
- **Liste** : Recto (tronqué), deck, niveau, nombre de révisions, nombre de succès, prochaine révision
- **Filtres** : Par niveau (0-4), deck, date de prochaine révision
- **Recherche** : Par recto, verso, titre du deck
- **Champs en lecture seule** : Niveau, statistiques, dates (gérés automatiquement)
- **Hiérarchie de dates** : Par date de prochaine révision

#### Révisions (Revision)
- **Liste** : Utilisateur, flashcard (aperçu), réussie/échouée, temps de réponse, date
- **Filtres** : Par statut (réussie/échouée), date
- **Recherche** : Par contenu de la flashcard, username
- **Hiérarchie de dates** : Par date de révision

---

### 📝 **Resume (Résumés)**

#### Résumés (Resume)
- **Liste** : Titre, utilisateur, chapitre, longueur original, longueur résumé, nombre de points clés, date
- **Filtres** : Par date, matière
- **Recherche** : Par titre, texte original, texte résumé, username
- **Fieldsets** : Organisation en sections (Informations, Contenu, Dates)
- **Champs en lecture seule** : Dates, points clés (générés automatiquement)
- **Statistiques** : Affichage des longueurs et nombre de points clés

---

### 🌍 **Translation (Traduction)**

#### Traductions (Traduction)
- **Liste** : Utilisateur, texte original (aperçu), langue originale, langue cible, date
- **Filtres** : Par langues (originale/cible), date
- **Recherche** : Par texte original, texte traduit, username
- **Hiérarchie de dates** : Par date de traduction

#### Dictionnaire (Dictionnaire)
- **Liste** : Mot français, mot éwé, mot kabiyè, catégorie
- **Filtres** : Par catégorie
- **Recherche** : Par mots (français, éwé, kabiyè), définition
- **Fieldsets** : Organisation en sections (Mots, Informations)
- **Actions** : Gérer le dictionnaire local pour améliorer les traductions

---

### 📊 **Analytics (Analyses)**

#### Performances (Performance)
- **Liste** : Utilisateur, matière, score moyen, nombre QCM, nombre flashcards, temps d'étude (heures), dernière mise à jour
- **Filtres** : Par matière, date de mise à jour
- **Recherche** : Par username, nom de matière
- **Calculs automatiques** : Conversion minutes → heures
- **Hiérarchie de dates** : Par date de mise à jour

#### Activités (Activite)
- **Liste** : Utilisateur, type d'activité, description (aperçu), durée (minutes), date
- **Filtres** : Par type d'activité, date
- **Recherche** : Par description, username
- **Types** : QCM, Flashcard, Tuteur, Résumé, Traduction

---

### 📅 **Planner (Planificateur)**

#### Examens (Examen)
- **Liste** : Nom, utilisateur, matière, date d'examen, jours restants (avec code couleur), date de création
- **Filtres** : Par date d'examen, matière, date de création
- **Recherche** : Par nom, description, username, matière
- **Indicateurs visuels** :
  - 🔴 Rouge : Examen passé
  - 🟠 Orange : Aujourd'hui ou dans moins de 7 jours
  - ⚪ Normal : Plus de 7 jours
- **Hiérarchie de dates** : Par date d'examen

#### Révisions Planifiées (RevisionPlanifiee)
- **Liste** : Chapitre, utilisateur, date de révision, type, durée prévue, terminée, date de création
- **Filtres** : Par type, statut (terminée/non terminée), date, matière
- **Recherche** : Par titre du chapitre, username
- **Actions en masse** :
  - Marquer comme terminée
  - Marquer comme non terminée
- **Hiérarchie de dates** : Par date de révision

#### Rappels (Rappel)
- **Liste** : Titre, utilisateur, date du rappel, envoyé, date de création
- **Filtres** : Par statut (envoyé/non envoyé), date
- **Recherche** : Par titre, message, username
- **Actions en masse** :
  - Marquer comme envoyé
  - Marquer comme non envoyé
- **Hiérarchie de dates** : Par date du rappel

---

### 📷 **OCR (Reconnaissance de Devoirs)**

#### Devoirs (Devoir)
- **Liste** : Utilisateur, matière, note (avec code couleur), aperçu image, texte (aperçu), date
- **Filtres** : Par matière, date, note
- **Recherche** : Par texte reconnu, matière, commentaires, username
- **Codes couleur pour notes** :
  - 🟢 Vert : ≥ 16/20 (Excellent)
  - 🔵 Bleu : ≥ 12/20 (Bon)
  - 🟠 Orange : ≥ 10/20 (Passable)
  - 🔴 Rouge : < 10/20 (Insuffisant)
- **Aperçus** : Image miniature dans la liste, image grande dans le détail
- **Hiérarchie de dates** : Par date de création

---

### 🧭 **Orientation (Orientation Scolaire)**

#### Questionnaires (Questionnaire)
- **Liste** : Utilisateur, filière suggérée, scores (scientifique, littéraire, commercial, technique), date
- **Filtres** : Par filière suggérée, date
- **Recherche** : Par username, filière
- **Fieldsets** : Organisation en sections (Utilisateur, Résultats, Détails, Dates)
- **Champs en lecture seule** : Réponses JSON, métiers suggérés (calculés automatiquement)

#### Filières (Filiere)
- **Liste** : Nom, code, type, nombre de métiers
- **Filtres** : Par type (Scientifique, Littéraire, Commercial, Technique)
- **Recherche** : Par nom, code, description
- **Fieldsets** : Organisation en sections (Informations, Description, Détails)
- **Champs** : Matières principales, métiers (JSON)

#### Métiers (Metier)
- **Liste** : Nom, nombre de filières, formation requise (aperçu)
- **Recherche** : Par nom, description, formation requise
- **Filtres horizontaux** : Sélection multiple des filières associées
- **Fieldsets** : Organisation en sections (Informations, Formation, Filières)

---

## Fonctionnalités Générales de l'Admin

### 🔍 Recherche Avancée
- Tous les modules ont des champs de recherche optimisés
- Recherche sur les champs pertinents de chaque modèle
- Recherche sur les relations (ex: `user__username`, `chapitre__matiere`)

### 📊 Filtres
- Filtres par dates, statuts, catégories
- Filtres combinables pour affiner les résultats
- Hiérarchie de dates pour navigation rapide

### 📋 Affichage Optimisé
- Colonnes personnalisées avec méthodes (`nombre_questions`, `texte_court`, etc.)
- Aperçus tronqués pour les longs textes
- Codes couleur pour les statuts importants
- Calculs automatiques (pourcentages, heures, etc.)

### 🔗 Relations (Inlines)
- **QCM → Questions → Choix** : Gestion en cascade
- **Deck → Flashcards** : Gestion des flashcards dans le deck
- **Conversation → Messages** : Visualisation des messages

### ⚡ Performances
- Utilisation de `select_related` pour éviter les requêtes N+1
- Optimisation des listes avec des jointures pré-chargées
- Hiérarchie de dates pour navigation efficace

### 🛡️ Sécurité
- Champs en lecture seule pour les données générées automatiquement
- Validation des formulaires Django
- Permissions basées sur les groupes Django

---

## Actions Recommandées pour l'Administrateur

### Initialisation
1. Créer des **Matières** (Mathématiques, Français, Sciences, etc.)
2. Ajouter des **Chapitres** pour chaque matière
3. Remplir le **Dictionnaire** de traduction avec des mots courants
4. Créer des **Filières** et **Métiers** pour l'orientation

### Maintenance Quotidienne
1. Vérifier les **Performances** des élèves
2. Consulter les **Résultats QCM** pour identifier les difficultés
3. Surveiller les **Révisions Planifiées** non terminées
4. Vérifier les **Rappels** à envoyer

### Statistiques
1. Analyser les **Activités** pour comprendre l'utilisation
2. Consulter les **Conversations** pour améliorer le tuteur
3. Examiner les **Questionnaires d'orientation** pour adapter les suggestions

---

## Notes Importantes

- Les champs marqués "readonly" sont gérés automatiquement par l'application
- Les calculs (scores, pourcentages, etc.) sont effectués automatiquement
- Les dates sont toujours affichées avec la hiérarchie pour faciliter la navigation
- Les relations sont optimisées avec `select_related` pour de meilleures performances



