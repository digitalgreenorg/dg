import os
import sys
from django.core.management.base import BaseCommand, CommandError
from libs.geocoder import Geocoder
from loop.models import Mandi, Village

class Command(BaseCommand):
    help = '''This command updates latitude longitude for Mandi and Village for LOOP. '''

    def handle(self,*args,**options):
        mandi_list = Mandi.objects.prefetch_related()
        for obj in mandi_list:
            address = u"%s,%s,%s,%s" % (obj.mandi_name_en,obj.district.district_name_en,obj.district.state.state_name_en,obj.district.state.country.country_name)
            self.get_coordinates(obj=obj,address=address)

        village_list = Village.objects.prefetch_related()
        for obj in village_list:
            address = u"%s,%s,%s,%s,%s" % (obj.village_name_en,obj.block.block_name_en,obj.block.district.district_name_en,obj.block.district.state.state_name_en,obj.block.district.state.country.country_name)
            self.get_coordinates(obj=obj,address=address)

    def get_coordinates(self,obj=None,address=None):
        geocoder = Geocoder()
        print address
        if geocoder.convert(address):
            try:
                lat = geocoder.getLatLng()[0]
                lon = geocoder.getLatLng()[1]
                print geocoder.getLatLng()
                obj.latitude = lat
                obj.longitude = lon
                obj.save()
            except Exception as e:
                print e
