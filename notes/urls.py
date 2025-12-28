from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.notes_list, name='list'),
    path('create/', views.note_create, name='create'),
    path('<int:note_id>/', views.note_detail, name='detail'),
    path('<int:note_id>/edit/', views.note_edit, name='edit'),
    path('<int:note_id>/delete/', views.note_delete, name='delete'),
    path('<int:note_id>/favorite/', views.note_toggle_favorite, name='toggle_favorite'),
]

