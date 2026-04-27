# users/tests/test_user_list.py
import pytest
from django.test import Client
from django.contrib.auth.models import User
from users.models import Profile


@pytest.mark.django_db
class TestUserList:

    def setup_method(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='alex', password='pass')
        self.user2 = User.objects.create_user(username='boris', password='pass')
        self.user3 = User.objects.create_user(username='alexander', password='pass')
        Profile.objects.create(user=self.user1)
        Profile.objects.create(user=self.user2)
        Profile.objects.create(user=self.user3)
        self.client.login(username='alex', password='pass')

    def test_user_list_page(self):
        response = self.client.get('/users/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'boris' in content
        assert 'alexander' in content

    def test_search_user_by_name(self):
        response = self.client.get('/users/?q=alex')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'alexander' in content
        assert 'boris' not in content

    def test_other_profile_hides_email(self):
        other_user = User.objects.create_user(
            username='secret_user',
            password='pass',
            email='topsecret@example.com'
        )
        Profile.objects.create(user=other_user)

        response = self.client.get(f'/users/{other_user.id}/')
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        assert 'secret_user' in content
        assert 'topsecret@example.com' not in content