"""
Service de génération de fiches de révision PDF
"""
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class FichePDFGenerator:
    """Générateur de fiches PDF"""
    
    @staticmethod
    def generate_fiche(fiche):
        """Génère un PDF pour une fiche"""
        buffer = BytesIO()
        
        # Créer le document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(fiche.couleur_titre),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=fiche.police
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            fontName=fiche.police
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            spaceAfter=12,
            fontName=fiche.police,
            alignment=TA_LEFT
        )
        
        # Contenu
        story = []
        
        # Titre
        story.append(Paragraph(fiche.titre, title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Informations
        if fiche.chapitre:
            info_text = f"<b>Matière:</b> {fiche.chapitre.matiere.nom}<br/>"
            info_text += f"<b>Chapitre:</b> {fiche.chapitre.titre}<br/>"
            info_text += f"<b>Date:</b> {datetime.now().strftime('%d/%m/%Y')}"
            story.append(Paragraph(info_text, body_style))
            story.append(Spacer(1, 0.2*inch))
        
        # Ligne séparatrice
        story.append(Spacer(1, 0.1*inch))
        
        # Contenu de la fiche (convertir les sauts de ligne)
        contenu_paragraphes = fiche.contenu.split('\n\n')
        for para in contenu_paragraphes:
            if para.strip():
                # Détecter les titres (lignes avec #)
                if para.strip().startswith('#'):
                    title_text = para.strip().lstrip('#').strip()
                    story.append(Paragraph(title_text, heading_style))
                else:
                    # Convertir les sauts de ligne simples en <br/>
                    para_html = para.replace('\n', '<br/>')
                    story.append(Paragraph(para_html, body_style))
                story.append(Spacer(1, 0.1*inch))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    @staticmethod
    def generate_from_chapitre(chapitre, user, titre_custom=None):
        """Génère une fiche depuis un chapitre"""
        titre = titre_custom or f"Fiche - {chapitre.titre}"
        
        # Extraire le contenu structuré
        contenu = f"<b>{chapitre.titre}</b><br/><br/>"
        contenu += chapitre.contenu
        
        # Créer la fiche temporaire
        from .models import FicheRevision
        fiche = FicheRevision(
            user=user,
            titre=titre,
            chapitre=chapitre,
            contenu=contenu
        )
        
        return FichePDFGenerator.generate_fiche(fiche)
    
    @staticmethod
    def generate_from_flashcards(deck, user):
        """Génère une fiche depuis un deck de flashcards"""
        titre = f"Fiche Flashcards - {deck.titre}"
        
        contenu = f"<b>{deck.titre}</b><br/><br/>"
        contenu += "<b>Flashcards:</b><br/><br/>"
        
        for i, flashcard in enumerate(deck.flashcards.all(), 1):
            contenu += f"<b>{i}. {flashcard.recto}</b><br/>"
            contenu += f"   {flashcard.verso}<br/><br/>"
        
        from .models import FicheRevision
        fiche = FicheRevision(
            user=user,
            titre=titre,
            chapitre=deck.chapitre,
            contenu=contenu
        )
        
        return FichePDFGenerator.generate_fiche(fiche)

