from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['created_at']
    fields = ['role', 'contenu_court', 'created_at']
    
    def contenu_court(self, obj):
        return obj.contenu[:100] + '...' if len(obj.contenu) > 100 else obj.contenu
    contenu_court.short_description = 'Contenu'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'nombre_messages', 'created_at', 'updated_at']
    list_filter = ['created_at', 'chapitre__matiere']
    search_fields = ['titre', 'user__username', 'chapitre__titre']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [MessageInline]
    list_select_related = ['user', 'chapitre']
    
    def nombre_messages(self, obj):
        return obj.messages.count()
    nombre_messages.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'role', 'contenu_court', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['contenu', 'conversation__titre']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_select_related = ['conversation', 'conversation__user']
    
    def contenu_court(self, obj):
        return obj.contenu[:100] + '...' if len(obj.contenu) > 100 else obj.contenu
    contenu_court.short_description = 'Contenu'

