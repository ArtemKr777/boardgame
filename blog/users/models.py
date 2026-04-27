from django.db import models
from django.contrib.auth.models import User
from games.models import Game


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class OwnedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"


class PlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='played_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    play_date = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} played {self.game.name}"


class PlayerResult(models.Model):
    played_game = models.ForeignKey(PlayedGame, on_delete=models.CASCADE, related_name='results')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.IntegerField()
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['place']

    def __str__(self):
        return f"{self.player.username} - {self.place} место"