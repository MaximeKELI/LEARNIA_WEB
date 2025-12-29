from django.urls import path
from . import views

app_name = 'export'

urlpatterns = [
    path('', views.export_dashboard, name='dashboard'),
    path('users/csv/', views.export_users_csv, name='export_users_csv'),
    path('statistics/csv/', views.export_statistics_csv, name='export_statistics_csv'),
    path('flashcards/csv/', views.export_flashcards_csv, name='export_flashcards_csv'),
    path('performances/csv/', views.export_performances_csv, name='export_performances_csv'),
    path('activities/csv/', views.export_activities_csv, name='export_activities_csv'),
    path('data-science/csv/', views.export_data_science_csv, name='export_data_science_csv'),
    path('statistics/pdf/', views.export_statistics_pdf, name='export_statistics_pdf'),
    path('user/<int:user_id>/pdf/', views.export_user_report_pdf, name='export_user_report_pdf'),
    path('data-science/pdf/', views.export_data_science_pdf, name='export_data_science_pdf'),
    path('users/import/', views.import_users_csv, name='import_users_csv'),
]


