import settings
from django.core.management import setup_environ
setup_environ(settings)
import urllib,urllib2,json
from website.models import *

i=1
for obj in Collection.objects.all():
    url = "http://localhost:9200/website/searchcollection/"
    url = url + str(i)
    request = urllib2.Request(url)
    vid_data = []
    likes = views = adoptions = 0
    for vid in obj.videos.all():
        vid_data.append({"title" : vid.title, "subtopic" : vid.subtopic, "description" : vid.description})
        likes += vid.onlineLikes + vid.offlineLikes
        views += vid.onlineViews + vid.offlineViews
        adoptions += vid.adoptions
    video = json.dumps(vid_data)
    data = json.dumps({"title" : obj.title, "url" : "", "language" : obj.language.name,"partner" : obj.partner.name, 
                       "state" : obj.state, "country" : obj.country.countryName,"category" : obj.category, 
                       "subcategory" : obj.subcategory, "topic": obj.topic, "subject" : obj.subject, "video" : video,
                       "likes" : likes, "views" : views, "adoptions" : adoptions})
    request.get_method = lambda: 'PUT'
    try:
        result = urllib2.urlopen(request, data)
        i =i + 1
    except Exception,ex:
        print str(ex) + " " +  str(data) + " " + url
print i