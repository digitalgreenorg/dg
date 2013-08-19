from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import datetime
from dashboard import models
from social_website.models import CronTimestamp
from social_website.migration_functions import populate_adoptions, populate_farmers, update_person_video_record, update_questions_asked, update_website_video


def process_log(objects, logfile):
    pma_count = 0
    for object in objects:
        logfile.write(object.entry_table)
        if object.entry_table == 'Screening':
            screening_object = models.Screening.objects.get(id = object.model_id)
            videos = screening_object.videoes_screened.all()
            for pma in screening_object.personmeetingattendance_set.all():
                update_person_video_record(pma, videos)
                update_questions_asked(pma)
                logfile.write(' Added Pma ')
                pma_count += 1
        elif object.entry_table == "PersonAdoptPractice":
            pap_object = models.PersonAdoptPractice.objects.get(id = object.model_id)
            populate_adoptions(pap_object)
            logfile.write(' Added Pap ')
        elif object.entry_table == 'Video':
            video_object = models.Video.objects.get(id = object.model_id)
            update_website_video(video_object)
            logfile.write(' Added Video ')
        elif object.entry_table == 'Person':
            person_object = models.Person.objects.get(id = object.model_id)
            if person_object.image_exists :
                populate_farmers(person_object)
                logfile.write(' Added Person ')
        logfile.write('\n')
        print pma_count
        
        
         

script_name = 'website_sync'
file_name = script_name + str(datetime.datetime.now().date()) + ".txt"
logfile = open(file_name, "w")
timestamp = CronTimestamp.objects.get(name = script_name).last_time
serverlog_objects = models.ServerLog.objects.filter(timestamp__gte = timestamp)
process_log(serverlog_objects[:100], logfile)

    


