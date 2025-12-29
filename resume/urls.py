from django.urls import path
from . import views

app_name = 'resume'

urlpatterns = [
    path('', views.resume_index, name='index'),
    path('generate/', views.generate_resume, name='generate'),
    path('<int:resume_id>/', views.resume_detail, name='detail'),
]



