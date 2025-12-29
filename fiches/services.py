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
    
    # Mapping des polices vers les polices standard de ReportLab
    FONT_MAPPING = {
        'Arial': 'Helvetica',
        'Helvetica': 'Helvetica',
        'Times': 'Times-Roman',
        'Times New Roman': 'Times-Roman',
        'Courier': 'Courier',
        'Courier New': 'Courier',
    }
    
    @staticmethod
    def _get_reportlab_font(font_name):
        """Convertit un nom de police en police ReportLab compatible"""
        if not font_name:
            return 'Helvetica'
        
        # Normaliser le nom de police
        font_name = font_name.strip()
        
        # Vérifier le mapping
        if font_name in FichePDFGenerator.FONT_MAPPING:
            return FichePDFGenerator.FONT_MAPPING[font_name]
        
        # Polices standard de ReportLab
        standard_fonts = ['Helvetica', 'Times-Roman', 'Courier', 'Symbol']
        if font_name in standard_fonts:
            return font_name
        
        # Par défaut, utiliser Helvetica (sans-serif, similaire à Arial)
        return 'Helvetica'
    
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
        
        # Obtenir la police compatible avec ReportLab
        reportlab_font = FichePDFGenerator._get_reportlab_font(fiche.police)
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor(fiche.couleur_titre),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=reportlab_font
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            fontName=reportlab_font
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            spaceAfter=12,
            fontName=reportlab_font,
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
        lines = fiche.contenu.split('\n')
        current_para = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_para:
                    para_text = ' '.join(current_para)
                    story.append(Paragraph(para_text, body_style))
                    story.append(Spacer(1, 0.1*inch))
                    current_para = []
                continue
            
            # Détecter les titres (lignes avec #)
            if line.startswith('##'):
                if current_para:
                    para_text = ' '.join(current_para)
                    story.append(Paragraph(para_text, body_style))
                    story.append(Spacer(1, 0.1*inch))
                    current_para = []
                title_text = line.lstrip('#').strip()
                story.append(Paragraph(f"<b>{title_text}</b>", heading_style))
                story.append(Spacer(1, 0.1*inch))
            elif line.startswith('#'):
                if current_para:
                    para_text = ' '.join(current_para)
                    story.append(Paragraph(para_text, body_style))
                    story.append(Spacer(1, 0.1*inch))
                    current_para = []
                title_text = line.lstrip('#').strip()
                story.append(Paragraph(f"<b>{title_text}</b>", heading_style))
                story.append(Spacer(1, 0.1*inch))
            else:
                # Convertir **bold** en HTML
                line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
                current_para.append(line)
        
        # Ajouter le dernier paragraphe
        if current_para:
            para_text = ' '.join(current_para)
            story.append(Paragraph(para_text, body_style))
        
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
            contenu=contenu,
            police='Helvetica',  # Police par défaut compatible ReportLab
            couleur_titre='#000000'  # Couleur par défaut
        )
        
        return FichePDFGenerator.generate_fiche(fiche)
    
    @staticmethod
    def generate_from_flashcards(deck, user):
        """Génère une fiche depuis un deck de flashcards"""
        titre = f"Fiche Flashcards - {deck.titre}"
        
        contenu = f"## {deck.titre}\n\n"
        contenu += "### Flashcards\n\n"
        
        for i, flashcard in enumerate(deck.flashcards.all(), 1):
            contenu += f"**{i}. {flashcard.recto}**\n\n"
            contenu += f"   → {flashcard.verso}\n\n"
        
        from .models import FicheRevision
        fiche = FicheRevision(
            user=user,
            titre=titre,
            chapitre=deck.chapitre,
            contenu=contenu,
            police='Helvetica',  # Police par défaut compatible ReportLab
            couleur_titre='#000000'  # Couleur par défaut
        )
        
        return FichePDFGenerator.generate_fiche(fiche)

