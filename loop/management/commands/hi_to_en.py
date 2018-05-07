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
        translator = Translator()
        
        # farmer_list = Farmer.objects.filter(village__id__in=[1,2]).values('id','name')
        # for farmer in farmer_list:
        # 	translation = translator.translate(farmer['name'], src='hi', dest='en')
        # 	print farmer['name'], ' - >', translation.text
        # 	farmer_obj = Farmer.objects.get(id=farmer['id'])
        # 	farmer_obj.farmer_name_en = translation.text
        # 	farmer_obj.save()

        transporter_list = Transporter.objects.values('id','transporter_name')
        print transporter_list.count()
        for transporter in transporter_list:
        	translation = translator.translate(transporter['transporter_name'], src='hi', dest='en')
        	transporter_obj = Transporter.objects.get(id=transporter['id'])
        	transporter_obj.transporter_name_en = translation.text
        	transporter_obj.save()





