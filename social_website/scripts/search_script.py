import site, sys
sys.path.append('/home/ubuntu/code/dg_test')
site.addsitedir('/home/ubuntu/.virtualenv/dg_/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)
import json, urllib2
from pyes import *
from social_website.models import Collection

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

#putting in the data
i = 0
print Collection.objects.all().count()
for collection in Collection.objects.all():
    data = json.dumps({"searchTerm":collection.title + " in " + collection.state})
    conn.index(data, "test-index", "test-index",i+1)
    i+= 1
    print i

    
#################  QUERY  ###########################
conn.default_indices="test-index"
conn.refresh("test-index")
q = {"query" : {
                "query_string" :{
                                 "fields" : ["searchTerm.partial"],
                                 "query" : "madhy"
                                 }
                },
     "size" : 10
     }
                                  
query = json.dumps(q)
response = urllib2.urlopen('http://localhost:9200/test-index/_search',query)
result = json.loads(response.read())
result_list = []
for res in result['hits']['hits']:
    result_list.append(res['_source'])

    
