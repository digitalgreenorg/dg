import settings
from django.core.management import setup_environ
setup_environ(settings)
import urllib,urllib2,json
from website.models import *
i=1
vids = Collection.objects.all().values_list('videos',flat=True)
vids = set(vids)
for id in vids:
    vid = Video.objects.get(uid = id)
    url = "http://localhost:9200/website/searchcompletion/"
    url = url + str(i)
    request = urllib2.Request(url)
    data = json.dumps({"text":vid.title,"url":"","type":"Video"})
    request.get_method = lambda: 'PUT'
    try:
        result = urllib2.urlopen(request, data)
        i =i + 1
    except Exception,ex:
        print str(ex) + " " +  str(data) + " " + url
print i

#for coll in Collection.objects.all():
#    url = "http://localhost:9200/website/searchcompletion/"
#    url = url + str(i)
#    request = urllib2.Request(url)
#    data = json.dumps({"text":coll.title,"url":"","type":"Collection"})
#    request.get_method = lambda: 'PUT'
#    try:
#        result = urllib2.urlopen(request, data)
#        i =i + 1
#    except Exception,ex:
#        print str(ex) + " " +  str(data) + " " + url
#print i

for partner in Partner.objects.all():
    url = "http://localhost:9200/website/searchcompletion/"
    url = url + str(i)
    request = urllib2.Request(url)
    data = json.dumps({"text":partner.name,"url":"","type":"Partner"})
    request.get_method = lambda: 'PUT'
    try:
        result = urllib2.urlopen(request, data)
        i =i + 1
    except Exception,ex:
        print str(ex) + " " +  str(data) + " " + url
print i 

