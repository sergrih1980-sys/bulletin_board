import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@pytest.fixture
def user_factory():
    """Фабрика для создания тестовых пользователей (с учётом REQUIRED_FIELDS)."""
    def _create(email="test@example.com", first_name="Test", last_name="User", **kwargs):
        defaults = {
            "email": email,
            "password": "password123",
            "first_name": first_name,
            "last_name": last_name,
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return _create

@pytest.fixture
def authenticated_client(user_factory):
    """Клиент с авторизацией (Bearer token)."""
    user = user_factory()
    client = APIClient()
    token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    client.user = user  # Сохраняем пользователя, чтобы можно было проверить авторство
    return client

@pytest.fixture
def ad_factory(authenticated_client):
    """Фабрика для быстрого создания объявлений."""
    def _create(**kwargs):
        defaults = {
            "title": "Тестовое объявление",
            "description": "Описание для теста",
            "price": 100,
        }
        defaults.update(kwargs)
        # Используем того же клиента, что и в фикстуре, он уже авторизован
        response = authenticated_client.post("/api/ads/", defaults, format="json")
        assert response.status_code == 201, f"Не удалось создать объявление: {response.data}"
        return response.data
    return _create