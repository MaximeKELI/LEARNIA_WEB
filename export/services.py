"""
Services d'export et import de données
Support CSV et PDF pour la data science
"""
import csv
import io
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from accounts.models import Matiere, Chapitre
from qcm.models import QCM, ResultatQCM
from flashcards.models import Deck, Flashcard, Revision
from tutor.models import Conversation, Message
from analytics.models import Performance, Activite
import json

User = get_user_model()


class CSVExporter:
    """Service d'export CSV"""
    
    @staticmethod
    def export_users(queryset=None):
        """Export des utilisateurs en CSV"""
        if queryset is None:
            queryset = User.objects.all()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="users_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        # En-têtes
        writer.writerow([
            'ID', 'Username', 'Email', 'Prénom', 'Nom',
            'Niveau d\'étude', 'Classe', 'École', 'Date de naissance',
            'Date d\'inscription', 'Dernière connexion', 'Actif'
        ])
        
        # Données
        for user in queryset:
            writer.writerow([
                user.id,
                user.username,
                user.email,
                user.first_name or '',
                user.last_name or '',
                user.niveau_etude,
                user.classe or '',
                user.ecole or '',
                user.date_naissance.strftime('%Y-%m-%d') if user.date_naissance else '',
                user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
                user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
                'Oui' if user.is_active else 'Non'
            ])
        
        return response
    
    @staticmethod
    def export_statistics(queryset=None):
        """Export des statistiques en CSV"""
        if queryset is None:
            queryset = ResultatQCM.objects.all()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="statistics_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        # En-têtes
        writer.writerow([
            'ID', 'Utilisateur', 'QCM', 'Matière', 'Score', 'Total',
            'Pourcentage', 'Date'
        ])
        
        for resultat in queryset.select_related('user', 'qcm', 'qcm__chapitre__matiere'):
            matiere = resultat.qcm.chapitre.matiere.nom if resultat.qcm.chapitre else 'N/A'
            writer.writerow([
                resultat.id,
                resultat.user.username,
                resultat.qcm.titre,
                matiere,
                resultat.score,
                resultat.total,
                f"{resultat.pourcentage:.2f}%",
                resultat.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    @staticmethod
    def export_flashcards_stats(queryset=None):
        """Export des statistiques de flashcards en CSV"""
        if queryset is None:
            queryset = Revision.objects.all()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="flashcards_stats_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Utilisateur', 'Deck', 'Question', 'Réponse',
            'Réussie', 'Temps (secondes)', 'Date'
        ])
        
        for revision in queryset.select_related('user', 'flashcard', 'flashcard__deck'):
            writer.writerow([
                revision.id,
                revision.user.username,
                revision.flashcard.deck.titre,
                revision.flashcard.recto[:50],
                revision.flashcard.verso[:50],
                'Oui' if revision.reussie else 'Non',
                revision.temps_reponse,
                revision.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    @staticmethod
    def export_performances(queryset=None):
        """Export des performances en CSV"""
        if queryset is None:
            queryset = Performance.objects.all()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="performances_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Utilisateur', 'Matière', 'Score moyen',
            'Nombre QCM', 'Nombre flashcards', 'Temps étude (minutes)',
            'Dernière mise à jour'
        ])
        
        for perf in queryset.select_related('user', 'matiere'):
            writer.writerow([
                perf.id,
                perf.user.username,
                perf.matiere.nom,
                f"{perf.score_moyen:.2f}",
                perf.nombre_qcm,
                perf.nombre_flashcards,
                perf.temps_etude_minutes,
                perf.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    @staticmethod
    def export_activities(queryset=None):
        """Export des activités en CSV"""
        if queryset is None:
            queryset = Activite.objects.all()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="activities_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Utilisateur', 'Type', 'Description',
            'Durée (minutes)', 'Date'
        ])
        
        for activity in queryset.select_related('user'):
            writer.writerow([
                activity.id,
                activity.user.username,
                activity.type_activite,
                activity.description,
                activity.duree_minutes,
                activity.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    @staticmethod
    def export_for_data_science():
        """Export consolidé pour la data science"""
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="learnia_data_science_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'user_id', 'username', 'niveau_etude', 'matiere', 'score_qcm',
            'total_qcm', 'pourcentage_qcm', 'flashcards_reussies',
            'flashcards_total', 'temps_etude_minutes', 'nombre_activites',
            'date_inscription', 'derniere_connexion'
        ])
        
        # Agrégation des données par utilisateur
        for user in User.objects.all():
            # Stats QCM
            resultats_qcm = ResultatQCM.objects.filter(user=user)
            score_total = sum(r.score for r in resultats_qcm)
            total_qcm = sum(r.total for r in resultats_qcm)
            pourcentage_moyen = (score_total / total_qcm * 100) if total_qcm > 0 else 0
            
            # Stats Flashcards
            revisions = Revision.objects.filter(user=user)
            flashcards_reussies = revisions.filter(reussie=True).count()
            flashcards_total = revisions.count()
            
            # Stats activités
            activites = Activite.objects.filter(user=user)
            temps_total = sum(a.duree_minutes for a in activites)
            nombre_activites = activites.count()
            
            # Par matière
            for matiere in Matiere.objects.all():
                resultats_matiere = resultats_qcm.filter(
                    qcm__chapitre__matiere=matiere
                )
                if resultats_matiere.exists():
                    score_matiere = sum(r.score for r in resultats_matiere)
                    total_matiere = sum(r.total for r in resultats_matiere)
                    pourcentage_matiere = (score_matiere / total_matiere * 100) if total_matiere > 0 else 0
                    
                    writer.writerow([
                        user.id,
                        user.username,
                        user.niveau_etude,
                        matiere.nom,
                        score_matiere,
                        total_matiere,
                        f"{pourcentage_matiere:.2f}",
                        flashcards_reussies,
                        flashcards_total,
                        temps_total,
                        nombre_activites,
                        user.date_joined.strftime('%Y-%m-%d'),
                        user.last_login.strftime('%Y-%m-%d') if user.last_login else ''
                    ])
        
        return response


class CSVImporter:
    """Service d'import CSV"""
    
    @staticmethod
    def import_users(csv_file):
        """Import des utilisateurs depuis un fichier CSV"""
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        
        imported = 0
        errors = []
        
        for row in reader:
            try:
                username = row.get('Username') or row.get('username')
                email = row.get('Email') or row.get('email')
                
                if not username or not email:
                    errors.append(f"Ligne {reader.line_num}: Username et Email requis")
                    continue
                
                # Créer ou mettre à jour l'utilisateur
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'first_name': row.get('Prénom', '') or row.get('first_name', ''),
                        'last_name': row.get('Nom', '') or row.get('last_name', ''),
                        'niveau_etude': row.get('Niveau d\'étude', '6e') or row.get('niveau_etude', '6e'),
                        'classe': row.get('Classe', '') or row.get('classe', ''),
                        'ecole': row.get('École', '') or row.get('ecole', ''),
                    }
                )
                
                if not created:
                    # Mettre à jour les champs
                    user.email = email
                    user.first_name = row.get('Prénom', '') or row.get('first_name', '')
                    user.last_name = row.get('Nom', '') or row.get('last_name', '')
                    user.niveau_etude = row.get('Niveau d\'étude', user.niveau_etude) or row.get('niveau_etude', user.niveau_etude)
                    user.classe = row.get('Classe', user.classe) or row.get('classe', user.classe)
                    user.ecole = row.get('École', user.ecole) or row.get('ecole', user.ecole)
                    user.save()
                
                imported += 1
                
            except Exception as e:
                errors.append(f"Ligne {reader.line_num}: {str(e)}")
        
        return imported, errors

