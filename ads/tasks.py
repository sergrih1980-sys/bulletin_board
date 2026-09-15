from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Ad

@shared_task
def deactivate_old_ads():
    cutoff = timezone.now() - timedelta(days=30)
    old_ads = Ad.objects.filter(is_active=True, created_at__lt=cutoff)
    count = old_ads.update(is_active=False)
    return f'Deactivated {count} ads'