from django.urls import path
from . import views

app_name = 'tutor'

urlpatterns = [
    path('', views.tutor_index, name='index'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('send-message/', views.send_message, name='send_message'),
    path('new/', views.new_conversation, name='new_conversation'),
]



