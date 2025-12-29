from django.urls import path
from . import views

app_name = 'ocr'

urlpatterns = [
    path('', views.ocr_index, name='index'),
    path('upload/', views.upload_devoir, name='upload'),
    path('<int:devoir_id>/', views.devoir_detail, name='devoir_detail'),
]


