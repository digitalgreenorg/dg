from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import ast, datetime, json, urllib2
from elastic_search import get_related_collections
from social_website.models import  Collection, Partner, FeaturedCollection

def social_home(request):
    language = Collection.objects.exclude(language = None).values_list('language',flat=True) # only using those languages that have collections 
    language = sorted(set(language))
    context= {
        'header': {
            'jsController':'Home',
            'loggedIn':False
             },
        'language':language,
        }
    return render_to_response('home.html', context, context_instance = RequestContext(request))

def collection_view(request, partner, state, language, title, video=1):
    try:
        collection = Collection.objects.get(partner__name__iexact = partner, state__iexact = state, language__iexact = language, title__iexact = title)
    except Collection.DoesNotExist:
        return HttpResponseRedirect(reverse('discover'))
    try:
        video_index = int(video)
        video = collection.videos.all()[video_index - 1]
    except (IndexError, AssertionError):
        video_index = 1
        video = collection.videos.all()[video_index - 1]    
    tags = [x for x in [video.category,video.subcategory,video.topic,video.subtopic,video.subject] if x is not u'']
    duration = sum([v.duration for v in collection.videos.all()])
    related_collection_dict = get_related_collections(collection)
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'loggedIn':False
                         },
              'collection': collection,
              'duration' : duration,
              'video' : video,
              'video_index' : video_index,
              'tags' : tags,
              'related_collections' : related_collection_dict[:4], # restricting to 4 related collections for now
              }
    return render_to_response('collections-view.html' , context, context_instance = RequestContext(request)) 

def partner_view(request, partner):
    try:
        partner = Partner.objects.get(name__iexact = partner)
    except Partner.DoesNotExist:
        return HttpResponseRedirect(reverse('connect'))
    context= {
        'header': {
            'jsController':'Profile',
            'loggedIn':False},
        'partner': partner,
        }
    return render_to_response('profile.html' , context, context_instance = RequestContext(request))

def search_view(request):
    searchString = request.GET.get('searchString', None)
    partner = request.GET.get('partner', None)
    title = request.GET.get('title', None)
    state = request.GET.get('state', None)
    context= {
              'header': {
                         'jsController':'Collections',
                         'currentPage':'Discover',
                         'loggedIn'    : False
                         },
              'searchString' : searchString,
              'partner' : partner,
              'title' : title,
              'state' : state,
        }
    return render_to_response('collections.html', context, context_instance=RequestContext(request))
    
def make_sub_filter(filters, field, active_filter_list, facet_dict):
    kwargs = {}
    kwargs[field] = ''
    filters[field] = {}
    filters[field]['title'] = field.title()
    filters[field]['options'] = []
    for obj in set(Collection.objects.exclude(**kwargs).values_list(field, flat=True)): #works same as .exclude(field = '')
        facet_count = facet_dict[obj] if facet_dict.has_key(obj) else 0
        if facet_count or facet_dict == {}:
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
    filters['partner'] = {}
    filters['partner']['title'] = 'Partner'
    filters['partner']['options'] = []
    for obj in Partner.objects.all():
        facet_count = facet_dict[obj.name] if facet_dict.has_key(obj.name) else 0
        if facet_count or facet_dict == {}:
            filters['partner']['options'].append({"title" : obj.name,"value" : obj.name, "filterActive" : obj.name in partner, "count" : facet_count })
        
    filters = make_sub_filter(filters, 'category', category, facet_dict)
    filters = make_sub_filter(filters, 'subcategory', subcategory, facet_dict)
    filters = make_sub_filter(filters, 'topic', topic, facet_dict)
    filters = make_sub_filter(filters, 'state', state, facet_dict)
    filters = make_sub_filter(filters, 'subject', subject, facet_dict)
    filters = make_sub_filter(filters, 'language', language, facet_dict)

    data = json.dumps({"categories" : filters})
    return HttpResponse(data)


    
def featuredCollection(request):
    language_name = request.GET.get('language__name', None)
    try:
        featured_collection = FeaturedCollection.objects.get(collection__language=language_name)
    except FeaturedCollection.DoesNotExist:
        featured_collection = FeaturedCollection.objects.get(collection__language="Mundari")
    collection= featured_collection.collection
    collage_url = featured_collection.collageURL
    time = 0
    for video in collection.videos.all():
        time = time + video.duration
    featured_collection_dict = {
        'title': collection.title,
        'state': collection.state,
        'likes': collection.likes,
        'views': collection.views,
        'adoptions': collection.adoptions,
        'language': collection.language,
        'partner_name': collection.partner.name,
        'partner_logo': '' if collection.partner.logoURL._file is None else collection.partner.logoURL,
        'partner_url': '/social/connect/?id='+str(collection.partner.uid),
        'video_count': collection.videos.all().count(),
        'link': '/social/collections/?id=' + str(collection.uid) +'&video=1',
        'collageURL': collage_url,
        'duration': str(datetime.timedelta(seconds=time)),
    }
    resp = json.dumps({"featured_collection": featured_collection_dict})
    return HttpResponse(resp)

def footer_view(request):
    response = urllib2.urlopen('https://graph.facebook.com/digitalgreenorg')
    data = data = json.loads(response.read())
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
