from django.urls import path
from . import views

app_name = 'fiches'

urlpatterns = [
    path('', views.fiches_list, name='list'),
    path('create/', views.fiche_create, name='create'),
    path('from-chapitre/<int:chapitre_id>/', views.fiche_from_chapitre, name='from_chapitre'),
    path('from-deck/<int:deck_id>/', views.fiche_from_deck, name='from_deck'),
    path('<int:fiche_id>/download/', views.fiche_download, name='download'),
    path('<int:fiche_id>/delete/', views.fiche_delete, name='delete'),
]

