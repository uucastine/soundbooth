import json
import uuid
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from crontab import CronTab
from recurrent import RecurringEvent
from dateutil import rrule

# We setup a temporary file storage location on the server for our media files
# so we can get our mimetypes before uploading to S3
from django.core.files.storage import FileSystemStorage

temp_fs = FileSystemStorage(location='/tmp')

class Recording(models.Model):
    ''' Recording

    Keeps track of recordings made by the system and their progress on the
    way up to S3 '''

    # Fields
    uid = models.UUIDField(
        _('Public ID'),
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False
    )
    audio_file = models.FileField(
        _('Audio file'),
        upload_to='audio_files',
        null=True,
        blank=True
    )
    in_progress = models.BooleanField(
        _('Recoridng in progress'),
        default=False
    )
    s3_path = models.CharField(
        _('S3 path'),
        max_length=255,
        null=True,
        blank=True
    )
    schedule = models.ForeignKey(
        'Schedule',
        blank=True,
        null=True
    )


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Recording from {}'.format(self.created)

    def get_absolute_url(self):
        return reverse('booth:recordings-detail', args=(self.uid,))


    def get_update_url(self):
        return reverse('booth:recordings-update', args=(self.uid,))


    def save(self, *args, **kwargs):
        super(Recording, self).save(*args, **kwargs)


class Schedule(models.Model):
    uid = models.UUIDField(
        _('Public ID'),
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False
    )
    active = models.BooleanField(
        _('Active'),
        default=True,
    )
    date = models.DateTimeField(
        _('Date'),
        blank=True,
        null=True,
        help_text='One-off recording date, can be blank for recurring events.'
    )
    crontab = models.CharField(
        _('Crontab format'),
        max_length=255,
        blank=True,
        null=True,
        help_text='A crontab format for recurring schedules',
    )
    duration = models.IntegerField(
        _('Duration (minutes)'),
        default=30,
    )


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Scheduled recording for {}'.format(self.created)

    def get_absolute_url(self):
        return reverse('booth:schedules-detail', args=(self.uid,))


    def get_update_url(self):
        return reverse('booth:schedules-update', args=(self.uid,))

    def get_crontab(self):
        tab = {}
        if self.crontab:
            pieces = self.crontab.split(' ')
            tab['minute']=pieces[0]
            tab['hour']=pieces[1]
            tab['day_of_week']=pieces[2]
            tab['day_of_month']=pieces[3]
            tab['month_of_year']=pieces[4]
            tab, _ = CrontabSchedule.objects.get_or_create(**tab)
        return tab


    def save(self, *args, **kwargs):
        super(Schedule, self).save(*args, **kwargs)
        self._create_periodictask()


    def _create_periodictask(self):
        if self.crontab:
            task, _ = PeriodicTask.objects.get_or_create(
                name='Task for schedule {}'.format(self.uid),
            )
            task.crontab=self.get_crontab()
            task.task='booth.tasks.new_recording'
            task.kwargs=json.dumps({
                'schedule_id': self.id
            })
            task.save()

