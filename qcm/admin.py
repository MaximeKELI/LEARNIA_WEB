from django.contrib import admin
from .models import QCM, Question, Choix, ResultatQCM


class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 3
    fields = ['texte', 'est_correct']


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['numero', 'texte']
    show_change_link = True


@admin.register(QCM)
class QCMAdmin(admin.ModelAdmin):
    list_display = ['titre', 'user', 'chapitre', 'nombre_questions', 'created_at']
    list_filter = ['created_at', 'chapitre__matiere']
    search_fields = ['titre', 'user__username', 'texte_source']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'titre', 'chapitre', 'texte_source', 'created_at', 'updated_at']
    inlines = [QuestionInline]
    
    def nombre_questions(self, obj):
        return obj.questions.count()
    nombre_questions.short_description = 'Nombre de questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['numero', 'qcm', 'texte_court', 'nombre_choix', 'choix_correct']
    list_filter = ['qcm', 'qcm__chapitre__matiere']
    search_fields = ['texte', 'qcm__titre']
    inlines = [ChoixInline]
    
    def texte_court(self, obj):
        return obj.texte[:100] + '...' if len(obj.texte) > 100 else obj.texte
    texte_court.short_description = 'Texte'
    
    def nombre_choix(self, obj):
        return obj.choix.count()
    nombre_choix.short_description = 'Choix'
    
    def choix_correct(self, obj):
        correct = obj.choix.filter(est_correct=True).first()
        return correct.texte[:50] if correct else 'Aucun'
    choix_correct.short_description = 'Bonne réponse'


@admin.register(Choix)
class ChoixAdmin(admin.ModelAdmin):
    list_display = ['question', 'texte_court', 'est_correct']
    list_filter = ['est_correct', 'question__qcm']
    search_fields = ['texte', 'question__texte']
    
    def texte_court(self, obj):
        return obj.texte[:50] + '...' if len(obj.texte) > 50 else obj.texte
    texte_court.short_description = 'Texte'


@admin.register(ResultatQCM)
class ResultatQCMAdmin(admin.ModelAdmin):
    list_display = ['user', 'qcm', 'score', 'total', 'pourcentage', 'created_at']
    list_filter = ['created_at', 'qcm__chapitre__matiere']
    search_fields = ['user__username', 'qcm__titre']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'qcm')

