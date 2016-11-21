from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'soundbooth.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations
configurations.setup()

from django.conf import settings

app = Celery('soundbooth')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
