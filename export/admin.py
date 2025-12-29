"""
Actions admin pour l'export de données
"""
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .services import CSVExporter, CSVImporter
from .pdf_services import PDFExporter

User = get_user_model()


@admin.action(description='Exporter les utilisateurs sélectionnés en CSV')
def export_selected_users_csv(modeladmin, request, queryset):
    """Action admin pour exporter les utilisateurs sélectionnés"""
    response = CSVExporter.export_users(queryset)
    return response
export_selected_users_csv.short_description = "Exporter en CSV"


@admin.action(description='Exporter les utilisateurs sélectionnés en PDF')
def export_selected_users_pdf(modeladmin, request, queryset):
    """Action admin pour exporter des rapports utilisateurs"""
    from io import BytesIO
    from datetime import datetime
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    
    buffer = BytesIO()
    
    with PdfPages(buffer) as pdf:
        for user in queryset:
            response = PDFExporter.export_user_report(user.id)
            if response:
                # Copier le contenu du PDF utilisateur dans le PDF global
                pass
    
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="users_report_{datetime.now().strftime("%Y%m%d")}.pdf"'
    return response
export_selected_users_pdf.short_description = "Exporter rapports PDF"


