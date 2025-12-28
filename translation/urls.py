from django.urls import path
from . import views

app_name = 'translation'

urlpatterns = [
    path('', views.translation_index, name='index'),
    path('translate/', views.translate_text, name='translate'),
    path('dictionary/', views.dictionary, name='dictionary'),
]

