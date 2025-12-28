from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'created_at']
    list_filter = ['created_at']
    search_fields = ['titre', 'user__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['contenu']

