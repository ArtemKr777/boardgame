from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    min_players = models.IntegerField(verbose_name="Мин. игроков")
    max_players = models.IntegerField(verbose_name="Макс. игроков")
    min_duration = models.IntegerField(verbose_name="Мин. время (мин)", null=True, blank=True)
    max_duration = models.IntegerField(verbose_name="Макс. время (мин)", null=True, blank=True)
    min_age = models.IntegerField(verbose_name="Мин. возраст", null=True, blank=True)
    max_age = models.IntegerField(verbose_name="Макс. возраст", null=True, blank=True)
    thematics = models.TextField(verbose_name="Тематики", blank=True)
    categories = models.TextField(verbose_name="Категории", blank=True)

    def __str__(self):
        return self.name

    def get_duration_display(self):
        if self.min_duration and self.max_duration:
            if self.min_duration == self.max_duration:
                return f"{self.min_duration} мин"
            else:
                return f"{self.min_duration}-{self.max_duration} мин"
        elif self.min_duration:
            return f"от {self.min_duration} мин"
        elif self.max_duration:
            return f"до {self.max_duration} мин"
        return "Не указано"

    def get_age_display(self):
        if self.min_age and self.max_age:
            if self.min_age == self.max_age:
                return f"{self.min_age}+"
            else:
                return f"{self.min_age}-{self.max_age}"
        elif self.min_age:
            return f"{self.min_age}+"
        return "Не указано"

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"