from django.contrib import admin
from .models import Examen, RevisionPlanifiee, Rappel


@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ['nom', 'user', 'matiere', 'date_examen']
    list_filter = ['date_examen', 'matiere']


@admin.register(RevisionPlanifiee)
class RevisionPlanifieeAdmin(admin.ModelAdmin):
    list_display = ['chapitre', 'user', 'date_revision', 'type_revision', 'terminee']
    list_filter = ['type_revision', 'terminee', 'date_revision']


@admin.register(Rappel)
class RappelAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'date_rappel', 'envoye']
    list_filter = ['envoye', 'date_rappel']

