from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.planner_index, name='index'),
    path('examen/create/', views.create_examen, name='create_examen'),
    path('revision/create/', views.create_revision, name='create_revision'),
    path('revision/<int:revision_id>/done/', views.mark_revision_done, name='mark_revision_done'),
    path('generate/', views.generate_plan, name='generate_plan'),
]



