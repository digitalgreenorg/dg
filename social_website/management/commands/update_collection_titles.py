from dg.settings import *

from django.core.management.base import BaseCommand

from django.db import models

from geographies.models import *

from people.models import *

from activities.models import *
from social_website.models import *

import csv, ast

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            obj = Collection.objects.all()
            for item in obj:
                item.title = item.title.strip()
                item.save()
            print "success"
        except Exception as e:
            print e
        
