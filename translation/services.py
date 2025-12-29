"""
Service de traduction en langues locales (éwé, kabiyè)
Mode hors ligne avec dictionnaire local
"""


class TranslationService:
    """Service de traduction"""
    
    # Dictionnaire basique pour simulation (devrait être dans la base de données)
    DICTIONNAIRE = {
        'bonjour': {'ewe': 'Woé zɔ', 'kab': 'Wobisiya'},
        'merci': {'ewe': 'Akpe na wò', 'kab': 'Alafiya'},
        'au revoir': {'ewe': 'Hede nyuie', 'kab': 'Wobisiya'},
        'comment': {'ewe': 'Akae', 'kab': 'Kpada'},
        'oui': {'ewe': 'Enyo', 'kab': 'Awo'},
        'non': {'ewe': 'Oo', 'kab': 'Aha'},
        'élève': {'ewe': 'Fofoa', 'kab': 'Kpɔkpɔkpɔ'},
        'maître': {'ewe': 'Kɔla', 'kab': 'Kpɔkpɔkpɔma'},
        'école': {'ewe': 'Suku', 'kab': 'Kpɔkpɔkpɔɣu'},
        'livre': {'ewe': 'Nu', 'kab': 'Suku'},
        'cours': {'ewe': 'Dɔwɔƒe', 'kab': 'Kpɔkpɔkpɔɣu'},
        'mathématiques': {'ewe': 'Xexeme', 'kab': 'Matematik'},
        'français': {'ewe': 'Franseto', 'kab': 'Franse'},
    }
    
    def translate(self, texte, langue_cible):
        """Traduit un texte"""
        texte_lower = texte.lower().strip()
        
        # Recherche directe dans le dictionnaire
        if texte_lower in self.DICTIONNAIRE:
            return self.DICTIONNAIRE[texte_lower].get(langue_cible, texte)
        
        # Traduction mot par mot
        mots = texte.split()
        mots_traduits = []
        
        for mot in mots:
            mot_clean = mot.lower().strip('.,!?;:')
            if mot_clean in self.DICTIONNAIRE:
                traduction = self.DICTIONNAIRE[mot_clean].get(langue_cible, mot)
                mots_traduits.append(traduction)
            else:
                mots_traduits.append(mot)
        
        return ' '.join(mots_traduits)
    
    def get_dictionary_entry(self, mot):
        """Récupère une entrée du dictionnaire"""
        mot_lower = mot.lower().strip()
        if mot_lower in self.DICTIONNAIRE:
            return self.DICTIONNAIRE[mot_lower]
        return None



