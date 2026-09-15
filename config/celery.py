import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('bulletin_board')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'deactivate-old-ads': {
        'task': 'ads.tasks.deactivate_old_ads',
        'schedule': 86400,  # раз в сутки (в секундах)
    },
}