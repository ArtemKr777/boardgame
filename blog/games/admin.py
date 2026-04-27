from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_players', 'max_players', 'get_duration_display', 'get_age_display', 'min_duration', 'max_duration', 'min_age', 'max_age')
    search_fields = ('name', 'thematics', 'categories')
    list_filter = ('min_players', 'max_players')
    list_editable = ('min_players', 'max_players')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
        ('Количество игроков', {
            'fields': ('min_players', 'max_players')
        }),
        ('Время игры', {
            'fields': ('min_duration', 'max_duration')
        }),
        ('Возраст', {
            'fields': ('min_age', 'max_age')
        }),
        ('Описание', {
            'fields': ('thematics', 'categories')
        }),
    )