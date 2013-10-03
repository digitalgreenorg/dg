'''populate_district_lat_long.py: One time script to populate existing districts coordinates.
   To run this file type python -m feeds.populate_district_lat_long'''

__author__ = "Aadish Gupta"

from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from dashboard.models import District
from libs.geocoder import Geocoder

geocoder = Geocoder()
for d in District.objects.all():
    address = u"%s,%s,%s" % (d.district_name, d.state.state_name, d.state.country.country_name)
    if (geocoder.convert(address)):
        try:
            (d.latitude, d.longitude) = geocoder.getLatLng()
            d.save()
        except:
            print "Geocodes not found for %s, %s" % (d.district_name, d.state.state_name)
