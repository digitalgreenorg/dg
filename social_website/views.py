import datetime

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import *
from social_website.models import Language, Collection, Partner, FeaturedCollection
from pyes import *
import ast, json, urllib2

MAX_RESULT_SIZE = 500 # max hits for elastic, default is 10

def social_home(request):
    language=Collection.objects.exclude(language = None).values_list('language__name',flat=True) # only using those languages that have collections 
    language=list(set(language))
    language = sorted(language) # setting them in alphabetical order
    fcollection_uid=34
    featured_collection=Collection.objects.get(uid=fcollection_uid)
    time=0
    vid_thumbnails=[]
    for vid in featured_collection.videos.all():
        time=time+vid.duration
        vid_thumbnails.append(vid.thumbnailURL)
    featured_collection_dict={
        'thumbnail':vid_thumbnails[:5],
        'thumbnail_default':vid_thumbnails[0],
        'title':featured_collection.title,
        'state':featured_collection.state,
        'country':featured_collection.country.countryName,
        'likes':featured_collection.likes,
        'views':featured_collection.views,
        'adoptions':featured_collection.adoptions,
        'language':featured_collection.language.name,
        'partner_name':featured_collection.partner.name,
        'partner_logo':featured_collection.partner.logoURL,
        'partner_url':'/social/connect/?id='+str(featured_collection.partner.uid),
        'video_count':featured_collection.videos.all().count(),
        'duration':str(datetime.timedelta(seconds=time)),
        'link':'/social/collections/?id='+ str(fcollection_uid)+'&video=1'
        }
    context= {
        'header': {
            'jsController':'Home',
             'loggedIn':False
             },
        'language':language,
#         'featured_collection':featured_collection_dict
        }
    
    return render_to_response('home.html' , context,context_instance = RequestContext(request))

def collection_view(request):
    id = request.GET.get('id', 1)
    videoID= request.GET.get('video', 1)
    if id:
         collection_uid=id
    collection=Collection.objects.get(uid=id)
    time=0
    online_likes=0
    online_views=0
    videos=collection.videos.all()
    video_info=[]
    i=1
    for vid in videos:
        if i==int(videoID):
            tag_list=[vid.sector,vid.subsector,vid.topic,vid.subtopic,vid.subject]
            tag_list=list(set(tag_list))
            if '' in tag_list:
                tag_list.remove('')
            video_dict={
                'uid' : vid.uid,
                'videoID' : int(videoID),
                'title' : vid.title,
                'description' : vid.description,
                'youtubeID' : vid.youtubeID,
                'tags' : vid.tags,
                'date' : vid.date,
                'tags' : tag_list
                }
        i=i+1
        time=time+vid.duration
        online_likes=online_likes+vid.onlineLikes
        online_views=online_views+vid.onlineViews
        video_info.append([vid.title,vid.thumbnailURL16by9,str(datetime.timedelta(seconds=vid.duration))[2:]])
    collection_dict={
        'uid':collection.uid,
        'title':collection.title,
        'state':collection.state,
        'country':collection.country.countryName,
        'online_likes':online_likes,
        'offline_likes':collection.likes-online_likes,
        'online_views':online_views,
        'offline_views':collection.views-online_views,
        'adoptions':collection.adoptions,
        'language':collection.language.name,
        'partner_name':collection.partner.name,
        'partner_logo':collection.partner.logoURL,
        'video_count':collection.videos.all().count(),
        'duration':str(datetime.timedelta(seconds=time)),
        'partner_collections':collection.partner.collectionCount,
        'partner_year':collection.partner.joinDate.year
        }
    related_collection_dict = []
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices="test2"
    conn.refresh("test2")
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
        response = urllib2.urlopen('http://localhost:9200/test2/_search',query)
        result = json.loads(response.read())
        for res in result['hits']['hits']:
            related_collection_dict.append({"uid" : res['_source']['uid'], 
                                            "title" : res['_source']['title'], 
                                            "partner" : res['_source']['partner']['name'],
                                            "language" : res['_source']['language']['name'],
                                            "state" : res['_source']['state'],
                                            "thumbnailURL" : res['_source']['thumbnailURL'],
                                            "likes" : res['_source']['likes'],
                                            "views" : res['_source']['views'],
                                            "adoptions" : res['_source']['adoptions'],
                                            "duration" : str(datetime.timedelta(seconds=res['_source']['duration'])),
                                            "vid_count" : len(res['_source']['videos']),
                                            })
    except Exception, ex:
        pass
    context= {
        'header': {
            'jsController':'ViewCollections',
            'loggedIn':False
             },
        'collection':collection_dict,
        'videos':video_info,
        'video':video_dict,
        'slides':range(((len(videos)-1)/5)+1),
        'related_collections' : related_collection_dict[:4], # restricting to 4 related collections for now
        }
    return render_to_response('collections-view.html' , context,context_instance = RequestContext(request))

def partner_view(request):
    id = request.GET.get('id', None)
    if id:
         partner_uid=id
    partner=Partner.objects.get(uid=id)
    partner_dict={
        'uid':partner.uid,
        'name':partner.name,
        'joinyear':partner.joinDate.year,
        'description':partner.description,
        'videos':partner.videos,
        'views':partner.views,
        'likes':partner.likes,
        'adoptions':partner.adoptions,
        'logoURL':partner.logoURL,
        }
    context= {
        'header': {
            'jsController':'Profile',
            'loggedIn':False},
        'partner':partner_dict
        }
    return render_to_response('profile.html' , context,context_instance = RequestContext(request))

def search_view(request):
    searchString = request.GET.get('searchString')
    context= {
              'header': {
                         'jsController':'Collections',
                         'currentPage':'Discover',
                         'loggedIn'    : False
                         },
              'searchString': searchString
        }
    return render_to_response('collections.html', context, context_instance=RequestContext(request))
    

def searchCompletions(request):
    searchString = request.GET.get('searchString')
    maxCount = int(request.GET.get('maxCount'))
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices="test-index"
    conn.refresh("test-index")
    q = {"query" : {
                    "query_string" :{
                                    "fields" : ["searchTerm.partial"],
                                    "query" : searchString
                                    }
                    },
         "size" : maxCount
        }
    try:
        query = json.dumps(q)
        response = urllib2.urlopen('http://localhost:9200/test-index/_search',query)
        result = json.loads(response.read())
        result_list = []
        for res in result['hits']['hits']:
            result_list.append(res['_source'])
        if len(result_list) == 0:
            result_list.append({"searchTerm" : "No Results"})    # for now just displaying no results when nothing is found in completion
        resp = json.dumps({"responseCode":"OK","requestParameters":{"searchString":searchString,"maxCount":unicode(maxCount)},"completions": result_list, "totalCount": unicode(maxCount)})
        return HttpResponse(resp)
    except Exception, ex:
        return HttpResponse('0')

def make_sub_filter(filters, field, active_filter_list, facet_dict):
    kwargs = {}
    kwargs[field] = ''
    filters[field] = {}
    filters[field]['title'] = field.title()
    filters[field]['options'] = []
    for obj in set(Collection.objects.exclude(**kwargs).values_list(field, flat=True)): #works same as .exclude(field = '')
        facet_count = facet_dict[obj] if facet_dict.has_key(obj) else 0
        if facet_count:
            filters[field]['options'].append({"title" : obj,"value" : obj, "filterActive" : obj in active_filter_list, "count" : facet_count})
    return filters

def searchFilters(request):
    params = request.GET
    facets = params.get('facets', None)
    facet_dict = {}
    if facets:
        facet_dict = {}
        facets = ast.literal_eval(facets)
        for row in facets:
            facet_dict[row['term']] = int(row['count']) 
        
    language = params.getlist('filters[language][]', None)
    subcategory = params.getlist('filters[subcategory][]', None)
    category = params.getlist('filters[category][]', None)
    partner = params.getlist('filters[partner][]', None)
    state = params.getlist('filters[state][]', None)
    topic = params.getlist('filters[topic][]', None)
    subject = params.getlist('filters[subject][]', None)
    
    filters = {}
    filters['language'] = {}
    filters['language']['title'] = 'Language'
    filters['language']['options'] = []
    for obj in Language.objects.all():
        facet_count = facet_dict[obj.name] if facet_dict.has_key(obj.name) else 0
        if facet_count:
            filters['language']['options'].append({"title" : obj.name,"value" : obj.name, "filterActive" : obj.name in language, "count" : facet_count })
            
    filters['partner'] = {}
    filters['partner']['title'] = 'Partner'
    filters['partner']['options'] = []
    for obj in Partner.objects.all():
        facet_count = facet_dict[obj.name] if facet_dict.has_key(obj.name) else 0
        if facet_count:
            filters['partner']['options'].append({"title" : obj.name,"value" : obj.name, "filterActive" : obj.name in partner, "count" : facet_count })
        
    filters = make_sub_filter(filters, 'category', category, facet_dict)
    filters = make_sub_filter(filters, 'subcategory', subcategory, facet_dict)
    filters = make_sub_filter(filters, 'topic', topic, facet_dict)
    filters = make_sub_filter(filters, 'state', state, facet_dict)
    filters = make_sub_filter(filters, 'subject', subject, facet_dict)

    data = json.dumps({"categories" : filters})
    return HttpResponse(data)

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
        query.append({"terms":{"language_name" : language}})
    elif language_name:
        query.append({"terms":{"language_name" : [language_name]}})
    if subcategory:
        query.append({"terms":{"subcategory" : subcategory}})
    if category:
        query.append({"terms":{"category" : category}})
    if partner:
        query.append({"terms":{"partner_name" : partner}})
    if state:
        query.append({"terms":{"state" : state}})
    if topic:
        query.append({"terms":{"topic" : topic}})
    if subject:
        query.append({"terms":{"subject" : subject}})
    return query

def elasticSearch(request):
    params = request.GET
    language_name = params.get('language__name', None)
    searchString = params.get('searchString', 'None')
    if searchString != 'None':
        match_query = {"match" : {"_all":{"query":searchString}}}
    else:
        match_query = {"match_all" : {}}
    query = []
    filter = []
    if language_name == 'All Languages':
        language_name = None
    query = create_query(params, language_name)
    if query:
        filter = {"and" : query}
    order_by = params.get('order_by')
    offset = int(params.get('offset'))
    limit = int(params.get('limit'))
    order_by = order_by[1:] #removing '-' since it will always be '-'
    conn = ES(['127.0.0.1:9200'])
    conn.default_indices="test2"
    conn.refresh("test2")
    q ={"query": {
                  "filtered":{
                              "query" : match_query,
                              "filter" : filter
                              }
                  },
        "facets" : {
                    "facet" :{
                              "terms": {
                                        "fields" : ["language_name", "partner_name", "state", "category", "subcategory" , "topic", "subject"], 
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
        response = urllib2.urlopen('http://localhost:9200/test2/_search',query)
        result = json.loads(response.read())
        for res in result['hits']['hits']:
            result_list.append(res['_source'])
        facets = json.dumps(result['facets']['facet']['terms'])
        
        resp = json.dumps({"meta": {"limit": str(limit), "next": "", "offset": str(offset), "previous": "null", "total_count": str(len(result_list))},"objects": result_list[offset:offset+limit], "facets" : facets})
        return HttpResponse(resp)
    except Exception, ex:
        return HttpResponse('0')
    
def featuredCollection(request):
    params = request.GET
    language_name = params.get('language__name', None)
    featured_collection = FeaturedCollection.objects.get(language__name=language_name)
    collection_uid = featured_collection.collection
    collage_url = featured_collection.collageURL
    collection = Collection.objects.get(uid=collection_uid)
    time=0
    for vid in collection.videos.all():
        time=time+vid.duration
    featured_collection_dict={
        'title':collection.title,
        'state':collection.state,
        'country':collection.country.countryName,
        'likes':collection.likes,
        'views':collection.views,
        'adoptions':collection.adoptions,
        'language':collection.language.name,
        'partner_name':collection.partner.name,
        'partner_logo':collection.partner.logoURL,
        'partner_url':'/social/connect/?id='+str(collection.partner.uid),
        'video_count':collection.videos.all().count(),
        'link':'/social/collections/?id='+collection_uid +'&video=1',
        'collageURL':collage_url,
        'duration':str(datetime.timedelta(seconds=time)),
        }
    resp = json.dumps({"featured_collection":featured_collection_dict})
    return HttpResponse(resp)

def footer_view(request):
    response = urllib2.urlopen('https://graph.facebook.com/digitalgreenorg')
    data = data = json.loads(res.read())
    footer_dict={
        'likes':data['likes'],
        }
    context= {
        'header': {
            'jsController':'Footer',
            'loggedIn':False},
        'footer_dict':footer_dict
        }
    return render_to_response('footer.html' , context,context_instance = RequestContext(request))
