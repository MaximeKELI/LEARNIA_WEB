# Guide d'Export/Import de Données - Learnia

Ce guide explique comment utiliser les fonctionnalités d'export et d'import de données pour la data science.

## 🚀 Accès

L'interface d'export/import est accessible uniquement aux administrateurs :
- URL : `/export/`
- Ou via le menu admin

## 📊 Exports Disponibles

### Export CSV

#### 1. Utilisateurs
**URL**: `/export/users/csv/`

**Contenu**:
- ID, Username, Email, Prénom, Nom
- Niveau d'étude, Classe, École
- Date de naissance, Date d'inscription, Dernière connexion
- Statut actif

**Utilisation**:
```python
import pandas as pd
df = pd.read_csv('users_20240101.csv')
```

#### 2. Statistiques QCM
**URL**: `/export/statistics/csv/`

**Contenu**:
- ID, Utilisateur, QCM, Matière
- Score, Total, Pourcentage
- Date

**Utilisation**:
```python
df = pd.read_csv('statistics_20240101.csv')
# Analyse des performances
df.groupby('Matière')['Pourcentage'].mean()
```

#### 3. Statistiques Flashcards
**URL**: `/export/flashcards/csv/`

**Contenu**:
- ID, Utilisateur, Deck, Question, Réponse
- Réussie (Oui/Non), Temps en secondes
- Date

**Utilisation**:
```python
df = pd.read_csv('flashcards_stats_20240101.csv')
# Taux de réussite
df['Réussie'].value_counts()
```

#### 4. Performances
**URL**: `/export/performances/csv/`

**Contenu**:
- ID, Utilisateur, Matière
- Score moyen, Nombre QCM, Nombre flashcards
- Temps d'étude (minutes), Dernière mise à jour

#### 5. Activités
**URL**: `/export/activities/csv/`

**Contenu**:
- ID, Utilisateur, Type, Description
- Durée (minutes), Date

#### 6. Data Science (Consolidé)
**URL**: `/export/data-science/csv/`

**Contenu consolidé** optimisé pour analyses :
- Données agrégées par utilisateur et matière
- Scores QCM, statistiques flashcards
- Temps d'étude, nombre d'activités
- Format idéal pour machine learning

**Exemple d'analyse**:
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Charger les données
df = pd.read_csv('learnia_data_science_20240101.csv')

# Préparer les données
X = df[['score_qcm', 'flashcards_reussies', 'temps_etude_minutes']]
y = df['pourcentage_qcm']

# Modèle de prédiction
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Prédictions
predictions = model.predict(X_test)
```

### Export PDF

#### 1. Statistiques PDF
**URL**: `/export/statistics/pdf/`

**Contenu**:
- Vue d'ensemble des statistiques
- Graphique des scores par matière (barres)
- Graphique d'évolution temporelle (ligne)
- Pages multiples avec visualisations

#### 2. Rapport Utilisateur PDF
**URL**: `/export/user/<user_id>/pdf/`

**Contenu**:
- Profil utilisateur
- Graphique des performances QCM
- Graphique des révisions flashcards (camembert)
- Rapport personnalisé

#### 3. Rapport Data Science PDF
**URL**: `/export/data-science/pdf/`

**Contenu**:
- Vue d'ensemble complète
- Distribution des niveaux d'étude
- Autres visualisations statistiques

## 📥 Import CSV

### Import Utilisateurs
**URL**: `/export/users/import/` (POST)

**Format CSV attendu**:
```csv
Username,Email,Prénom,Nom,Niveau d'étude,Classe,École
john,john@example.com,John,Doe,6e,6ème A,École Test
jane,jane@example.com,Jane,Smith,5e,5ème B,École Primaire
```

**Champs requis**:
- Username
- Email

**Champs optionnels**:
- Prénom, Nom
- Niveau d'étude (défaut: 6e)
- Classe, École

**Comportement**:
- Si l'utilisateur existe (même username), il est mis à jour
- Si l'utilisateur n'existe pas, il est créé
- Les erreurs sont affichées dans les messages

## 🔬 Utilisation pour Data Science

### Python avec Pandas

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv('learnia_data_science_20240101.csv')

# Analyse exploratoire
print(df.describe())
print(df.info())

# Visualisations
sns.pairplot(df[['score_qcm', 'pourcentage_qcm', 'temps_etude_minutes']])
plt.show()

# Corrélations
correlation_matrix = df[['score_qcm', 'flashcards_reussies', 
                        'temps_etude_minutes', 'pourcentage_qcm']].corr()
sns.heatmap(correlation_matrix, annot=True)
plt.show()
```

### R

```r
# Charger les données
df <- read.csv("learnia_data_science_20240101.csv")

# Analyse
summary(df)
str(df)

# Visualisations
library(ggplot2)
ggplot(df, aes(x = score_qcm, y = pourcentage_qcm)) +
  geom_point() +
  geom_smooth(method = "lm")

# Modèle
model <- lm(pourcentage_qcm ~ score_qcm + flashcards_reussies + temps_etude_minutes, data = df)
summary(model)
```

### Excel / LibreOffice

1. Ouvrir le fichier CSV
2. Utiliser les fonctions de tableau croisé dynamique
3. Créer des graphiques avec les données

### Tableau / Power BI

1. Importer le fichier CSV
2. Créer des visualisations interactives
3. Construire des dashboards

## 📈 Exemples d'Analyses

### 1. Prédiction de Performance
```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X_train, y_train)
importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
```

### 2. Segmentation des Utilisateurs
```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(X)
df['cluster'] = clusters
```

### 3. Analyse de Corrélation
```python
correlations = df.corr()
# Identifier les facteurs qui influencent le plus les performances
```

## 🔒 Sécurité

- Accès réservé aux administrateurs (`@staff_member_required`)
- Validation des fichiers d'import
- Encodage UTF-8 pour les caractères spéciaux
- Protection contre les injections

## 📝 Format des Dates

- CSV : `YYYY-MM-DD HH:MM:SS` (format ISO)
- Compatible avec pandas `pd.to_datetime()`

## 🐛 Dépannage

### Erreur d'encodage
Les fichiers CSV utilisent l'encodage UTF-8 avec BOM pour Excel.

### Fichier PDF vide
Vérifier que matplotlib est correctement installé :
```bash
pip install matplotlib
```

### Import échoue
- Vérifier le format CSV
- S'assurer que Username et Email sont présents
- Vérifier les logs Django pour plus de détails

## 📚 Ressources

- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)



