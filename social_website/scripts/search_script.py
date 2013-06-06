import site, sys
sys.path.append('/home/ubuntu/code/dg_test')
site.addsitedir('/home/ubuntu/.virtualenv/dg_/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)
import json
from pyes import *
from social_website.models import Collection

conn = ES(['127.0.0.1:9200'])
try:
    conn.delete_index("test-index")
    print "Previous index deleted"
except Exception, ex:
    print "No Previous index"

mappings ={
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
                                                "tokenizer":"standard"
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
                       },
           "mapping":{ 
           "text_index":{
                 "properties":{
                               "type" : {
                                         "type" : "string"
                                         },
                               "targetURL" : {
                                        "type" : "string"
                                        } ,     
                               "searchTerm":{
                                       "fields":{
                                                 "text":{
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
}
conn.indices.create_index("test-index")

conn.indices.put_mapping("text_index",mapping = mappings, indices = ["test-index"])

# putting in the data
i = 0
print Collection.objects.all().count()
for collection in Collection.objects.all():
    data = json.dumps({"searchTerm":collection.title,"targetURL":"","type":"Collection"})
    conn.index(data, "test-index", "test-index",i+1)
#    conn.index({"name":"data1", "value":"value1"}, "test-index", "test-type2", i+1, parent=i+1)
    i+= 1
    print i
    
conn.default_indices="test-index"
conn.refresh("test-index")
q = { "term":{"searchTerm" : "seed treatment"}}
try :
    results = conn.search(q,indices=['test-index'])
    print len(results)
except Exception, ex:
    print ex
print type(results)
for r in results:
    print r 
    print r._meta.score
    