import settings
from django.core.management import setup_environ
setup_environ(settings)
import json
from pyes import *
from social_website.models import Collection
from django.core import serializers
from django.forms.models import model_to_dict
import datetime
from time import mktime

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)
    
conn = ES(['127.0.0.1:9200'])
#try:
#    conn.delete_index("test2")
#    print "Previous index deleted"
#except Exception, ex:
#    print "No Previous index"
#
#mappings ={
#          "test2":{
#                 "properties":{
#                               "type" : {
#                                         "type" : "string"
#                                         },
#                               "targetURL" : {
#                                        "type" : "string"
#                                        } ,     
#                               "title":{
#                                             "type":"string",
#                                            },
#                               "subcategory" : {
#                                                "type" : "string",
#                                                "tokenizer" : "keyword",
#                                                "analyzer" : "keyword"
#                                        
#                                       },
#                               "language_name" : {
#                                                "type" : "string",
#                                                
#                                                "analyzer" : "keyword"
#                                        
#                                       }
#                   }
#           }
#        }
#
#             
#conn.indices.create_index("test2")
#
#conn.indices.put_mapping(doc_type = "test2", mapping = mappings, indices = ["test2"])
#
## putting in the data
#i = 0
#print Collection.objects.all().count()
#for obj in Collection.objects.all():
#    vid_data = []
#    likes = views = adoptions = 0
#    for vid in obj.videos.all():
#        vid_data.append({"title" : vid.title, "subtopic" : vid.subtopic, 
#                         "description" : vid.description,"duration" : vid.duration, 
#                         "thumbnailURL" : vid.thumbnailURL, "youtubeID" : vid.youtubeID})
#        likes += vid.onlineLikes + vid.offlineLikes
#        views += vid.onlineViews + vid.offlineViews
#        adoptions += vid.adoptions
#    country = model_to_dict(obj.country)
#    language = model_to_dict(obj.language)
#    partner = model_to_dict(obj.partner)
#    partner["joinDate"] = partner["joinDate"].strftime("%Y-%m-%d %H:%M:%S")
#    
#    video = json.dumps(vid_data)
#    data = json.dumps({"title" : obj.title,
#                       "country" : country,
#                       "url" : "", 
#                       "language" : language,
#                       "language_name" : obj.language.name, # to search using elastic for the time being
#                       "partner" : partner, 
#                       "state" : obj.state,
#                       "category" : obj.category,
#                       "subcategory" : obj.subcategory, 
#                       "topic": obj.topic, 
#                       "subject" : obj.subject, 
#                       "likes" : likes, 
#                       "views" : views, 
#                       "adoptions" : adoptions,
#                       "thumbnailURL" : obj.thumbnailURL,
#                       "uid" : obj.uid,
#                       "videos" : vid_data,
#                       })    
#    conn.index(data, "test2","test2",i+1)
##    conn.index({"name":"data1", "value":"value1"}, "test-index", "test-type2", i+1, parent=i+1)
#    i+= 1
#    
conn.default_indices="test2"
conn.refresh("test2")
q = {"match_all" : {}}

     

#q = {"term": {"subcategory" : "crop management"}}
try :
    results = conn.search(q,indices=['test2'])
    print len(results)
except Exception, ex:
    print ex
print type(results)
for r in results:
    print r 
    print r._meta.score
    