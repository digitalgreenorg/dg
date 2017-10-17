import os
import sys
from django.core.management.base import BaseCommand, CommandError
from loop.models import Mandi, Village
from libs.geocoder import Geocoder

class Command(BaseCommand):
    help = '''This command updates. '''

    def handle(self,*args,**options):
        mandi_list = Mandi.objects.prefetch_related()
        for mandi in mandi_list:
            self.get_coordinates(mandi)



    def get_coordinates(self,obj):
        geocoder = Geocoder()
        # print obj
        # print obj.mandi_name_en
        # print obj.district.district_name_en
        address = u"%s,%s,%s,%s" % (obj.mandi_name_en,obj.district.district_name_en,obj.district.state.state_name_en,obj.district.state.country.country_name)
        print address
        if geocoder.convert(address):
            try:
                print geocoder.getLatLng()
                # (self.latitude,self.longitude) = geocoder.getLatLng()
            except:
                pass
