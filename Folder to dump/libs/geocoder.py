import json
import urllib
import urllib2


class Geocoder():
    ''' This class call Google's geocoding service to geocode addresses
    How to use this class:
    geocoder = Geocoder()
    if (geocoder.convert(address)):
        (lat, lng) = geocoder.getLatLng()
    '''

    def __init__(self):
        self.SUCCESS = False
        self.google_geocode_webservice = "http://maps.googleapis.com/maps/api/geocode/json?%s"

    def convert(self, address):
        self.SUCCESS = False
        params = (('address', address.encode('utf-8')), ('sensor', 'false'))
        try:
            urlstream = urllib2.urlopen(self.google_geocode_webservice % (urllib.urlencode(params)))
        except urllib2.URLError:
            return self.SUCCESS
        data = json.loads(urlstream.read())
        try:
            self.lat = data['results'][0]['geometry']['location']['lat']
            self.lng = data['results'][0]['geometry']['location']['lng']
            self.SUCCESS = True
        except:
            return self.SUCCESS
        return self.SUCCESS

    def getLatLng(self):
        ''' Call this function only if SUCCESS is True
        '''
        if (self.SUCCESS == False):
            raise Exception
        return (self.lat, self.lng)