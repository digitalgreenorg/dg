from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

import datetime
import logging
from activities.models import Screening
from coco.models import ServerLog
from people.models import Person
from videos.models import Video
from social_website.models import CronTimestamp, PersonVideoRecord
from social_website.migration_functions import delete_person, delete_video, initial_personvideorecord, populate_farmers, update_questions_asked, update_website_video


def process_log(objects, logger):
    '''
    Server Log is used to
    - update questions asked (via dashboard.models.Screening)
    - update person details (via dashboard.models.Person)
    - create a new entry for newly linked video (via dashboard.models.Video)
    '''
    
    for object in objects:
        logger.info(object.entry_table)
        if object.entry_table == 'Screening':
            try:
                screening_object = Screening.objects.get(id = object.model_id)
                for pma in screening_object.personmeetingattendance_set.all():
                    update_questions_asked(pma)
                    logger.info(' Added Pma ')
            except Screening.DoesNotExist:
                continue
#        elif object.entry_table == "PersonAdoptPractice":
#            pap_object = models.PersonAdoptPractice.objects.get(id = object.model_id)
#            populate_adoptions(pap_object)
#            logfile.write(' Added Pap ')
        elif object.entry_table == 'Video':
            try:
                video_object = Video.objects.get(id = object.model_id)
                if object.action == -1:
                    delete_video(video_object)
                    logger.info(' Deleted Video ')
                else:
                    update_website_video(video_object)
                    logger.info(' Added Video ')
            except Video.DoesNotExist:
                continue
        elif object.entry_table == 'Person':
            try:
                person_object = Person.objects.get(id = object.model_id)
                if object.action == -1:
                    delete_person(person_object)
                    logger.info(' Deleted Person ')
                elif person_object.image_exists :
                    populate_farmers(person_object)
                    logger.info(' Added Person ')
            except Person.DoesNotExist:
                continue
        logger.info('\n')

def recreate_person_video_record():
    # Drop and re-create PersonVideoRecord
    PersonVideoRecord.objects.all().delete()
    initial_personvideorecord()

def sync_with_serverlog():
    logger = logging.getLogger('social_website')
    script_name = 'website_sync'
        
    try:
        crontimestamp = CronTimestamp.objects.get(name = script_name)
    except CronTimestamp.DoesNotExist:
        crontimestamp = CronTimestamp(last_time=datetime.datetime(2013, 7, 22, 3, 30), name=script_name)
    timestamp = crontimestamp.last_time
    serverlog_objects = ServerLog.objects.filter(timestamp__gte = timestamp)
    
    # Update last_time but dont save
    crontimestamp.last_time = datetime.datetime.now()
    
    process_log(serverlog_objects, logger)
    crontimestamp.save()

