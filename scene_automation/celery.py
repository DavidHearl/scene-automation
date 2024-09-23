from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scene_automation.settings')

app = Celery('your_project_name')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-ships-cache-every-5-minutes': {
        'task': 'your_app_name.tasks.update_ships_cache',
        'schedule': crontab(minute='*/5'),
    },
    'update-areas-cache-every-5-minutes': {
        'task': 'your_app_name.tasks.update_areas_cache',
        'schedule': crontab(minute='*/5'),
    },
}