import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from ads.models import Ad

User = get_user_model()

@pytest.fixture
def user_factory():
    def _create(email="test@example.com", first_name="Test", last_name="User", **kwargs):
        defaults = {"email": email, "password": "password123", "first_name": first_name, "last_name": last_name}
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return _create

@pytest.fixture
def authenticated_client(user_factory):
    user = user_factory()
    client = APIClient()
    token = str(AccessToken.for_user(user))
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    client.user = user
    return client

@pytest.mark.django_db
def test_ads_list_returns_200(authenticated_client):
    response = authenticated_client.get("/api/ads/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_ad_create_returns_201(authenticated_client):
    data = {"title": "Новое тестовое объявление", "description": "Описание", "price": 250}
    response = authenticated_client.post("/api/ads/", data, format="json")
    assert response.status_code == 201

@pytest.mark.django_db
def test_ads_filtering(authenticated_client, user_factory):
    owner = user_factory(email="filter@example.com")
    Ad.objects.create(title="Дешёвый товар", description="", price=10, author=owner)
    Ad.objects.create(title="Дорогой товар", description="", price=1000, author=owner)

    response = authenticated_client.get("/api/ads/?price=10")
    assert response.status_code == 200
    results = response.json().get("results", [])
    assert any(item["title"] == "Дешёвый товар" for item in results)

@pytest.mark.django_db
def test_ad_retrieve(authenticated_client, user_factory):
    owner = user_factory(email="retrieve@example.com")
    ad = Ad.objects.create(title="Для получения", description="", price=50, author=owner)
    response = authenticated_client.get(f"/api/ads/{ad.id}/")
    assert response.status_code == 200
    assert response.json()["title"] == ad.title


@pytest.mark.django_db
def test_ad_update_own(authenticated_client):
    # Создаём объявление от имени ТОГО ЖЕ пользователя, что в authenticated_client
    ad = Ad.objects.create(
        title="До обновления",
        description="",
        price=70,
        author=authenticated_client.user,
    )

    data = {"title": "После обновления"}
    response = authenticated_client.patch(f"/api/ads/{ad.id}/", data, format="json")
    assert response.status_code == 200, f"Ожидался 200, пришёл {response.status_code}: {response.data}"
    assert response.json()["title"] == data["title"]


@pytest.mark.django_db
def test_ad_delete_own(authenticated_client):
    # Создаём объявление от имени ТОГО ЖЕ пользователя
    ad = Ad.objects.create(
        title="К удалению",
        description="",
        price=90,
        author=authenticated_client.user,
    )

    response = authenticated_client.delete(f"/api/ads/{ad.id}/")
    assert response.status_code == 204, f"Ожидался 204, пришёл {response.status_code}"
    assert not Ad.objects.filter(id=ad.id).exists()

@pytest.mark.django_db
def test_cannot_delete_others_ad(authenticated_client, user_factory):
    other_owner = user_factory(email="owner@example.com")
    ad = Ad.objects.create(title="Чужое объявление", description="", price=999, author=other_owner)

    # authenticated_client — это ДРУГОЙ пользователь
    response = authenticated_client.delete(f"/api/ads/{ad.id}/")
    # Правильно: 403 (Forbidden) или 404 (если эндпоинт скрывает чужие)
    assert response.status_code in [403, 404]
