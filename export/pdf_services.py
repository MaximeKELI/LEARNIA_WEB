"""
Services d'export PDF pour statistiques et graphiques
"""
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from accounts.models import Matiere
from qcm.models import ResultatQCM
from flashcards.models import Revision
from analytics.models import Performance
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

User = get_user_model()


class PDFExporter:
    """Service d'export PDF avec graphiques"""
    
    @staticmethod
    def export_statistics_pdf(queryset=None):
        """Export des statistiques en PDF avec graphiques"""
        if queryset is None:
            queryset = ResultatQCM.objects.all()
        
        buffer = BytesIO()
        
        with PdfPages(buffer) as pdf:
            # Page 1: Statistiques générales
            fig = plt.figure(figsize=(11, 8.5))
            fig.text(0.5, 0.95, 'Rapport Statistiques Learnia', 
                    ha='center', fontsize=16, fontweight='bold')
            fig.text(0.5, 0.92, f'Généré le {datetime.now().strftime("%d/%m/%Y %H:%M")}',
                    ha='center', fontsize=10)
            
            # Statistiques globales
            total_qcm = queryset.count()
            score_moyen = queryset.aggregate(avg_score=lambda x: sum(r.pourcentage for r in queryset) / len(queryset) if queryset else 0) if queryset else 0
            score_moyen_val = score_moyen.get('avg_score', 0) if score_moyen else 0
            
            stats_text = f"""
            STATISTIQUES GÉNÉRALES
            
            Total QCM complétés: {total_qcm}
            Score moyen: {score_moyen_val:.2f}%
            """
            
            fig.text(0.1, 0.8, stats_text, fontsize=12, 
                    verticalalignment='top', family='monospace')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 2: Graphique des scores par matière
            if queryset.exists():
                fig, ax = plt.subplots(figsize=(11, 8.5))
                
                # Group by matière
                matieres_scores = {}
                for resultat in queryset.select_related('qcm__chapitre__matiere'):
                    matiere = resultat.qcm.chapitre.matiere.nom if resultat.qcm.chapitre else 'Autre'
                    if matiere not in matieres_scores:
                        matieres_scores[matiere] = []
                    matieres_scores[matiere].append(resultat.pourcentage)
                
                if matieres_scores:
                    matieres = list(matieres_scores.keys())
                    moyennes = [np.mean(scores) for scores in matieres_scores.values()]
                    
                    bars = ax.bar(matieres, moyennes, color='steelblue')
                    ax.set_xlabel('Matière', fontsize=12)
                    ax.set_ylabel('Score moyen (%)', fontsize=12)
                    ax.set_title('Scores moyens par matière', fontsize=14, fontweight='bold')
                    ax.set_ylim(0, 100)
                    
                    # Ajouter les valeurs sur les barres
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.1f}%', ha='center', va='bottom')
                    
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close()
            
            # Page 3: Évolution dans le temps
            if queryset.exists():
                fig, ax = plt.subplots(figsize=(11, 8.5))
                
                # Grouper par date
                dates = []
                scores = []
                for resultat in queryset.order_by('created_at'):
                    dates.append(resultat.created_at.date())
                    scores.append(resultat.pourcentage)
                
                if dates:
                    ax.plot(dates, scores, marker='o', linestyle='-', color='green')
                    ax.set_xlabel('Date', fontsize=12)
                    ax.set_ylabel('Score (%)', fontsize=12)
                    ax.set_title('Évolution des scores dans le temps', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close()
        
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="statistics_{datetime.now().strftime("%Y%m%d")}.pdf"'
        return response
    
    @staticmethod
    def export_user_report(user_id):
        """Export d'un rapport personnalisé pour un utilisateur"""
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
        buffer = BytesIO()
        
        with PdfPages(buffer) as pdf:
            # Page 1: Profil utilisateur
            fig = plt.figure(figsize=(11, 8.5))
            fig.text(0.5, 0.95, f'Rapport Utilisateur: {user.username}',
                    ha='center', fontsize=16, fontweight='bold')
            
            profile_text = f"""
            INFORMATIONS PERSONNELLES
            
            Nom d'utilisateur: {user.username}
            Email: {user.email}
            Niveau d'étude: {user.niveau_etude}
            Classe: {user.classe or 'Non renseignée'}
            École: {user.ecole or 'Non renseignée'}
            Date d'inscription: {user.date_joined.strftime("%d/%m/%Y")}
            """
            
            fig.text(0.1, 0.7, profile_text, fontsize=12,
                    verticalalignment='top', family='monospace')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 2: Performances QCM
            resultats = ResultatQCM.objects.filter(user=user)
            if resultats.exists():
                fig, ax = plt.subplots(figsize=(11, 8.5))
                
                scores = [r.pourcentage for r in resultats]
                dates = [r.created_at.date() for r in resultats]
                
                ax.plot(dates, scores, marker='o', linestyle='-', color='blue')
                ax.axhline(y=np.mean(scores), color='r', linestyle='--', 
                          label=f'Moyenne: {np.mean(scores):.1f}%')
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('Score (%)', fontsize=12)
                ax.set_title('Performances QCM', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
            
            # Page 3: Statistiques flashcards
            revisions = Revision.objects.filter(user=user)
            if revisions.exists():
                fig, ax = plt.subplots(figsize=(11, 8.5))
                
                reussies = revisions.filter(reussie=True).count()
                echecs = revisions.count() - reussies
                
                labels = ['Réussies', 'Échecs']
                sizes = [reussies, echecs]
                colors = ['#2ecc71', '#e74c3c']
                
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax.set_title('Répartition des révisions flashcards', fontsize=14, fontweight='bold')
                
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
        
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="user_report_{user.username}_{datetime.now().strftime("%Y%m%d")}.pdf"'
        return response
    
    @staticmethod
    def export_data_science_report():
        """Export d'un rapport complet pour la data science"""
        buffer = BytesIO()
        
        with PdfPages(buffer) as pdf:
            # Page 1: Vue d'ensemble
            fig = plt.figure(figsize=(11, 8.5))
            fig.text(0.5, 0.95, 'Rapport Data Science - Learnia',
                    ha='center', fontsize=16, fontweight='bold')
            
            total_users = User.objects.count()
            total_qcm = ResultatQCM.objects.count()
            total_flashcards = Revision.objects.count()
            
            overview_text = f"""
            VUE D'ENSEMBLE
            
            Nombre d'utilisateurs: {total_users}
            Nombre de QCM complétés: {total_qcm}
            Nombre de révisions flashcards: {total_flashcards}
            Date du rapport: {datetime.now().strftime("%d/%m/%Y %H:%M")}
            """
            
            fig.text(0.1, 0.7, overview_text, fontsize=12,
                    verticalalignment='top', family='monospace')
            
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
            
            # Page 2: Distribution des niveaux d'étude
            fig, ax = plt.subplots(figsize=(11, 8.5))
            
            niveaux = User.objects.values_list('niveau_etude', flat=True)
            niveaux_counts = {}
            for niveau in niveaux:
                niveaux_counts[niveau] = niveaux_counts.get(niveau, 0) + 1
            
            if niveaux_counts:
                ax.bar(niveaux_counts.keys(), niveaux_counts.values(), color='steelblue')
                ax.set_xlabel('Niveau d\'étude', fontsize=12)
                ax.set_ylabel('Nombre d\'utilisateurs', fontsize=12)
                ax.set_title('Distribution des niveaux d\'étude', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                pdf.savefig(fig, bbox_inches='tight')
                plt.close()
        
        buffer.seek(0)
        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="data_science_report_{datetime.now().strftime("%Y%m%d")}.pdf"'
        return response

