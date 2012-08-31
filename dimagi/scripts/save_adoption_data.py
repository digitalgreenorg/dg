from django.core.management import setup_environ
import settings
setup_environ(settings)
from xml.dom import minidom
import time
from datetime import datetime,timedelta
from dashboard.models import *

xml_tree = minidom.parse(r'C:\Users\dg_systems\Documents\GitHub\dg\dimagi\submitted\adoption_sample1.xml')
xml_data=xml_tree.getElementsByTagName('data')


for record in xml_data:
    screening_data = {}
    screening_data['date'] = record.getElementsByTagName('date')[0].firstChild.data
    screening_data['selected_village'] = record.getElementsByTagName('selected_village')[0].firstChild.data
    screening_data['selected_group'] = record.getElementsByTagName('selected_group')[0].firstChild.data
    screening_data['selected_mediator'] = record.getElementsByTagName('selected_mediator')[0].firstChild.data
    screening_data['selected_person'] = record.getElementsByTagName('selected_person')[0].firstChild.data
    screening_data['selected_video'] = record.getElementsByTagName('selected_video')[0].firstChild.data


# saving the person_adopt_practice record    
pap = PersonAdoptPractice( person_id = screening_data['selected_person'],
                             date_of_adoption = screening_data['date'],
                             video_id = screening_data['selected_video'])
try:
    pap.save()
    print "Adoption record saved"
except Exception as exception:
    print "Exception occurred- " + str(exception)
