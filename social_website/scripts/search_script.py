import site, sys
from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
import json, urllib2
from pyes import *
from social_website.models import Collection, Video, Partner

conn = ES(['127.0.0.1:9200'])
try:
    conn.delete_index("test-index")
    print "Previous index deleted"
except Exception, ex:
    print "No Previous index"
settings = {
            "analysis":{
               "filter":{
                  "name_ngrams":{
                     "side":"front",
                     "max_gram":20,
                     "min_gram":2,
                     "type":"edgeNGram"
                  }
               },
               "analyzer":{
                  "full_name":{
                     "filter":[
                        "standard",
                        "lowercase",
                        "asciifolding"
                     ],
                     "type":"custom",
                     "tokenizer":"keyword"
                  },
                  "partial_name":{
                     "filter":[
                        "standard",
                        "lowercase",
                        "asciifolding",
                        "name_ngrams"
                     ],
                     "type":"custom",
                     "tokenizer":"standard"
                  }
               }
            }
         }

mappings = {
      "test-index":{
        "properties":{
            "searchTerm":{
               "fields":{
                  "searchTerm":{
                     "type":"string",
                     "analyzer":"full_name"
                  },
                  "partial":{
                     "search_analyzer":"full_name",
                     "index_analyzer":"partial_name",
                     "type":"string"
                  }
               },
               "type":"multi_field"
            }
         }
      }
}
        
conn.indices.create_index("test-index", settings = settings)

conn.indices.put_mapping(doc_type = "test-index", mapping = mappings, indices = ["test-index"])

# Video
i = 0
for video in Video.objects.all():
    if len(video.collection_set.all()):
        collection = video.collection_set.all()[0]  # choosing the first collection
        for index, vid in enumerate(collection.videos.all()):
            if vid.uid == video.uid:
                vid_id = index+1 
        url = "/social/collections/?id=" + str(collection.uid) + "&video=" + str(vid_id) 
        data = json.dumps({"searchTerm":video.title, 
                           "targetURL" : url,
                           "type" : "Videos"})
        conn.index(data, "test-index", "test-index",i+1)
        i+= 1
print i 

# Collections        
for collection in Collection.objects.all():
    if collection.subject != '':
        url = "/social/discover/?title=%s" % str(collection.subject)
        data = json.dumps({"searchTerm" : collection.subject,
                           "targetURL" : url, 
                           "type" : "Collections"}) 
        conn.index(data, "test-index", "test-index",i+1)
        i+= 1
    if collection.topic != '':
        url = "/social/discover/?title=%s" % str(collection.topic)
        data = json.dumps({"searchTerm" : collection.topic,
                           "targetURL" : url, 
                           "type" : "Collections"}) 
        conn.index(data, "test-index", "test-index",i+1)
        i+= 1
print i

# Partner
for partner in Partner.objects.all():
    url = "/social/connect/?id=" + str(partner.uid)
    data = json.dumps({"searchTerm" : partner.name,
                       "targetURL" : url, 
                       "type" : "Partners"}) 
    conn.index(data, "test-index", "test-index",i+1)
    i+= 1
print i
    
#################  QUERY  ###########################
#===============================================================================
# conn.default_indices="test-index"
# conn.refresh("test-index")
# q = {"query" : {
#                "query_string" :{
#                                 "fields" : ["searchTerm.partial"],
#                                 "query" : "see"
#                                 }
#                },
#     "facets" : {
#                 "facet" : {
#                            "terms" : { "fields"  : ["searchTerm"] }
#                            }
#                 },
#     "size" : 10
#     }
#                                  
# query = json.dumps(q)
# response = urllib2.urlopen('http://localhost:9200/test-index/_search',query)
# result = json.loads(response.read())
# print result
# result_list = []
# for res in result['hits']['hits']:
#    result_list.append(res['_source'])
# print len(result_list)
# facets = json.dumps(result['facets']['facet']['terms'])
# print facets
#===============================================================================

    
