"""
Service de génération de résumé automatique
Mode hors ligne avec traitement local
"""
import re


class ResumeService:
    """Service pour générer des résumés"""
    
    def generate_resume(self, texte, longueur_max=200):
        """Génère un résumé du texte"""
        # Extraire les phrases
        phrases = re.split(r'[.!?]\s+', texte)
        phrases = [p.strip() for p in phrases if len(p.strip()) > 20]
        
        # Calculer l'importance des phrases (basé sur la longueur et les mots-clés)
        phrases_importantes = self._extraire_phrases_importantes(phrases)
        
        # Générer le résumé
        resume = ' '.join(phrases_importantes[:len(phrases_importantes)//2])
        
        # Limiter la longueur
        if len(resume) > longueur_max:
            resume = resume[:longueur_max] + "..."
        
        return resume
    
    def _extraire_phrases_importantes(self, phrases):
        """Extrait les phrases les plus importantes"""
        # Mots-clés éducatifs
        mots_cles = ['important', 'notion', 'concept', 'définition', 'exemple', 'caractéristique',
                     'propriété', 'règle', 'principe', 'formule', 'théorème']
        
        phrases_avec_score = []
        for phrase in phrases:
            score = len(phrase)  # Score de base = longueur
            
            # Bonus pour les mots-clés
            for mot_cle in mots_cles:
                if mot_cle.lower() in phrase.lower():
                    score += 50
            
            # Bonus pour les phrases au début (généralement plus importantes)
            position = phrases.index(phrase)
            score += (len(phrases) - position) * 10
            
            phrases_avec_score.append((phrase, score))
        
        # Trier par score
        phrases_avec_score.sort(key=lambda x: x[1], reverse=True)
        
        return [p[0] for p in phrases_avec_score]
    
    def extraire_points_cles(self, texte):
        """Extrait les points clés du texte"""
        phrases = re.split(r'[.!?]\s+', texte)
        phrases = [p.strip() for p in phrases if len(p.strip()) > 20]
        
        points = []
        for phrase in phrases[:10]:  # Limiter à 10 points
            # Chercher les phrases qui semblent être des points clés
            if any(mot in phrase.lower() for mot in ['est', 'sont', 'caractérisé', 'défini', 'notion']):
                points.append(phrase[:100])  # Limiter la longueur
        
        return points[:5]  # Retourner max 5 points


