"""
Service de génération de QCM à partir d'un texte
Utilise Gemini AI avec fallback vers génération locale
"""
import re
import random
import json
from learnia.gemini_service import GeminiService


class QCMGenerator:
    """Générateur de QCM à partir d'un texte"""
    
    def generate_questions(self, texte, nombre_questions=5):
        """Génère des questions à partir d'un texte avec Gemini AI"""
        # Essayer d'abord avec Gemini
        if GeminiService.is_available():
            questions = self._generate_with_gemini(texte, nombre_questions)
            if questions:
                return questions
        
        # Fallback vers l'ancien système
        return self._generate_fallback(texte, nombre_questions)
    
    def _generate_with_gemini(self, texte, nombre_questions=5):
        """Génère des questions avec Gemini AI"""
        system_instruction = """Tu es un générateur de questions pédagogiques pour des élèves togolais.
        
Génère des questions de qualité adaptées au niveau scolaire, avec :
- Des questions claires et précises
- Des choix de réponses variés et pertinents
- Une seule bonne réponse par question
- Des distracteurs réalistes (mauvaises réponses plausibles)

Format de réponse : JSON avec une liste de questions, chaque question ayant :
- "texte" : le texte de la question
- "choix" : liste de choix, chaque choix ayant "texte" et "correct" (true/false)"""
        
        prompt = f"""À partir du texte suivant, génère exactement {nombre_questions} questions à choix multiple (QCM) de qualité pédagogique.

TEXTE :
{texte[:2000]}  # Limiter la longueur pour éviter les tokens excessifs

Génère les questions en format JSON. Chaque question doit avoir :
- "numero" : numéro de la question (1, 2, 3...)
- "texte" : le texte de la question
- "choix" : liste de 4 choix, avec exactement UN choix ayant "correct": true

Réponds UNIQUEMENT en JSON valide, sans texte supplémentaire."""
        
        response = GeminiService.generate_structured_response(
            prompt=prompt,
            system_instruction=system_instruction,
            format_type="json"
        )
        
        if not response:
            return None
        
        try:
            # Nettoyer la réponse (enlever markdown si présent)
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            if response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            # Parser le JSON
            data = json.loads(response_clean)
            
            # Vérifier le format
            if isinstance(data, dict) and 'questions' in data:
                questions = data['questions']
            elif isinstance(data, list):
                questions = data
            else:
                return None
            
            # Valider et formater les questions
            formatted_questions = []
            for i, q in enumerate(questions[:nombre_questions], 1):
                if 'texte' in q and 'choix' in q:
                    formatted_q = {
                        'numero': q.get('numero', i),
                        'texte': q['texte'],
                        'choix': []
                    }
                    
                    # Formater les choix
                    for choix in q['choix']:
                        if isinstance(choix, dict) and 'texte' in choix:
                            formatted_q['choix'].append({
                                'texte': choix['texte'],
                                'correct': choix.get('correct', False)
                            })
                    
                    # Vérifier qu'il y a au moins 2 choix et une bonne réponse
                    if len(formatted_q['choix']) >= 2 and any(c['correct'] for c in formatted_q['choix']):
                        formatted_questions.append(formatted_q)
            
            return formatted_questions if formatted_questions else None
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            # En cas d'erreur de parsing, retourner None pour utiliser le fallback
            return None
    
    def _generate_fallback(self, texte, nombre_questions=5):
        """Génère des questions avec le système de fallback (ancien système)"""
        questions = []
        
        # Extraire les phrases importantes
        phrases = self._extract_key_phrases(texte)
        
        # Générer des questions
        for i in range(min(nombre_questions, len(phrases))):
            if i < len(phrases):
                question_data = self._create_question(phrases[i], texte, i + 1)
                questions.append(question_data)
        
        return questions
    
    def _extract_key_phrases(self, texte):
        """Extrait les phrases clés du texte"""
        # Diviser en phrases
        phrases = re.split(r'[.!?]\s+', texte)
        
        # Filtrer les phrases significatives (plus de 20 caractères)
        phrases_importantes = [p.strip() for p in phrases if len(p.strip()) > 20]
        
        return phrases_importantes[:10]  # Limiter à 10 phrases
    
    def _create_question(self, phrase, texte_complet, numero):
        """Crée une question à partir d'une phrase"""
        # Types de questions possibles
        question_types = [
            'completion',
            'choix_multiple',
            'vrai_faux',
        ]
        
        type_question = random.choice(question_types)
        
        if type_question == 'vrai_faux':
            return self._create_true_false(phrase, numero)
        elif type_question == 'completion':
            return self._create_completion(phrase, numero)
        else:
            return self._create_multiple_choice(phrase, texte_complet, numero)
    
    def _create_true_false(self, phrase, numero):
        """Crée une question vrai/faux"""
        # Choisir aléatoirement vrai ou faux
        est_vrai = random.choice([True, False])
        
        if est_vrai:
            question_texte = phrase
            choix = [
                {'texte': 'Vrai', 'correct': True},
                {'texte': 'Faux', 'correct': False},
            ]
        else:
            # Modifier légèrement la phrase pour la rendre fausse
            question_texte = phrase.replace('est', 'n\'est pas').replace('sont', 'ne sont pas')
            choix = [
                {'texte': 'Vrai', 'correct': False},
                {'texte': 'Faux', 'correct': True},
            ]
        
        return {
            'numero': numero,
            'texte': f"D'après le texte, cette affirmation est-elle correcte : \"{question_texte}\" ?",
            'choix': choix
        }
    
    def _create_completion(self, phrase, numero):
        """Crée une question à trous"""
        mots = phrase.split()
        if len(mots) > 3:
            mot_a_cacher = random.choice(mots[1:-1])  # Ne pas prendre le premier ni le dernier
            phrase_completee = phrase.replace(mot_a_cacher, '______')
            
            # Créer des choix
            choix_correct = {'texte': mot_a_cacher, 'correct': True}
            choix_faux = [
                {'texte': word, 'correct': False}
                for word in mots[:5] if word != mot_a_cacher
            ][:3]
            
            choix = [choix_correct] + choix_faux
            random.shuffle(choix)
            
            return {
                'numero': numero,
                'texte': f"Complétez : {phrase_completee}",
                'choix': choix
            }
        
        return self._create_multiple_choice(phrase, "", numero)
    
    def _create_multiple_choice(self, phrase, texte_complet, numero):
        """Crée une question à choix multiple"""
        # Extraire un concept clé de la phrase
        mots_cles = [m for m in phrase.split() if len(m) > 4]
        if not mots_cles:
            mots_cles = phrase.split()[:3]
        
        concept = mots_cles[0] if mots_cles else "concept"
        
        # Créer la question
        question_texte = f"Quelle affirmation concernant \"{concept}\" est correcte selon le texte ?"
        
        # Générer des choix
        choix_correct = {'texte': phrase[:100], 'correct': True}
        
        # Générer des choix incorrects à partir d'autres parties du texte
        autres_phrases = [p for p in texte_complet.split('.') if p != phrase][:3]
        choix_faux = [
            {'texte': p[:100], 'correct': False}
            for p in autres_phrases if len(p.strip()) > 20
        ]
        
        # Si pas assez de choix, en créer des génériques
        while len(choix_faux) < 3:
            choix_faux.append({
                'texte': f"Une autre affirmation sur {concept}",
                'correct': False
            })
        
        choix = [choix_correct] + choix_faux[:3]
        random.shuffle(choix)
        
        return {
            'numero': numero,
            'texte': question_texte,
            'choix': choix
        }


