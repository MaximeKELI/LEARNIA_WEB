"""
Service OCR pour la reconnaissance de devoirs manuscrits
Mode hors ligne avec Tesseract
"""
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


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
    
    def analyze_homework(self, texte):
        """Analyse un devoir et donne une note (simulation)"""
        # Simulation d'analyse
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

