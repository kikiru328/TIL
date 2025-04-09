import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery')  # 이름은 아무거나, 보통 프로젝트 이름 또는 celery
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
