from django.contrib import admin
from .models import Devoir


@admin.register(Devoir)
class DevoirAdmin(admin.ModelAdmin):
    list_display = ['user', 'matiere', 'note', 'created_at']
    list_filter = ['matiere', 'created_at']
    search_fields = ['texte_reconnu', 'matiere']

