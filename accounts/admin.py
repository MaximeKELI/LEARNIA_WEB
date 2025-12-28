from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Matiere, Chapitre


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'niveau_etude', 'classe', 'date_joined']
    list_filter = ['niveau_etude', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations Learnia', {
            'fields': ('niveau_etude', 'classe', 'ecole', 'date_naissance', 'avatar')
        }),
    )


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'niveau', 'icone']
    list_filter = ['niveau']
    search_fields = ['nom', 'code']


@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ['titre', 'matiere', 'numero', 'niveau']
    list_filter = ['matiere', 'niveau']
    search_fields = ['titre', 'contenu']

