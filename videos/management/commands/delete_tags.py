from dg.settings import *

from django.core.management.base import BaseCommand

from django.db import models
from django.db import connection

from geographies.models import *

from activities.models import *

import csv, ast

class Command(BaseCommand):
   def handle(self, *args, **options):
       with connection.cursor() as cursor:
            query = '''delete from videos_video_tags where tag_id not in (1,2,3)'''
            cursor.execute(query)
            print 'Query Completed'
