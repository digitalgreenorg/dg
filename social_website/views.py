import ast
import datetime
import json
import urllib2

from django.contrib.auth import logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect

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
                         'currentPage':'Discover',
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
            'loggedIn':False,
            'currentPage':'Connect',
            },
        'partner': partner,
        }
    return render_to_response('profile.html', context, context_instance = RequestContext(request))

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
    for obj in sorted(set(Collection.objects.exclude(**kwargs).values_list(field, flat=True))): #works same as .exclude(field = '')
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
    for obj in Partner.objects.all().order_by('name'):
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
    featured_collections = FeaturedCollection.objects.filter(collection__language=language_name, show_on_language_selection=True).order_by('-uid')
    if len(featured_collections) == 0:
        featured_collections = FeaturedCollection.objects.filter(collection__language=language_name).order_by('-uid')
        if len(featured_collections) == 0:
            # This code should be triggered on
            # homepage without language selection
            # language sent is all_languages or None
            # there is no featured collection with the chosen language
            featured_collections = FeaturedCollection.objects.filter(show_on_homepage = True).order_by('-uid')
            if len(featured_collections) == 0:
                featured_collections = FeaturedCollection.objects.all().order_by('-uid')
    featured_collection = featured_collections[0]
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
        'partner_logo': collection.partner.logoURL.url,
        'partner_url': collection.partner.get_absolute_url(),
        'video_count': collection.videos.all().count(),
        'link': collection.get_absolute_url(),
        'collageURL': collage_url.url,
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


def logout_view(request):
    next_url = request.GET.get('next', None)
    logout(request)
    return HttpResponseRedirect(next_url)


@csrf_protect
def signup_view(request, template_name='social_website/signup.html',
                redirect_field_name=REDIRECT_FIELD_NAME,
                signup_form=UserCreationForm,
                current_app=None, extra_context=None):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = signup_form(data=request.POST)
        if form.is_valid():
            a = form.save()
            a.email = a.username
            a.save()
            return HttpResponseRedirect(redirect_to)
    else:
        form = signup_form(None)

    context = {
        'form': form,
    }

    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
