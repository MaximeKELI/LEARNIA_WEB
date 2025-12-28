from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('', views.gamification_dashboard, name='dashboard'),
    path('badges/', views.badges_list, name='badges'),
]

