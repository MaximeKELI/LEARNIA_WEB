"""
Vues pour l'export et import de données
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .services import CSVExporter, CSVImporter
from .pdf_services import PDFExporter


@staff_member_required
def export_dashboard(request):
    """Tableau de bord pour l'export/import"""
    return render(request, 'export/dashboard.html')


@staff_member_required
@require_http_methods(["GET"])
def export_users_csv(request):
    """Export des utilisateurs en CSV"""
    try:
        response = CSVExporter.export_users()
        messages.success(request, 'Export des utilisateurs réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_statistics_csv(request):
    """Export des statistiques en CSV"""
    try:
        response = CSVExporter.export_statistics()
        messages.success(request, 'Export des statistiques réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_flashcards_csv(request):
    """Export des statistiques flashcards en CSV"""
    try:
        response = CSVExporter.export_flashcards_stats()
        messages.success(request, 'Export des flashcards réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_performances_csv(request):
    """Export des performances en CSV"""
    try:
        response = CSVExporter.export_performances()
        messages.success(request, 'Export des performances réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_activities_csv(request):
    """Export des activités en CSV"""
    try:
        response = CSVExporter.export_activities()
        messages.success(request, 'Export des activités réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_data_science_csv(request):
    """Export consolidé pour la data science en CSV"""
    try:
        response = CSVExporter.export_for_data_science()
        messages.success(request, 'Export data science réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_statistics_pdf(request):
    """Export des statistiques en PDF avec graphiques"""
    try:
        response = PDFExporter.export_statistics_pdf()
        messages.success(request, 'Export PDF réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_user_report_pdf(request, user_id):
    """Export d'un rapport utilisateur en PDF"""
    try:
        response = PDFExporter.export_user_report(user_id)
        if response:
            messages.success(request, 'Export PDF réussi.')
            return response
        else:
            messages.error(request, 'Utilisateur non trouvé.')
            return redirect('export:dashboard')
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["GET"])
def export_data_science_pdf(request):
    """Export du rapport data science en PDF"""
    try:
        response = PDFExporter.export_data_science_report()
        messages.success(request, 'Export PDF data science réussi.')
        return response
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'export: {str(e)}')
        return redirect('export:dashboard')


@staff_member_required
@require_http_methods(["POST"])
def import_users_csv(request):
    """Import des utilisateurs depuis un fichier CSV"""
    if 'csv_file' not in request.FILES:
        messages.error(request, 'Aucun fichier fourni.')
        return redirect('export:dashboard')
    
    try:
        csv_file = request.FILES['csv_file']
        imported, errors = CSVImporter.import_users(csv_file)
        
        if errors:
            messages.warning(request, 
                f'{imported} utilisateur(s) importé(s). {len(errors)} erreur(s).')
            for error in errors[:5]:  # Afficher max 5 erreurs
                messages.error(request, error)
        else:
            messages.success(request, f'{imported} utilisateur(s) importé(s) avec succès.')
        
        return redirect('export:dashboard')
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'import: {str(e)}')
        return redirect('export:dashboard')



