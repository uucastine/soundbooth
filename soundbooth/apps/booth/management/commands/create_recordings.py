from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from booth.tasks import new_recording
from booth.models import Schedule

import logging
logger = logging.getLogger(__name__)

from booth.models import Recording

class Command(BaseCommand):
    help = 'Run through schedules creating new recordings'

    def handle(self, *args, **options):
        # Gather all subscriptions that need to go out
        #subs = Subscription.objects.live()
        schedules = Schedule.objects.filter(active=True)
        logger.debug('Checking for scheduled recordings ...')
        for schedule in schedules:
            if schedule.next_date:
                if schedule.next_date <= datetime.now():
                    logger.debug('Spin off recording task for {}'.format(schedule))
                    new_recording.delay(schedule.id)

                #email = EmailMessage("Where's Your Trash?", txt_content, FROM_EMAIL, [recipient])
                #email.send()
