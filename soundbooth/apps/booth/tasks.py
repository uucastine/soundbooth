from celery import shared_task
from .models import Schedule, Recording
from .utils import record_to_file
from datetime import datetime


@shared_task
def record_audio(duration):
    filename = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    record_to_file(duration, filename)

@shared_task
def check_schedules():
    """ process_schedules

    Grab all active schedules, and run through them, checking if :
    """
    schedules = Schedule.objects.filter(active=True)
    print('Checking for scheduled recordings ...')
    for schedule in schedules:
        if schedule.next_date:
            if schedule.next_date <= datetime.now():
                print('Spin off recording task for {}'.format(schedule))
                start_new_recording.delay(schedule.duration)

