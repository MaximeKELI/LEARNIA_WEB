from django.contrib import admin
from .models import Badge, UserBadge, UserProgress, Leaderboard


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['nom', 'icone', 'condition_type', 'points_xp']
    list_filter = ['condition_type']
    search_fields = ['nom', 'description']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'obtenu_le']
    list_filter = ['obtenu_le', 'badge']
    search_fields = ['user__username', 'badge__nom']
    date_hierarchy = 'obtenu_le'


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'niveau', 'points_xp', 'jours_streak', 'qcm_completes']
    list_filter = ['niveau']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'position', 'score', 'periode', 'date']
    list_filter = ['periode', 'date']

