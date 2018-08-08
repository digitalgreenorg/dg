from dg.settings import *
from django.core.management.base import BaseCommand
from django.db import models
from geographies.models import *
from videos.models import *
import csv, ast

class Command(BaseCommand):
   def handle(self, *args, **options):
        with open('videos/management/commands/tags.csv','rb') as f:
            reader = csv.reader(f)
            count = 0
            for line in reader:
                try:
                    obj, created = Tag.objects.get_or_create(tag_name=line[1], tag_code=line[0])
                except Exception as e:
                    print e
                    
