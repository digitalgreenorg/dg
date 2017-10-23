import os
import sys
from django.core.management.base import BaseCommand, CommandError
from loop.models import Mandi, Village
from libs.distance_matrix import DistanceMatrix

class Command(BaseCommand):
    help = '''This command fetches distance between source and destination. '''

    def handle(self,*args,**options):
        mandi_list = Mandi.objects.prefetch_related()
        source = str(mandi_list[0].latitude) + "," + str(mandi_list[0].longitude)
        destination = str(mandi_list[1].latitude) + "," + str(mandi_list[1].longitude)
        self.get_distance(source=source,destination=destination,mode='driving')

    def get_distance(self,source=None,destination=None, mode=None):
        distanceMatrix = DistanceMatrix()
        if distanceMatrix.distance(source=source, destination=destination, mode=mode):
            try:
                print distanceMatrix.getDistance()
            except Exception as e:
                print e
