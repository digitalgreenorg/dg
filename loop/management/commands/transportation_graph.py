import os
import sys
import pandas as pd
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from loop.models import LoopUser, CombinedTransaction, Crop, Mandi, Farmer, DayTransportation

class Command(BaseCommand):
    help = '''This command plost graph for transportation details for Market Recommendation. '''

    def handle(self,*args,**options):
        print("Transportation Graphs")
        dt_list = pd.DataFrame(list(DayTransportation.objects.filter(Q(transportation_vehicle__vehicle__id = 4) | Q(transportation_vehicle__vehicle__id =5)).values('id')))
        print dt_list.head()
