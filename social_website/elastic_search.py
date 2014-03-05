import datetime, json, urllib2
from django.http import HttpResponse
from pyes import ES
from social_website.models import Partner
from dg.settings import COMPLETION_INDEX, FACET_INDEX, VIDEO_INDEX

MAX_RESULT_SIZE = 500 # max hits for elastic, default is 10

def get_related_collections(collection):
    related_collections = []
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices = FACET_INDEX
    conn.refresh(FACET_INDEX)
    q ={"query": {
                        "bool" : {
                                  "must_not" : {"term" : { "uid" : collection.uid }},
                            "should" : [
                                        {"terms" : { "subject" : [collection.subject] }},
                                        {"terms" : { "topic" : [collection.topic] }},
                                        ],
                            "minimum_should_match" : 1,
                                }
                  }
        }
    try :
        query = json.dumps(q)
        url = "http://localhost:9200/%s/_search" % FACET_INDEX
        response = urllib2.urlopen(url, query)
        result = json.loads(response.read())
        for res in result['hits']['hits']:
            related_collections.append(res['_source'])
    except Exception:
        pass
    return related_collections
    
def create_query(params, language_name):
    language = params.getlist('filters[language][]', None)
    subcategory = params.getlist('filters[subcategory][]', None)
    category = params.getlist('filters[category][]', None)
    partner = params.getlist('filters[partner][]', None)
    state = params.getlist('filters[state][]', None)
    topic = params.getlist('filters[topic][]', None)
    subject = params.getlist('filters[subject][]', None)
    query = []
    if language:
        query.append({"terms":{"language" : language}})
    elif language_name:
        query.append({"term":{"language" : language_name}})
    if subcategory:
        query.append({"terms":{"subcategory" : subcategory}})
    if category:
        query.append({"terms":{"category" : category}})
    if partner:
        query.append({"terms":{"partner" : partner}})
    if state:
        query.append({"terms":{"state" : state}})
    if topic:
        query.append({"terms":{"topic" : topic}})
    if subject:
        query.append({"terms":{"subject" : subject}})
    return query

def get_collections_from_elasticsearch(request):
    params = request.GET
    language_name = params.get('language__name', None)
    # TODO: Change this from 'None'?
    searchString = params.get('searchString', 'None')
    partner_uid = params.get('uid', None)
    # TODO: Change this from 'None'?
    if searchString != 'None':
        match_query = {"flt" : {"fields" : ["_all", "subject.partial", "language.partial", "partner.partial", "state.partial", "category.partial", "subcategory.partial" , "topic.partial"],
                                "like_text" : searchString
                                }
                       }
    elif partner_uid:
        partner_name = Partner.objects.get(uid = partner_uid).name
        match_query = {"match" : {"partner" :{ "query" : partner_name}}}
    else:
        match_query = {"match_all" : {}}
    query = []
    filter = []
    if language_name == 'All Languages':
        language_name = None
    query = create_query(params, language_name)
    if query:
        filter = {"and" : query}
    order_by = params.get('order_by','-likes')
    offset = int(params.get('offset'))
    limit = int(params.get('limit'))
    order_by = order_by[1:] #removing '-' since it will always be '-'
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices = FACET_INDEX
    conn.refresh(FACET_INDEX)
    q ={"query": {
                  "filtered":{
                              "query" : match_query,
                              "filter" : filter
                              }
                  },
        "facets" : {
                    "facet" :{
                              "terms": {
                                        "fields" : ["language", "partner", "state", "category", "subcategory" , "topic", "subject"], 
                                        "size" : MAX_RESULT_SIZE
                                        }
                              }
                    },
        "sort" : {
                  order_by : {"order" : "desc"}
                  },
        "size" : MAX_RESULT_SIZE
        }
    result_list = []
    try :
        query = json.dumps(q)
        url = "http://localhost:9200/%s/_search" % FACET_INDEX
        response = urllib2.urlopen(url, query)
        result = json.loads(response.read())
        for res in result['hits']['hits']:
            result_list.append(res['_source'])
        facets = json.dumps(result['facets']['facet']['terms'])
        
        resp = json.dumps({"meta": {"limit": str(limit), "next": "", "offset": str(offset), "previous": "null", "total_count": str(len(result_list))},"objects": result_list[offset:offset+limit], "facets" : facets})
        return HttpResponse(resp)
    except Exception, ex:
        return HttpResponse('0')
    
def searchCompletions(request):
    searchString = request.GET.get('searchString')
    maxCount = int(request.GET.get('maxCount'))
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices = COMPLETION_INDEX
    conn.refresh(COMPLETION_INDEX)
    q = {"query" : {
                    "query_string" :{
                                    "fields" : ["searchTerm.partial"],
                                    "query" : searchString
                                    }
                    },
         "facets" : {
                    "facet" :{
                              "terms": {
                                        "fields" : [ "searchTerm"], 
                                        "size" : MAX_RESULT_SIZE
                                        }
                              }
                    },
         "size" : maxCount
        }
    try:
        query = json.dumps(q)
        url = "http://localhost:9200/%s/_search" % COMPLETION_INDEX
        response = urllib2.urlopen(url, query)
        result = json.loads(response.read())
        result_list = []
        done_list = []
        for res in result['hits']['hits']:
            if res['_source']['type'] != "Collections":
                result_list.append(res['_source'])
                res['_source']['count'] = 0
            elif res['_source']['searchTerm'] not in done_list:
                val = str(res['_source']['searchTerm']).lower()
                for term in result['facets']['facet']['terms']:
                    if val == term['term'] :
                        res['_source']['count'] = term['count']
                        done_list.append(res['_source']['searchTerm'])
                result_list.append(res['_source'])
        if len(result_list) == 0:
            result_list.append({"searchTerm" : "No Results"})    # for now just displaying no results when nothing is found in completion
        resp = json.dumps({"responseCode":"OK","requestParameters":{"searchString":searchString,"maxCount":unicode(maxCount)},"completions": result_list, "totalCount": unicode(maxCount)})
        return HttpResponse(resp)
    except Exception, ex:
        return HttpResponse('0')


def get_related_videos(video):
    related_videos = []
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices = VIDEO_INDEX
    conn.refresh(VIDEO_INDEX)
    q = {
        "query": {
                 "bool": {
                           "should": [
                                       {"term"  : { "uid" : video.uid } },
                                       {"terms" : { "category" : [video.category]}},
                                       {"terms" : { "topic" : [video.topic]}},
                                       {"terms" : { "language" : [video.language]}}
                                       ],
                           "minimum_should_match" : 1
                           }
                 }
        }
    try:
        query = json.dumps(q)
        url = "http://localhost:9200/%s/_search" % VIDEO_INDEX
        response = urllib2.urlopen(url, query)
        result = json.loads(response.read())
        for res in result['hits']['hits']:
            related_videos.append(res['_source'])
    except Exception:
        pass
    return related_videos