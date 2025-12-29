from django.urls import path
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.calendar_view, name='view'),
    path('create/', views.event_create, name='create'),
    path('<int:event_id>/edit/', views.event_edit, name='edit'),
    path('<int:event_id>/delete/', views.event_delete, name='delete'),
]



