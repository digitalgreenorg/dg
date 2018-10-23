import ast
import datetime
import json
import random
import urllib2

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import login as django_login_view
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from dg.settings import PERMISSION_DENIED_URL

from elastic_search import get_related_collections, get_related_videos
from social_website.models import  Collection, Partner, FeaturedCollection, Video, ResourceVideo
from videos.models import Practice, Video as Dashboard_Video
from videos.models import Category, SubCategory, Tag, VideoPractice

from mezzanine.blog.models import BlogPost
import logging
class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(label=("Username"), help_text=("Enter Email Address"))


def social_home(request):
    language = Collection.objects.exclude(language = None).values_list('language',flat=True) # only using those languages that have collections
    language = sorted(set(language))
    blog = BlogPost.objects.all()[:3]
    context= {
        'header': {
            'jsController':'Home',
            'currentPage':'Home',
            'loggedIn':False,
            'random':random.randint(0, 1),
             },
        'language':language,
        'blog_posts':blog,
                }
    return render_to_response('home.html', context, context_instance = RequestContext(request))


def collection_view(request, partner, country, state, language, title, video=1):
    try:
        collection = Collection.objects.get(partner__name__iexact = partner, country__iexact = country, state__iexact = state, language__iexact = language, title__iexact = title)
    except Collection.DoesNotExist:
        return HttpResponseRedirect(reverse('discover'))
    try:
        video_index = int(video)
    except (IndexError, AssertionError):
        video_index = 1
    finally:
        video = collection.videoincollection_set.all()[video_index - 1].video
    tags = [x for x in [video.category,video.subcategory,video.topic,video.subtopic,video.subject] if x is not u'']
    duration = sum([v.duration for v in collection.videos.all()])
    related_collections = get_related_collections(collection, collection.featured)
    video_list = [i.video for i in collection.videoincollection_set.all()]
    description = collection.description
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'currentPage':'Discover',
                         'loggedIn':False
                         },
              'is_collection': True,
              'object': collection,
              'video_list': video_list,
              'collection_duration' : duration,
              'video' : video,
              'video_index' : video_index,
              'tags' : tags,
              'related_collections' : related_collections[:4], # restricting to 4 related collections for now
              }
    if collection.featured :
      return render_to_response('featured-collections-view.html' , context, context_instance = RequestContext(request))
    return render_to_response('collections-view.html' , context, context_instance = RequestContext(request))


def picoseekho_view(request, uid=1):
    video_list = [
    {'uid':1,'title':"Using the pico projector for disseminating information",'description':"Using the pico projector for sharing information can make the work of a village resource person or mediators much easier. They can use the device to share videos that convince farmers by describing and demonstrating a practice. Birju, a MRP, gets together a group of mediators under him and helps them to master using the pico projector.",'youtubeID':'7qpSC1P9Fi8'},
    {'uid':2,'title':"Setting up the pico projector",'description':"In this video, Birju emphasizes that the image created by the pico projector must be large and clear, so that all the details in the video are clearly visible to everyone in the room.",'youtubeID':'o1NbQegGCWM'},
    {'uid':3,'title':"Playing a video",'description':"Birju demonstrates the various steps that need to be followed for selecting and playing a specific video. Videos are sometimes loaded on the pico projector. They could also be loaded on external memory such as USB keys or SD cards. Once the external memory device is chosen, the list of videos available on the device can be browsed.",'youtubeID':'011IvbCIfuM'},
    {'uid':4,'title':"Increasing volume and connecting external speakers",'description':"Savita devi points out that viewers should be able to listen to the video as well as they can view it. Birju demonstrates how to increase the sound on a pico projector and attach external speakers if required.",'youtubeID':'xC57bLoWqnI'},
    {'uid':5,'title':"Pausing and rewinding for discussion and repetition",'description':"Birju explains how to pause the video to encourage recall and discussion. Nisar chacha asks how to rewind a video to show certain points again.",'youtubeID':'DAs3Pcr8d68'},
    {'uid':6,'title':"Benefits of following practices",'description':"In conclusion, the group highlights the need to keep the room dark during screening,checking the pico projector and playing the video before people arrive, keeping the picture and sound clear, and pausing and rewinding the video. Following these practices would benefit the rural community members watching a video.",'youtubeID':'7jUv6A9kAKI'}
    ]

    try:
        video_index = int(uid)
    except (IndexError, AssertionError):
        video_index = 1
    video = video_list[video_index-1]
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'currentPage':'Discover',
                         'loggedIn':False
                         },
              'is_collection': True,
              'video_list': video_list,
              'video' : video,
              'video_index' : video_index,
              }
    return render_to_response('pico_seekho.html' , context, context_instance = RequestContext(request))


def disseminationprep_view(request, uid=1):
    video_list = [
    {'uid':1, 'title':"Pre-video dissemination preparation", 'description':"Preparing for the video dissemination beforehand can ensure that the dissemination goes smoothly. They can prepare by watching the video, noting down non-negotiables, charging the equipment and reminding SHG members a day before the dissemination. Abha, an experienced mediator, invites two other new mediators to learn the process from her.", 'youtubeID':'gIKNVu4XTw4'},
    {'uid':2, 'title':"Understanding non-negotiables", 'description':"One of the essential aspects while preparing for dissemination is to understand the non-negotiables. Non-negotiable's are those points that make a practice successful. If a community member does not adopt all the non-negotiables, they may not get the desired results.", 'youtubeID':'EPcb7dbKReM'}
    ]

    try:
        video_index = int(uid)
    except (IndexError, AssertionError):
        video_index = 1
    video = video_list[video_index-1]
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'currentPage':'Discover',
                         'loggedIn':False
                         },
              'is_collection': True,
              'video_list': video_list,
              'video' : video,
              'video_index' : video_index,
              }
    return render_to_response('dissemination_prep.html' , context, context_instance = RequestContext(request))


def disseminationform_view(request, uid=1):
    video_list = [
    {'uid':1, 'title':"Filling the upper-left hand part of the form", 'description':"The mediator fills a form to document which video was shown and who came. The new mediators observe how Abha fills her form and conducts her dissemination. This part explains the upper left hand of the form. This part contains information about the video being shown, the date and time and the groups attending.", 'youtubeID':'rytq0SLzJdw'},
    {'uid':2, 'title':"Filling the upper-right hand part of the form", 'description':"The upper-right hand of the form consists of basic information about the place where the screening is to be conducted, including the village, block and district name.", 'youtubeID':'kAyrh7mj-ig'},
    {'uid':3, 'title':"Filling  member's information", 'description':"One of the more important parts of the form is filling information about the group members who are attending the screening. This part explains how to easily fill this information in the form, specially when there are multiple groups attending the training.", 'youtubeID':'zbB9xzzOcgQ'},
    {'uid':4, 'title':"Conducting dissemination", 'description':"Disseminations conducted by mediators follow a standard procedure, where the mediator welcomes the group members, introduces the video, shows the video, pauses the video in critical places, takes questions from the audience and summarizes the video with the non-negotiables adoption points. At the end of the dissemination, the mediator has to take signature/thumb-print of all the group members who attended the training. This also helps them to later on follow up with those who adopted the practice.", 'youtubeID':'7OG6npRQbiM'}
    ]

    try:
        video_index = int(uid)
    except (IndexError, AssertionError):
        video_index = 1
    video = video_list[video_index-1]
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'currentPage':'Discover',
                         'loggedIn':False
                         },
              'is_collection': True,
              'video_list': video_list,
              'video' : video,
              'video_index' : video_index,
              }
    return render_to_response('dissemination_form.html' , context, context_instance = RequestContext(request))


def adoptionverification_view(request, uid=1):
    video_list = [
    {'uid':1, 'title':"Understanding the adoption verification form", 'description':"Adoption verification part of the form contains information about group members who adopted the practice, when thy adopted the practice and which all non-negotiable points they adopted. Abha explains the two new mediators what each field means.", 'youtubeID':'1LT9xdLFagc'},
    {'uid':2, 'title':"Conducting an adoption verification", 'description':"The filling of the form in a real scenario is demonstrated through Abha and the other two mediators by visiting one of the group members in her field and verifying all the non-negotiable points.", 'youtubeID':'Z5LVB8qTKtc'},
    {'uid':3, 'title':"Adoption verification assessment", 'description':"You can assess your own knowledge of filling the adoption verification form by following the case that is being shown in this part of the video.", 'youtubeID':'55hru37cOuk'}
    ]

    try:
        video_index = int(uid)
    except (IndexError, AssertionError):
        video_index = 1
    video = video_list[video_index-1]
    context= {
              'header': {
                         'jsController':'ViewCollections',
                         'currentPage':'Discover',
                         'loggedIn':False
                         },
              'is_collection': True,
              'video_list': video_list,
              'video' : video,
              'video_index' : video_index,
              }
    return render_to_response('adoption_verification.html' , context, context_instance = RequestContext(request))


def video_view(request, uid):
    try:
        video = Video.objects.get(uid=uid)
    except Video.DoesNotExist:
        return HttpResponseRedirect(reverse('discover'))

    tags = [x for x in [video.category, video.subcategory, video.topic, video.subtopic, video.subject] if x is not u'']
    if Collection.objects.filter(partner=video.partner).count():
        collection = Collection.objects.filter(partner=video.partner)[0]
    else:
        collection = Collection.objects.all()[0]
    related_collections = get_related_collections(collection, False)
    related_videos = get_related_videos(video)
    context = {
               'header': {
                          'jsController':'ViewCollections',
                          'currentPage':'Discover',
                          },
              'is_collection': False,
              'object': video,
              'video_list': related_videos,
              'video' : video,
              'video_index' : 1,
              'tags' : tags,
              'related_collections' : related_collections[:4], # restricting to 4 related collections for now
               }
    return render_to_response('collections-view.html' , context, context_instance = RequestContext(request))


def partner_view(request, partner):
    try:
        partner = Partner.objects.get(name__iexact = partner)
    except Partner.DoesNotExist:
        return HttpResponseRedirect('/videos/library/')
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
    country = request.GET.get('country', None)
    state = request.GET.get('state', None)
    language = request.GET.get('language', None)
    category = request.GET.get('category', None)
    subcategory = request.GET.get('subcategory', None)
    topic = request.GET.get('topic', None)
    subject = request.GET.get('subject', None)
    order = request.GET.get('order_by', None)
    
    context= {
              'header': {
                         'jsController':'Collections',
                         'currentPage':'Discover',
                         'loggedIn'    : False
                         },
              'searchString' : searchString,
              'partner' : partner,
              'title' : title,
              'country': country,
              'state' : state,
              'language' : language,
              'category' : category,
              'subcategory' : subcategory,
              'topic' : topic,
              'subject': subject,
              'order': order,
        }
    return render_to_response('collections.html', context, context_instance=RequestContext(request))

def make_sub_filter(filters, field, active_filter_list, facet_dict, m2m_field=False):
    kwargs = {}
    if m2m_field:
        kwargs[field] = None
    else:
        kwargs[field] = ''
    filters[field] = {}
    filters[field]['title'] = field.title()
    filters[field]['options'] = []
    facet_dict = {k.lower():v for k,v in facet_dict.items()}
    if m2m_field:
        m2m_list = sorted(set([obj[field] for obj in Collection.objects.exclude(**kwargs).values(field)]))
        if field == 'videopractice':
            m2m_values = [item for item in VideoPractice.objects.filter(id__in=m2m_list).values_list('videopractice_name', \
                                            flat=True)]
        elif field == 'tags':
            m2m_values = [item for item in Tag.objects.filter(id__in=m2m_list).values_list('tag_name', \
                                            flat=True)]
        for obj in m2m_values:
            
            facet_count = facet_dict[obj.lower()] if facet_dict.has_key(obj.lower()) else 0
            if facet_count or facet_dict == {}:
                filters[field]['options'].append({"title" : obj,"value" : obj, "filterActive" : obj in active_filter_list,\
                                                "count" : facet_count})
    elif field == 'title':
        for obj in sorted(Collection.objects.exclude(**kwargs).values_list(field, flat=True)): #works same as .exclude(field = '')
            facet_count = facet_dict[obj.lower()] if facet_dict.has_key(obj.lower()) else 0
            if facet_count or facet_dict == {}:
                filters[field]['options'].append({"title" : obj,"value" : obj, "filterActive" : obj in active_filter_list, "count" : facet_count})
        
    else:
        for obj in sorted(set(Collection.objects.exclude(**kwargs).values_list(field, flat=True))): #works same as .exclude(field = '')
            facet_count = facet_dict[obj.lower()] if facet_dict.has_key(obj.lower()) else 0
            if facet_count or facet_dict == {}:
                filters[field]['options'].append({"title" : obj,"value" : obj, "filterActive" : obj in active_filter_list, "count" : facet_count})
    return filters

@csrf_exempt
def searchFilters(request):
    if request.method == 'GET':
        params = request.GET
        facets = params.get('facets', None)
    else:
        params = request.POST
        facets_json = json.loads(request.body)
        facets = facets_json['facets']
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
    country = params.getlist('filters[country][]', None)
    topic = params.getlist('filters[topic][]', None)
    subject = params.getlist('filters[subject][]', None)
    videopractice = params.getlist('filters[videopractice][]', None)
    tags = params.getlist('filters[tags][]', None)
    title = params.getlist('filters[title][]', None)
    filters = {}
    filters['partner'] = {}
    filters['partner']['title'] = 'Partner'
    filters['partner']['options'] = []
    facet_dict = {k.lower():v for k,v in facet_dict.items()}
    for obj in Partner.objects.all().order_by('name'):
        facet_count = facet_dict[obj.name.lower()] if facet_dict.has_key(obj.name.lower()) else 0
        if facet_count or facet_dict == {}:
            filters['partner']['options'].append({"title" : obj.name,"value" : obj.name, "filterActive" : obj.name in partner, "count" : facet_count })

    filters = make_sub_filter(filters, 'category', category, facet_dict)
    filters = make_sub_filter(filters, 'subcategory', subcategory, facet_dict)
    filters = make_sub_filter(filters, 'topic', topic, facet_dict)
    filters = make_sub_filter(filters, 'country', country, facet_dict)
    filters = make_sub_filter(filters, 'state', state, facet_dict)
    filters = make_sub_filter(filters, 'subject', subject, facet_dict)
    filters = make_sub_filter(filters, 'language', language, facet_dict)
    filters = make_sub_filter(filters, 'videopractice', videopractice, facet_dict, True, )
    filters = make_sub_filter(filters, 'tags', tags, facet_dict, True)
    filters = make_sub_filter(filters, 'title', title, facet_dict)
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
        'country': collection.country,
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


def resource_view(request, uid=None):
    resource_object = ResourceVideo.objects.all()
    film_list = resource_object.filter(videoTag='f').order_by('-date')
    testimonial_list = resource_object.filter(videoTag='t').order_by('-date')
    if uid is not None:
        selected_video = resource_object.filter(uid=uid)
        return render_to_response('resources.html' , {'resources':selected_video, 'film_list':film_list, 'testimonial_list':testimonial_list}, context_instance = RequestContext(request))
    try:
        resources = resource_object.order_by('-uid')
    except ResourceVideo.DoesNotExist:
        return HttpResponseRedirect(reverse('about'))

    return render_to_response('resources.html' , {'resources':resources[0:1], 'film_list':film_list, 'testimonial_list':testimonial_list}, context_instance = RequestContext(request))


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


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Collection Czars').count() > 0, login_url=PERMISSION_DENIED_URL)
def collection_edit_view(request, collection):
    try:
        collection = Collection.objects.get(uid=collection)
    except Collection.DoesNotExist:
        return HttpResponseRedirect(reverse('create_collection'))
    collection_videos = [i.video_id for i in collection.videoincollection_set.all()]
    video = Video.objects.all()
    language = video.values_list('language',flat=True)
    language = sorted(set(language))
    partner = Partner.objects.values('name', 'uid')
    partner = sorted(partner)
    state = video.values_list('state',flat=True)
    state = sorted(set(state))
    country = video.values_list('country',flat=True)
    country = sorted(set(country))
    
    context= {
              'header': {
                         'jsController':'CollectionAdd',
                         },
              'collection': collection,
              'collection_videos': collection_videos,
              'language': language,
              'partner' : partner,
              'state' : state,
              'country': country,
              }
    return render_to_response('collection_add.html' , context, context_instance = RequestContext(request))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Collection Czars').count() > 0, login_url=PERMISSION_DENIED_URL)
def collection_add_view(request):
    video = Video.objects.all()
    language = video.values_list('language',flat=True)
    language = sorted(set(language))
    partner = Partner.objects.values('name', 'uid')
    partner = sorted(partner)
    state = video.values_list('state',flat=True)
    state = sorted(set(state))
    country = video.values_list('country',flat=True)
    country = sorted(set(country))

    context= {
              'header': {
                         'jsController':'CollectionAdd',
                         },
              'language': language,
              'partner' : partner,
              'state' : state,
              'country': country,
              }
    return render_to_response('collection_add.html' , context, context_instance = RequestContext(request))


# def mapping(request):
#     practice_dictionary = {}

#     query = Dashboard_Video.objects.values_list('related_practice', flat=True).distinct()
#     for a in Practice.objects.select_related('practice_topic', 'practice_subtopic', 'practice_sector', 'practice_subsector', 'practice_subject').filter(id__in=query).order_by('practice_subtopic').order_by('practice_topic').order_by('practice_subsector').order_by('practice_sector'):

#         if a.practice_sector.name not in practice_dictionary: #sector will be key
#             practice_dictionary[a.practice_sector.name] = {'subject': []}
#         sector_dictionary = practice_dictionary[a.practice_sector.name]
#         if a.practice_subject:
#             subject_list = practice_dictionary[a.practice_sector.name]['subject']
#             if a.practice_subject.name not in subject_list:
#                 subject_list.append(a.practice_subject.name)
#         if a.practice_subsector:
#             if a.practice_subsector.name not in sector_dictionary:
#                 sector_dictionary[a.practice_subsector.name] = {}
#             subsector_dictionary = sector_dictionary[a.practice_subsector.name]
#             if a.practice_topic:
#                 if a.practice_topic.name not in subsector_dictionary:
#                     subsector_dictionary[a.practice_topic.name] = []
#                 topic_list = subsector_dictionary[a.practice_topic.name]
#                 if a.practice_subtopic:
#                     if a.practice_subtopic.name not in topic_list:
#                         topic_list.append(a.practice_subtopic.name)

#     resp = json.dumps({"mapping_dropdown": practice_dictionary})
#     return HttpResponse(resp)



def mapping(request):
    dictionary = {}
    category_obj = Category.objects.all()
    for a in category_obj:
        dictionary[a.category_name]={}
        category_dictionary = dictionary[a.category_name]
        subcategory_obj = SubCategory.objects.filter(category=a.id)
        for b in subcategory_obj:
            if a.category_name:
                if b.subcategory_name not in category_dictionary:
                    category_dictionary[b.subcategory_name] = {}
                subcategory_dictionary = category_dictionary[b.subcategory_name]
                videopractice_obj = VideoPractice.objects.filter(subcategory=b.id)
                for c in videopractice_obj:
                    if b.subcategory_name:
                        if c.videopractice_name not in subcategory_dictionary:
                            subcategory_dictionary[c.videopractice_name] = {}
                        practice_dictionary=subcategory_dictionary[c.videopractice_name]
                        
    dictionary['tags'] = {}
    tags_obj = Tag.objects.filter(is_ap_tag=False)
    for d in tags_obj:
        if d.tag_name not in dictionary['tags']:
            dictionary['tags'][d.tag_name]={}
    
    resp = json.dumps({"mapping_dropdown": dictionary})
    return HttpResponse(resp)


  
def login_view(request, template_name='registration/login.html',
                      redirect_field_name=REDIRECT_FIELD_NAME,
                      authentication_form=AuthenticationForm,
                      current_app=None, extra_context=None):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return django_login_view(request, template_name, redirect_field_name, authentication_form, current_app, extra_context)

def signup_view(request, template_name='social_website/signup.html',
                redirect_field_name=REDIRECT_FIELD_NAME,
                signup_form=CustomUserCreationForm,
                current_app=None, extra_context=None):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":

        form = signup_form(data=request.POST)
        if form.is_valid():
            a = form.save()
            a.email = a.username
            a.save()

            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)

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
