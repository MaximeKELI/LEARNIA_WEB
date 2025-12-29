from django.urls import path
from . import views

app_name = 'qcm'

urlpatterns = [
    path('', views.qcm_index, name='index'),
    path('generate/', views.generate_qcm, name='generate'),
    path('<int:qcm_id>/', views.qcm_detail, name='detail'),
    path('<int:qcm_id>/submit/', views.submit_qcm, name='submit'),
]



