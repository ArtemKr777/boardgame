from django.db import models
from django.contrib.auth.models import User
from games.models import Game


class GameRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('closed', 'Закрыт'),
        ('cancelled', 'Отменён'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    desired_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    max_players = models.IntegerField(default=4)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.creator.username}"


class RequestResponse(models.Model):
    request = models.ForeignKey(GameRequest, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)