import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from faker import Faker

fake = Faker()

@pytest.mark.django_db
def test_ad_list_unauthenticated():
    client = APIClient()
    url = reverse('ad-list')
    resp = client.get(url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_ad_create_authenticated(user_factory):
    user = user_factory()
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse('ad-list')
    data = {
        'title': fake.sentence(),
        'price': 100,
        'description': fake.text(),
        'is_active': True,
    }
    resp = client.post(url, data)
    assert resp.status_code == 201
    assert resp.data['author'] == user.id

@pytest.mark.django_db
def test_ad_update_only_owner(user_factory, ad_factory):
    owner = user_factory()
    ad = ad_factory(author=owner)
    other = user_factory()

    client = APIClient()
    client.force_authenticate(user=other)
    url = reverse('ad-detail', kwargs={'pk': ad.pk})
    resp = client.patch(url, {'title': 'Hacked title'})
    assert resp.status_code == 403  # запрещено