from django.contrib import admin
from .models import QCM, Question, Choix, ResultatQCM


class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(QCM)
class QCMAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'created_at']
    list_filter = ['created_at']
    search_fields = ['titre', 'user__username']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'qcm', 'texte']
    list_filter = ['qcm']
    inlines = [ChoixInline]


@admin.register(ResultatQCM)
class ResultatQCMAdmin(admin.ModelAdmin):
    list_display = ['user', 'qcm', 'score', 'total', 'pourcentage', 'created_at']
    list_filter = ['created_at']

