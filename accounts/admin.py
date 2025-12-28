from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Matiere, Chapitre


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'niveau_etude', 'classe', 'ecole', 'date_joined', 'is_staff']
    list_filter = ['niveau_etude', 'date_joined', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'classe', 'ecole']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Learnia', {
            'fields': ('niveau_etude', 'classe', 'ecole', 'date_naissance', 'avatar')
        }),
    )
    readonly_fields = ['date_joined', 'last_login']
    date_hierarchy = 'date_joined'


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'niveau', 'icone', 'nombre_chapitres']
    list_filter = ['niveau']
    search_fields = ['nom', 'code', 'description']
    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'code', 'niveau', 'icone')
        }),
        ('Description', {
            'fields': ('description',)
        }),
    )
    
    def nombre_chapitres(self, obj):
        return obj.chapitres.count()
    nombre_chapitres.short_description = 'Chapitres'


@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'matiere', 'numero', 'niveau', 'date_creation']
    list_filter = ['matiere', 'niveau', 'created_at']
    search_fields = ['titre', 'contenu', 'matiere__nom']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    list_select_related = ['matiere']
    
    def date_creation(self, obj):
        return obj.created_at.strftime('%d/%m/%Y')
    date_creation.short_description = 'Date création'

