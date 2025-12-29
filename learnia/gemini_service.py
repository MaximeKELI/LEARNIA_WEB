"""
Service centralisé pour l'API Gemini
Gère toutes les interactions avec Google Gemini AI
"""
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    """Service centralisé pour utiliser l'API Gemini"""
    
    _initialized = False
    _model = None
    
    @classmethod
    def _initialize(cls):
        """Initialise la connexion à Gemini"""
        if cls._initialized:
            return
        
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            logger.warning("GEMINI_API_KEY non configurée dans settings.py")
            cls._initialized = True
            return
        
        try:
            genai.configure(api_key=api_key)
            # Essayer les modèles disponibles dans l'ordre de préférence
            model_names = [
                'gemini-2.5-flash',      # Plus récent, rapide et gratuit
                'gemini-2.0-flash',      # Alternative récente
                'gemini-1.5-flash',      # Ancien mais stable
                'gemini-1.5-pro',        # Plus performant mais peut être payant
            ]
            
            cls._model = None
            for model_name in model_names:
                try:
                    cls._model = genai.GenerativeModel(model_name)
                    logger.info(f"Gemini API initialisée avec le modèle: {model_name}")
                    break
                except Exception as e:
                    logger.debug(f"Modèle {model_name} non disponible: {e}")
                    continue
            
            if not cls._model:
                raise Exception("Aucun modèle Gemini disponible")
            
            cls._initialized = True
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de Gemini: {e}")
            cls._initialized = True  # Marquer comme initialisé pour éviter les tentatives répétées
    
    @classmethod
    def is_available(cls):
        """Vérifie si Gemini est disponible"""
        cls._initialize()
        return cls._model is not None
    
    @classmethod
    def generate_text(cls, prompt, system_instruction=None, temperature=0.7, max_tokens=None):
        """
        Génère du texte avec Gemini
        
        Args:
            prompt: Le prompt utilisateur
            system_instruction: Instruction système (optionnel)
            temperature: Contrôle la créativité (0.0-1.0)
            max_tokens: Nombre maximum de tokens (optionnel)
        
        Returns:
            str: Le texte généré, ou None en cas d'erreur
        """
        cls._initialize()
        
        if not cls._model:
            logger.warning("Gemini non disponible, fallback vers service local")
            return None
        
        try:
            generation_config = {
                'temperature': temperature,
            }
            if max_tokens:
                generation_config['max_output_tokens'] = max_tokens
            
            # Construire le prompt complet
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"
            
            response = cls._model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                logger.warning("Réponse Gemini vide")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération avec Gemini: {e}")
            return None
    
    @classmethod
    def generate_structured_response(cls, prompt, system_instruction=None, format_type="text"):
        """
        Génère une réponse structurée
        
        Args:
            prompt: Le prompt utilisateur
            system_instruction: Instruction système
            format_type: Type de format attendu (text, json, list, etc.)
        
        Returns:
            str: La réponse générée
        """
        if format_type == "json":
            system_instruction = (system_instruction or "") + "\n\nRéponds UNIQUEMENT en format JSON valide, sans markdown."
        elif format_type == "list":
            system_instruction = (system_instruction or "") + "\n\nRéponds sous forme de liste à puces, chaque élément sur une nouvelle ligne."
        
        return cls.generate_text(prompt, system_instruction)
    
    @classmethod
    def chat_response(cls, messages, system_instruction=None):
        """
        Génère une réponse dans un contexte de conversation
        
        Args:
            messages: Liste de messages [{"role": "user", "content": "..."}, ...]
            system_instruction: Instruction système
        
        Returns:
            str: La réponse générée
        """
        cls._initialize()
        
        if not cls._model:
            return None
        
        try:
            # Construire l'historique de conversation
            chat = cls._model.start_chat(history=[])
            
            # Ajouter l'instruction système si fournie
            if system_instruction:
                chat.send_message(system_instruction)
            
            # Envoyer le dernier message (les messages précédents sont dans l'historique)
            last_message = messages[-1] if messages else None
            if last_message and last_message.get("role") == "user":
                response = chat.send_message(last_message["content"])
                return response.text.strip() if response and response.text else None
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur lors du chat avec Gemini: {e}")
            return None

