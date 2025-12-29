"""
Service de simulation IA pour le tuteur intelligent
Mode hors ligne avec réponses pré-générées
"""


class TuteurService:
    """Service pour générer des réponses du tuteur"""
    
    # Base de connaissances locale (simulation IA hors ligne)
    REPONSES_GENERIQUES = {
        'bonjour': "Bonjour ! Je suis ton tuteur intelligent. Comment puis-je t'aider aujourd'hui ?",
        'aide': "Je peux t'aider à comprendre tes cours, répondre à tes questions, et t'expliquer les concepts difficiles.",
        'maths': "Les mathématiques, c'est logique ! Pose-moi une question spécifique et je t'expliquerai étape par étape.",
        'francais': "Pour le français, je peux t'aider avec la grammaire, l'orthographe, et la compréhension de texte.",
        'science': "Les sciences, c'est passionnant ! Que veux-tu apprendre aujourd'hui ?",
    }
    
    def get_response(self, question, chapitre=None, user=None):
        """Génère une réponse adaptée à la question"""
        question_lower = question.lower().strip()
        
        # Recherche de mots-clés
        if any(mot in question_lower for mot in ['bonjour', 'salut', 'bonsoir']):
            return self.REPONSES_GENERIQUES['bonjour']
        
        if any(mot in question_lower for mot in ['aide', 'help', 'comment']):
            return self.REPONSES_GENERIQUES['aide']
        
        if any(mot in question_lower for mot in ['math', 'calcul', 'équation']):
            return self._generate_math_response(question)
        
        if any(mot in question_lower for mot in ['français', 'grammaire', 'orthographe']):
            return self._generate_french_response(question)
        
        if any(mot in question_lower for mot in ['science', 'physique', 'chimie', 'biologie']):
            return self._generate_science_response(question)
        
        # Réponse générique adaptée
        if chapitre:
            return f"Excellent question sur {chapitre.titre} ! Voici une explication simplifiée :\n\n{self._simulate_explanation(question, chapitre)}"
        
        return f"Merci pour ta question ! Voici ce que je peux te dire :\n\n{self._simulate_explanation(question)}"
    
    def _generate_math_response(self, question):
        """Génère une réponse pour les questions de mathématiques"""
        if 'équation' in question.lower():
            return """Pour résoudre une équation, voici les étapes :
1. Regroupe les termes avec x d'un côté et les nombres de l'autre
2. Simplifie chaque côté
3. Divise pour isoler x
4. Vérifie ta réponse en remplaçant x dans l'équation originale

Peux-tu me donner un exemple spécifique ?"""
        
        return """En mathématiques, la clé est de bien comprendre chaque étape :
- Lisez attentivement le problème
- Identifiez ce qu'on vous demande
- Notez les informations données
- Choisissez la méthode appropriée
- Vérifiez votre réponse

Que veux-tu apprendre exactement ?"""
    
    def _generate_french_response(self, question):
        """Génère une réponse pour les questions de français"""
        return """Pour améliorer ton français :
- Lis régulièrement des textes variés
- Note les mots nouveaux
- Pratique l'écriture quotidiennement
- Fais attention à la grammaire et à l'orthographe

Quelle partie du français te pose problème ?"""
    
    def _generate_science_response(self, question):
        """Génère une réponse pour les questions scientifiques"""
        return """Les sciences nécessitent de la curiosité et de la méthode :
- Observe attentivement les phénomènes
- Pose des questions
- Formule des hypothèses
- Expérimente et vérifie

Quel sujet scientifique t'intéresse ?"""
    
    def _simulate_explanation(self, question, chapitre=None):
        """Simule une explication détaillée"""
        base = "C'est une excellente question ! "
        
        if chapitre:
            base += f"Dans le chapitre '{chapitre.titre}', "
        
        base += """voici comment je peux t'expliquer :

1. **Concept de base** : Commençons par les fondamentaux
2. **Exemples concrets** : Regardons des exemples pratiques
3. **Application** : Voyons comment l'utiliser dans la vie quotidienne
4. **Pratique** : Essayons ensemble quelques exercices

As-tu une question plus précise sur ce sujet ?"""
        
        return base


