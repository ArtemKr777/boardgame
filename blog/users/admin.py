from django.contrib import admin
from .models import UserSessionLog

@admin.register(UserSessionLog)
class UserSessionLogAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user', 'page_views', 'start_time', 'last_activity')
    list_filter = ('user', 'start_time')
    search_fields = ('session_key', 'user__username')
    readonly_fields = ('session_key', 'start_time', 'last_activity', 'page_views')