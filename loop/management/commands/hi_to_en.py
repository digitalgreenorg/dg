import os
import sys
import subprocess
from django.core.management.base import BaseCommand, CommandError
from dg.settings import DATABASES

import MySQLdb

from loop.models import Farmer, Gaddidar, \
    Transporter, Language

from googletrans import Translator

class Command(BaseCommand):
    help = '''This command converts hindi text to english using googletrans api. (http://py-googletrans.readthedocs.io/en/latest/)'''

    def handle(self, *args, **options):
        print("Start")
        farmer_list = Farmer.objects.filter(village__id__in=[1,2]).values('id','name')
        translator = Translator()

        print farmer_list.count()
        
        for farmer in farmer_list:
        	translation = translator.translate(farmer['name'], src='hi', dest='en')
        	print farmer['name'], ' - >', translation.text
        	farmer = Farmer.objects.get(id=farmer['id'])
        	farmer.farmer_name_en = translation.text
        	farmer.save()



