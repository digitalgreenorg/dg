from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
from dashboard.models import District
import urllib
import urllib2
import json

for d in District.objects.all():
    address = u"%s,%s,%s"%(d.district_name,d.state.state_name,d.state.country.country_name)
    urlparams = (('address',address.encode('utf-8')),('sensor','false'))
    print urllib.urlencode(urlparams)
    val = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?"+urllib.urlencode(urlparams))
    data = json.loads(val.read())
    try:
        d.latitude = data['results'][0]['geometry']['location']['lat']
        d.longitude = data['results'][0]['geometry']['location']['lng']
        d.save()
    except:
        print "Geocodes not found for %s, %s" % (d.district_name, d.state.state_name)


def get_lat_lon(self):

    # Call get_lat_lon in pre_save
    urlparams = (('address',"%s,%s,India"%(d.district_name,d.state.state_name)),('sensor',False))
    val = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?"+urllib.urlencode(urlparams))
    data = json.loads(val.read())
    try:
        d.lat = data['results'][0]['geometry']['location']['lat']
        d.lon = data['results'][0]['geometry']['location']['lon']
    except:
        pass

