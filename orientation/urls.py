from django.urls import path
from . import views

app_name = 'orientation'

urlpatterns = [
    path('', views.orientation_index, name='index'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('resultat/<int:questionnaire_id>/', views.resultat, name='resultat'),
    path('filieres/', views.filieres, name='filieres'),
    path('metiers/', views.metiers, name='metiers'),
]



