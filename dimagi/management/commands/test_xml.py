import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from datetime import datetime, timedelta
from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser, CommCareCase
from dimagi.scripts.update_cases_functions import close_case, update_case, write_new_cases
from people.models import Person

from xml.dom import minidom
from django.core.management.base import BaseCommand

from dimagi.models import error_list, XMLSubmission
from dimagi.scripts import save_mobile_data
from dimagi.scripts.exception_email import sendmail

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        xml_object = XMLSubmission.objects.get(id=12072)
        xml_string = xml_object.xml_data
        xml_parse = minidom.parseString(xml_string)
        save_mobile_data.save_screening_data(xml_parse)
