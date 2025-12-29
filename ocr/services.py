"""
Service OCR pour la reconnaissance de devoirs manuscrits
Utilise Tesseract et Gemini AI pour l'analyse
"""
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

from learnia.gemini_service import GeminiService


class OCRService:
    """Service OCR pour la reconnaissance de texte"""
    
    def extract_text(self, image_path):
        """Extrait le texte d'une image"""
        if not OCR_AVAILABLE:
            return "OCR non disponible. Veuillez installer pytesseract et Pillow."
        
        try:
            image = Image.open(image_path)
            texte = pytesseract.image_to_string(image, lang='fra')
            return texte.strip()
        except Exception as e:
            return f"Erreur lors de l'extraction : {str(e)}"
    
    def correct_text(self, texte):
        """Corrige automatiquement le texte (simulation)"""
        # Simulation de correction - devrait utiliser un modèle de correction
        corrections = {
            'maths': 'mathématiques',
            'francais': 'français',
            'sience': 'science',
        }
        
        for erreur, correction in corrections.items():
            texte = texte.replace(erreur, correction)
        
        return texte
    
    def analyze_homework(self, texte, image_path=None, matiere=None):
        """Analyse un devoir et donne une note avec Gemini AI"""
        # Essayer d'abord avec Gemini si une image est fournie
        if image_path and GeminiService.is_available():
            analyse = self._analyze_with_gemini(image_path, matiere)
            if analyse:
                return analyse
        
        # Fallback vers l'analyse basique basée sur le texte
        return self._analyze_basic(texte)
    
    def _analyze_with_gemini(self, image_path, matiere=None):
        """Analyse un devoir avec Gemini AI en utilisant l'image"""
        system_instruction = """Tu es un professeur expérimenté qui corrige des devoirs d'élèves togolais.
        
Ton rôle est de :
- Analyser le devoir manuscrit dans l'image
- Identifier les réponses correctes et incorrectes
- Donner une note sur 20
- Fournir des commentaires constructifs et encourageants
- Adapter ton analyse au niveau scolaire (primaire à terminale)

Réponds en français, de manière pédagogique et bienveillante."""
        
        prompt = f"""Analyse ce devoir manuscrit et fournis :
1. Une note sur 20 (justifie ta notation)
2. Des commentaires détaillés sur :
   - Les points forts
   - Les erreurs identifiées
   - Des suggestions d'amélioration
   - Des encouragements

"""
        
        if matiere:
            prompt += f"Matière : {matiere}\n\n"
        
        prompt += "Format ta réponse ainsi :\nNOTE: [note]/20\n\nCOMMENTAIRES:\n[tes commentaires détaillés]"
        
        response = GeminiService.analyze_image(image_path, prompt, system_instruction)
        
        if not response:
            return None
        
            # Parser la réponse
        try:
            import re
            note = None
            commentaires = response
            
            # Extraire la note si présente (plusieurs formats possibles)
            note_patterns = [
                r'(?:NOTE|note|Note):\s*(\d+(?:\.\d+)?)\s*/?\s*20',
                r'(\d+(?:\.\d+)?)\s*/20',
                r'note\s*[:\-]?\s*(\d+(?:\.\d+)?)',
            ]
            
            for pattern in note_patterns:
                note_match = re.search(pattern, response, re.IGNORECASE)
                if note_match:
                    try:
                        note = int(float(note_match.group(1)))
                        break
                    except (ValueError, IndexError):
                        continue
            
            # Extraire les commentaires si format structuré
            commentaires_patterns = [
                r'COMMENTAIRES?:\s*(.+?)(?:\n\n|\Z)',
                r'Commentaires?:\s*(.+?)(?:\n\n|\Z)',
                r'ANALYSE:\s*(.+?)(?:\n\n|\Z)',
            ]
            
            for pattern in commentaires_patterns:
                commentaires_match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if commentaires_match:
                    commentaires = commentaires_match.group(1).strip()
                    break
            
            # Si pas de note trouvée, essayer de l'estimer depuis le texte
            if note is None:
                note = self._estimate_note_from_text(response)
            
            # Nettoyer les commentaires (enlever les préfixes de note si présents)
            if note is not None:
                commentaires = re.sub(r'(?:NOTE|note|Note):\s*\d+.*?\n', '', commentaires, flags=re.IGNORECASE)
            
            return {
                'note': max(0, min(20, note)),
                'commentaires': commentaires.strip()
            }
        except Exception as e:
            # En cas d'erreur de parsing, retourner la réponse brute avec note estimée
            note = self._estimate_note_from_text(response)
            return {
                'note': max(0, min(20, note)),
                'commentaires': response
            }
    
    def _estimate_note_from_text(self, texte):
        """Estime une note depuis le texte d'analyse"""
        texte_lower = texte.lower()
        score = 10  # Score de base
        
        # Mots-clés positifs
        if any(mot in texte_lower for mot in ['excellent', 'parfait', 'très bien', 'bravo']):
            score = 18
        elif any(mot in texte_lower for mot in ['bon', 'bien', 'correct', 'satisfaisant']):
            score = 14
        elif any(mot in texte_lower for mot in ['moyen', 'acceptable', 'passable']):
            score = 10
        elif any(mot in texte_lower for mot in ['faible', 'insuffisant', 'erreurs']):
            score = 6
        
        return score
    
    def _analyze_basic(self, texte):
        """Analyse basique basée sur le texte (fallback)"""
        mots_cles_positifs = ['bon', 'excellent', 'correct', 'bien', 'compris']
        mots_cles_negatifs = ['erreur', 'faux', 'incorrect', 'pas']
        
        score = 50  # Score de base
        
        texte_lower = texte.lower()
        for mot in mots_cles_positifs:
            if mot in texte_lower:
                score += 10
        
        for mot in mots_cles_negatifs:
            if mot in texte_lower:
                score -= 5
        
        # Limiter entre 0 et 20
        note = max(0, min(20, score))
        
        commentaires = []
        if note >= 16:
            commentaires.append("Excellent travail !")
        elif note >= 12:
            commentaires.append("Bon travail, continuez ainsi.")
        elif note >= 10:
            commentaires.append("Travail correct mais peut être amélioré.")
        else:
            commentaires.append("Des efforts sont nécessaires. Relisez le cours.")
        
        return {
            'note': round(note),
            'commentaires': ' '.join(commentaires)
        }



