"""
Service d'orientation scolaire
"""


class OrientationService:
    """Service pour l'orientation scolaire"""
    
    FILIERES = {
        'scientifique': {
            'nom': 'Série Scientifique (C)',
            'metiers': ['Ingénieur', 'Médecin', 'Pharmacien', 'Vétérinaire', 'Architecte'],
            'description': 'Pour ceux qui aiment les sciences et les mathématiques'
        },
        'litteraire': {
            'nom': 'Série Littéraire (A)',
            'metiers': ['Enseignant', 'Journaliste', 'Avocat', 'Traducteur', 'Écrivain'],
            'description': 'Pour ceux qui aiment les langues et la littérature'
        },
        'commercial': {
            'nom': 'Série Commerciale (G)',
            'metiers': ['Comptable', 'Commerçant', 'Banquier', 'Marketing', 'Management'],
            'description': 'Pour ceux qui aiment le commerce et la gestion'
        },
        'technique': {
            'nom': 'Série Technique',
            'metiers': ['Technicien', 'Mécanicien', 'Électricien', 'Informaticien'],
            'description': 'Pour ceux qui aiment le travail manuel et technique'
        }
    }
    
    def analyser_questionnaire(self, reponses):
        """Analyse les réponses et suggère une filière"""
        scores = {
            'scientifique': 0,
            'litteraire': 0,
            'commercial': 0,
            'technique': 0
        }
        
        # Logique d'analyse basique
        for question, reponse in reponses.items():
            if 'math' in question.lower() or 'science' in question.lower():
                if reponse in ['beaucoup', 'oui', '5', '4']:
                    scores['scientifique'] += 2
                    scores['technique'] += 1
            
            if 'litterature' in question.lower() or 'francais' in question.lower():
                if reponse in ['beaucoup', 'oui', '5', '4']:
                    scores['litteraire'] += 2
            
            if 'commerce' in question.lower() or 'gestion' in question.lower():
                if reponse in ['beaucoup', 'oui', '5', '4']:
                    scores['commercial'] += 2
            
            if 'manuel' in question.lower() or 'technique' in question.lower():
                if reponse in ['beaucoup', 'oui', '5', '4']:
                    scores['technique'] += 2
        
        # Trouver la filière avec le score le plus élevé
        filiere_dominante = max(scores, key=scores.get)
        
        return {
            'scores': scores,
            'filiere': self.FILIERES[filiere_dominante],
            'filiere_code': filiere_dominante
        }
    
    def suggerer_metiers(self, filiere_code):
        """Suggère des métiers pour une filière"""
        if filiere_code in self.FILIERES:
            return self.FILIERES[filiere_code]['metiers']
        return []

