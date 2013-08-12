from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import base64, urllib2
from dashboard import models
from social_website.models import CronTimestamp
from social_website.migration_functions import update_person_video_record, update_questions_asked


def process_log(objects):
    for object in objects:
        if object.entry_table == 'Screening':
            screening_object =models.Screening.objects.get(id = object.model_id)
            videos = screening_object.videoes_screened.all()
            for pma in screening_object.personmeetingattendance_set.all():
                #TODO - possibility to club these two functions into one
                update_person_video_record(pma, videos)
                update_questions_asked(pma)
            

script_name = 'website_sync'
timestamp = CronTimestamp.objects.get(name = script_name).last_time
serverlog_objects = models.ServerLog.objects.filter(timestamp__gte = timestamp)
process_log(serverlog_objects)

    


