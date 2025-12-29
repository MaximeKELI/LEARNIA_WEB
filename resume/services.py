"""
Service de génération de résumé automatique
Utilise Gemini AI avec fallback vers traitement local
"""
import re
from learnia.gemini_service import GeminiService


class ResumeService:
    """Service pour générer des résumés"""
    
    def generate_resume(self, texte, longueur_max=200):
        """Génère un résumé du texte avec Gemini AI"""
        # Essayer d'abord avec Gemini
        if GeminiService.is_available():
            resume = self._generate_with_gemini(texte, longueur_max)
            if resume:
                return resume
        
        # Fallback vers l'ancien système
        return self._generate_fallback(texte, longueur_max)
    
    def _generate_with_gemini(self, texte, longueur_max=200):
        """Génère un résumé avec Gemini AI"""
        system_instruction = """Tu es un assistant pédagogique qui génère des résumés de cours pour des élèves togolais.
        
Génère des résumés :
- Clairs et structurés
- Qui capturent les points essentiels
- Adaptés au niveau scolaire
- En français, avec un langage accessible"""
        
        prompt = f"""Résume le texte suivant en maximum {longueur_max} mots, en capturant les points essentiels et les concepts clés.

TEXTE :
{texte[:3000]}  # Limiter la longueur

Génère un résumé concis et pédagogique."""
        
        response = GeminiService.generate_text(
            prompt=prompt,
            system_instruction=system_instruction,
            temperature=0.3,  # Température plus basse pour des résumés plus factuels
            max_tokens=longueur_max * 2  # Approximativement 2 tokens par mot
        )
        
        if response:
            # Limiter la longueur si nécessaire
            if len(response) > longueur_max:
                # Couper à la dernière phrase complète avant la limite
                words = response[:longueur_max].split()
                response = ' '.join(words)
                if not response.endswith(('.', '!', '?')):
                    response += "..."
            return response
        
        return None
    
    def _generate_fallback(self, texte, longueur_max=200):
        """Génère un résumé avec le système de fallback (ancien système)"""
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
        """Extrait les points clés du texte avec Gemini AI"""
        # Essayer d'abord avec Gemini
        if GeminiService.is_available():
            points = self._extraire_points_avec_gemini(texte)
            if points:
                return points
        
        # Fallback vers l'ancien système
        return self._extraire_points_fallback(texte)
    
    def _extraire_points_avec_gemini(self, texte):
        """Extrait les points clés avec Gemini AI"""
        system_instruction = """Tu es un assistant pédagogique qui extrait les points clés d'un texte de cours.
        
Extrais les 5 points les plus importants et présente-les sous forme de liste à puces."""
        
        prompt = f"""Extrais les 5 points clés les plus importants du texte suivant.

TEXTE :
{texte[:2000]}

Réponds sous forme de liste à puces, chaque point sur une nouvelle ligne commençant par "-"."""
        
        response = GeminiService.generate_structured_response(
            prompt=prompt,
            system_instruction=system_instruction,
            format_type="list"
        )
        
        if response:
            # Parser la liste à puces
            points = []
            for line in response.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    point = line.lstrip('-•*').strip()
                    if point and len(point) <= 150:  # Limiter la longueur
                        points.append(point)
                elif line and len(line) <= 150:
                    points.append(line)
            
            return points[:5] if points else None
        
        return None
    
    def _extraire_points_fallback(self, texte):
        """Extrait les points clés avec le système de fallback (ancien système)"""
        phrases = re.split(r'[.!?]\s+', texte)
        phrases = [p.strip() for p in phrases if len(p.strip()) > 20]
        
        points = []
        for phrase in phrases[:10]:  # Limiter à 10 points
            # Chercher les phrases qui semblent être des points clés
            if any(mot in phrase.lower() for mot in ['est', 'sont', 'caractérisé', 'défini', 'notion']):
                points.append(phrase[:100])  # Limiter la longueur
        
        return points[:5]  # Retourner max 5 points


