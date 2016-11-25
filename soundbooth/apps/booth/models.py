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


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Recording from {}'.format(self.created)

    def get_absolute_url(self):
        return reverse('booth:recording-detail', args=(self.uid,))


    def get_update_url(self):
        return reverse('booth:recording-update', args=(self.uid,))


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
    time = models.TimeField(
        _('Time to record'),
    )
    rule = models.CharField(
        _('Recurring rule'),
        max_length=255,
        blank=True,
        null=True,
        help_text='A human-readable pattern for recurring schedules',
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
        return reverse('booth:schedule-detail', args=(self.uid,))


    def get_update_url(self):
        return reverse('booth:schedule-update', args=(self.uid,))

    def get_rrule(self):
        if self.rule:
            return rrule.rrulestr(RecurringEvent().parse(self.rule))
        return False

    @property
    def next_date(self):
        next_date = None
        rule = self.get_rrule()

        if self.date:
            next_date = self.date

        if rule:
            if datetime.now().time() <= self.time:
                reference = datetime.now()-timedelta(days=1)
            else:
                reference = datetime.now()
            n = rule.after(reference)
            next_date = datetime(
                n.year,
                n.month,
                n.day,
                self.time.hour,
                self.time.minute
            )

        return next_date

