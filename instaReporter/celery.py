from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instaReporter.settings')

from django.conf import settings  # noqa

app = Celery('instaReporter')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'run-every-day': {
        'task': 'main.tasks.display_account',
        'schedule': timedelta(seconds=30),

    },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))