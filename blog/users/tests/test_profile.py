# users/tests/test_profile.py
import pytest
from django.test import Client
from django.contrib.auth.models import User
from users.models import Profile, OwnedGame, PlayedGame, PlayerResult
from games.models import Game


@pytest.mark.django_db
class TestUserProfile:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        Profile.objects.create(user=self.user, age=25, city='Moscow')
        self.client.login(username='testuser', password='testpass123')

        self.game = Game.objects.create(name="Carcassonne", min_players=2, max_players=5)
        self.game2 = Game.objects.create(name="Bunker", min_players=4, max_players=16)

    def test_profile_page(self):
        response = self.client.get('/users/profile/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'testuser' in content
        assert '25' in content
        assert 'Moscow' in content

    def test_edit_profile(self):
        response = self.client.post('/users/profile/edit/', {
            'first_name': 'Test',
            'email': 'test@example.com',
            'city': 'SPb',
            'age': 30,
            'phone': '123456789'
        })
        assert response.status_code == 302
        self.user.refresh_from_db()
        assert self.user.first_name == 'Test'
        profile = Profile.objects.get(user=self.user)
        assert profile.city == 'SPb'
        assert profile.age == 30

    def test_add_to_collection(self):
        response = self.client.get(f'/games/add-to-collection/{self.game.id}/')
        assert response.status_code == 302
        assert OwnedGame.objects.filter(user=self.user, game=self.game).exists()

    def test_user_list_page(self):
        # Создаём второго пользователя
        user2 = User.objects.create_user(username='boris', password='pass')
        Profile.objects.create(user=user2)

        response = self.client.get('/users/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'boris' in content

    def test_search_user_by_name(self):
        # Создаём пользователей
        User.objects.create_user(username='alexander', password='pass')
        User.objects.create_user(username='boris', password='pass')

        response = self.client.get('/users/?q=alex')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'alexander' in content
        assert 'boris' not in content

    def test_other_profile_hides_email(self):
        other_user = User.objects.create_user(
            username='other',
            password='pass',
            email='secret@example.com'
        )
        Profile.objects.create(user=other_user)

        response = self.client.get(f'/users/{other_user.id}/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'other' in content
        assert 'secret@example.com' not in content