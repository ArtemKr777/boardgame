# games/tests/test_views.py
import pytest
from django.test import Client
from django.contrib.auth.models import User
from games.models import Game
from users.models import Profile


@pytest.mark.django_db
class TestGamesViews:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass123')

        # Создаём тестовые игры (латиницей для тестов)
        Game.objects.create(
            name="Carcassonne", min_players=2, max_players=5,
            min_duration=30, max_duration=45, min_age=7
        )
        Game.objects.create(
            name="Bunker", min_players=4, max_players=16,
            min_duration=30, max_duration=60, min_age=18
        )

    def test_game_list_requires_login(self):
        self.client.logout()
        response = self.client.get('/games/')
        assert response.status_code == 302  # перенаправление на login

    def test_game_list_authenticated(self):
        response = self.client.get('/games/')
        assert response.status_code == 200
        # Проверяем через декодирование в строку
        content = response.content.decode('utf-8')
        assert "Carcassonne" in content
        assert "Bunker" in content

    def test_filter_by_name_icontains(self):
        response = self.client.get('/games/?name=carcassonne')
        content = response.content.decode('utf-8')
        assert "Carcassonne" in content
        assert "Bunker" not in content

    def test_filter_by_players(self):
        response = self.client.get('/games/?players=4')
        content = response.content.decode('utf-8')
        assert "Carcassonne" in content
        assert "Bunker" in content

    def test_filter_by_players_6(self):
        response = self.client.get('/games/?players=6')
        content = response.content.decode('utf-8')
        assert "Carcassonne" not in content
        assert "Bunker" in content

    def test_filter_by_age_min_12(self):
        response = self.client.get('/games/?age_min=12')
        content = response.content.decode('utf-8')
        assert "Carcassonne" not in content
        assert "Bunker" in content

    def test_filter_by_time_range(self):
        response = self.client.get('/games/?time_min=40&time_max=50')
        content = response.content.decode('utf-8')
        assert "Carcassonne" in content
        assert "Bunker" in content