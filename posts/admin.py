from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'type_post', 'publique', 'prioritaire', 'date_publication', 'is_active']
    list_filter = ['type_post', 'publique', 'prioritaire', 'date_publication']
    search_fields = ['titre', 'contenu', 'auteur__username']
    date_hierarchy = 'date_publication'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('titre', 'contenu', 'type_post', 'image')
        }),
        ('Paramètres', {
            'fields': ('auteur', 'publique', 'prioritaire')
        }),
        ('Dates', {
            'fields': ('date_publication', 'date_expiration')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(auteur=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nouveau post
            obj.auteur = request.user
        super().save_model(request, obj, form, change)


