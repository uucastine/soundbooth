from datetime import datetime

from celery import shared_task
from django.core import management

from .models import Schedule, Recording
from .utils import record_to_file

@shared_task
def new_recording(schedule_id):
    filename = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    schedule = Schedule.objects.filter(pk=schedule_id).first()
    recording = None
    if schedule:
        recording = Recording.objects.create(
            schedule=schedule
        )
        recording.audio_file = record_to_file(schedule.duration, filename)
        recording.in_progress = False
        recording.finished = datetime.now()
        recording.save()
    return recording


@shared_task
def upload_to_s3():
    """ 

    Should run through recordings and upload them to S3
    """
    return 's3_path'
