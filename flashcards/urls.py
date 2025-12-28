from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcards_index, name='index'),
    path('create/', views.create_deck, name='create_deck'),
    path('<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('<int:deck_id>/add/', views.add_flashcard, name='add_flashcard'),
    path('<int:deck_id>/review/', views.review_deck, name='review_deck'),
    path('flashcard/<int:flashcard_id>/mark/', views.mark_revision, name='mark_revision'),
]

