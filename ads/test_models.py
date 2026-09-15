import pytest
from django.utils import timezone
from ads.models import Ad


@pytest.mark.django_db
def test_ad_creation_defaults(user_factory):
    user = user_factory()
    ad = Ad.objects.create(
        title="Тест",
        description="Описание",
        price=500,
        author=user,
    )

    assert ad.is_active is True
    assert ad.created_at is not None
    # Проверка, что дата создания не в будущем
    assert ad.created_at <= timezone.now()


@pytest.mark.django_db
def test_ad_string_representation(user_factory):
    user = user_factory()
    ad = Ad.objects.create(
        title="Куплю велосипед",
        description="Срочно",
        price=1000,
        author=user,
    )
    assert str(ad) == "Куплю велосипед"