# games/tests/test_models.py
import pytest
from games.models import Game


@pytest.mark.django_db
class TestGameModel:

    def test_create_game(self):
        game = Game.objects.create(
            name="Test Game",
            min_players=2,
            max_players=4,
            min_duration=30,
            max_duration=60,
            min_age=12,
            thematics="Strategy, Fantasy",
            categories="For two, Card game"
        )
        assert game.name == "Test Game"
        assert game.min_players == 2
        assert game.max_players == 4
        # Метод возвращает русский текст
        assert game.get_duration_display() == "30-60 мин"  # ← изменено с "min" на "мин"

    def test_get_age_display(self):
        # Указываем оба обязательных поля: min_players и max_players
        game = Game.objects.create(
            name="Game 18+",
            min_players=1,
            max_players=4,  # ← добавили
            min_age=18
        )
        assert game.get_age_display() == "18+"

        game2 = Game.objects.create(
            name="Game 7-10",
            min_players=1,
            max_players=4,  # ← добавили
            min_age=7,
            max_age=10
        )
        assert game2.get_age_display() == "7-10"

    def test_get_duration_display_range(self):
        game = Game.objects.create(
            name="Test Range",
            min_players=1,
            max_players=4,  # ← добавили
            min_duration=45,
            max_duration=90
        )
        assert game.get_duration_display() == "45-90 мин"  # ← изменено

    def test_get_duration_display_single(self):
        game = Game.objects.create(
            name="Test Single",
            min_players=1,
            max_players=4,  # ← добавили
            min_duration=30,
            max_duration=30
        )
        assert game.get_duration_display() == "30 мин"  # ← изменено

    def test_get_duration_display_min_only(self):
        game = Game.objects.create(
            name="Test Min Only",
            min_players=1,
            max_players=4,  # ← добавили
            min_duration=30,
            max_duration=None
        )
        assert game.get_duration_display() == "от 30 мин"  # ← изменено