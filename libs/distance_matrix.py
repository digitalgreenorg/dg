import json
import urllib
import urllib2


class DistanceMatrix():
    ''' This class call Google's distance matrix service to get distance between source and destination
    How to use this class:
    distanceMatrix = DistanceMatrix()
    if (distanceMatrix.distance(source,destination,mode)):
        (distance) = distanceMatrix.getDistance()
    '''

    def __init__(self):
        self.SUCCESS = False
        self.google_distance_matrix_webservice = "http://maps.googleapis.com/maps/api/distancematrix/json?%s"

    def distance(self, source=None, destination=None, mode=None):
        self.SUCCESS = False
        params = [('origins', source.encode('utf-8')), ('destinations', destination.encode('utf-8')), ('mode', mode.encode('utf-8')),('units','metric')]
        try:
            urlstream = urllib2.urlopen(self.google_distance_matrix_webservice % (urllib.urlencode(params)))
        except urllib2.URLError:
            return self.SUCCESS
        data = json.loads(urlstream.read())
        try:
            self.distance = data['rows'][0]['elements'][0]['distance']['text']
            # print self.data
            self.SUCCESS = True
        except:
            return self.SUCCESS
        return self.SUCCESS

    def getDistance(self):
        ''' Call this function only if SUCCESS is True
        '''
        if (self.SUCCESS == False):
            raise Exception
        # return (self.lat, self.lng)
        return self.distance
