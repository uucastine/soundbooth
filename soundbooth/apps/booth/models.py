import uuid
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
    date = models.DateTimeField(
        _('Date'),
        blank=True,
        null=True
    )
    rule = models.CharField(
        _('Recurring rule'),
        max_length=255,
        blank=True,
        null=True
    )


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Scheduled recording for {}'.format(self.created)

    def get_absolute_url(self):
        return reverse('booth:schedule-detail', args=(self.uid,))


    def get_update_url(self):
        return reverse('booth:schedule-update', args=(self.uid,))
