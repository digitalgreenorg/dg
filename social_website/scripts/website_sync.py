from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import datetime
from dashboard import models
from social_website.models import CronTimestamp, PersonVideoRecord
from social_website.migration_functions import delete_person, delete_video, initial_personvideorecord, populate_farmers, update_questions_asked, update_website_video


def process_log(objects, logfile):
    for object in objects:
        logfile.write(object.entry_table)
        if object.entry_table == 'Screening':
            screening_object = models.Screening.objects.get(id = object.model_id)
            for pma in screening_object.personmeetingattendance_set.all():
                update_questions_asked(pma)
                logfile.write(' Added Pma ')
#        elif object.entry_table == "PersonAdoptPractice":
#            pap_object = models.PersonAdoptPractice.objects.get(id = object.model_id)
#            populate_adoptions(pap_object)
#            logfile.write(' Added Pap ')
        elif object.entry_table == 'Video':
            video_object = models.Video.objects.get(id = object.model_id)
            if object.action == -1:
                delete_video(video_object)
                logfile.write(' Deleted Video ')
            update_website_video(video_object)
            logfile.write(' Added Video ')
        elif object.entry_table == 'Person':
            person_object = models.Person.objects.get(id = object.model_id)
            if object.action == -1:
                delete_person(person_object)
                logfile.write(' Deleted Person ')
            if person_object.image_exists :
                populate_farmers(person_object)
                logfile.write(' Added Person ')
        logfile.write('\n')
        
        
         

script_name = 'website_sync'

# Drop and re-create PersonVIdeoRecord
PersonVideoRecord.objects.all().delete()
initial_personvideorecord()
file_name = script_name + str(datetime.datetime.now().date()) + ".txt"
logfile = open(file_name, "w")
crontimestamp = CronTimestamp.objects.get(name = script_name)
timestamp = crontimestamp.last_time
serverlog_objects = models.ServerLog.objects.filter(timestamp__gte = timestamp)

# Update last_time but dont save
crontimestamp.last_time = datetime.datetime.now()
process_log(serverlog_objects[:200], logfile)
crontimestamp.save()



    


