from django.db import models
from django.contrib.auth.models import User
from games.models import Game


# =====================================================
# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
# =====================================================

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


# =====================================================
# ИГРЫ ПОЛЬЗОВАТЕЛЯ (КОЛЛЕКЦИЯ)
# =====================================================

class OwnedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')  # Один пользователь не может добавить одну игру дважды

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"


# =====================================================
# СЫГРАННЫЕ ПАРТИИ
# =====================================================

class PlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='played_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_date = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} played {self.game.name} on {self.play_date}"


# =====================================================
# РЕЗУЛЬТАТЫ УЧАСТНИКОВ ПАРТИИ
# =====================================================

class PlayerResult(models.Model):
    played_game = models.ForeignKey(PlayedGame, on_delete=models.CASCADE, related_name='results')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.IntegerField()
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['place']

    def __str__(self):
        return f"{self.player.username} - {self.place} place"


# =====================================================
# АНАЛИТИКА: ЛОГИ СЕССИЙ ПОЛЬЗОВАТЕЛЕЙ
# =====================================================

class UserSessionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    start_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    page_views = models.IntegerField(default=0)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Session {self.session_key} - {self.page_views} views"

    class Meta:
        verbose_name = "Сессия пользователя"
        verbose_name_plural = "Сессии пользователей"