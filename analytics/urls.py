from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_index, name='index'),
    path('matiere/<int:matiere_id>/', views.performance_detail, name='performance_detail'),
]


