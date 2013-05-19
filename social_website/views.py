import datetime

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import *
from social_website.models import Language, Collection, Partner


def social_home(request):
    language=Language.objects.all().values_list('name',flat=True)
    language=list(language)
    featured_collection=Collection.objects.get(uid=1)
    time=0
    vid_thumbnails=[]
    for vid in featured_collection.videos.all():
        time=time+vid.duration
        vid_thumbnails.append(vid.thumbnailURL)
    featured_collection_dict={'thumbnail':vid_thumbnails[:5],'thumbnail_default':vid_thumbnails[0],'title':featured_collection.title,'state':featured_collection.state,'country':featured_collection.country.countryName,'likes':featured_collection.likes,'views':featured_collection.views,'adoptions':featured_collection.adoptions,'language':featured_collection.language.name,'partner_name':featured_collection.partner.name,'partner_logo':featured_collection.partner.logoURL,'video_count':featured_collection.videos.all().count(),'duration':str(datetime.timedelta(seconds=time))}
    context= {'header': {'jsController':'Home', 'loggedIn':False},'language':language,'featured_collection':featured_collection_dict}
    return render_to_response('home.html' , context,context_instance = RequestContext(request))

def collection_view(request):
    id = request.GET.get('id', None)
    if id:
         collection_uid=id
    collection=Collection.objects.get(uid=id)
    time=0
    online_likes=0
    online_views=0
    videos=collection.videos.all()
    for vid in videos:
        time=time+vid.duration
        online_likes=online_likes+vid.onlineLikes
        online_views=online_views+vid.onlineViews
    collection_dict={'title':collection.title,'state':collection.state,'country':collection.country.countryName,'online_likes':online_likes,'offline_likes':collection.likes-online_likes,'online_views':online_views,'offline_views':collection.views-online_views,'adoptions':collection.adoptions,'language':collection.language.name,'partner_name':collection.partner.name,'partner_logo':collection.partner.logoURL,'video_count':collection.videos.all().count(),'duration':str(datetime.timedelta(seconds=time)),'partner_collections':collection.partner.collectionCount,'partner_year':collection.partner.joinDate.year}
    context= {'header': {'jsController':'ViewCollections', 'loggedIn':False},'collection':collection_dict,'videos':videos}
    return render_to_response('collections-view.html' , context,context_instance = RequestContext(request))

def partner_view(request):
    id = request.GET.get('id', None)
    if id:
         partner_uid=id
    partner=Partner.objects.get(uid=id)
    partner_dict={'name':partner.name,'joinyear':partner.joinDate.year,'description':partner.description,'videos':partner.videos,'views':partner.views,'likes':partner.likes,'adoptions':partner.adoptions,'logoURL':partner.logoURL}
    context= {'header': {'jsController':'ViewCollections', 'loggedIn':False},'partner':partner_dict}
    return render_to_response('profile.html' , context,context_instance = RequestContext(request))