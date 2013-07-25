from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import social_home, collection_view, partner_view, searchFilters, search_view, featuredCollection
from elastic_search import get_collections_from_elasticsearch, searchCompletions
from django.conf import settings
from social_website.api import VideoResource, PersonResource, ActivityResource, CollectionResource, PartnerResource, CommentResource, PartnerFarmerResource

video_resource = VideoResource()
farmer_resource = PersonResource()
activity_resource = ActivityResource()
collection_resource = CollectionResource()
partner_resource = PartnerResource()
comment_resource = CommentResource()
partnerfarmer_resource = PartnerFarmerResource()

## following added for user based information
#signin_resource = SignInResource()
#usercollectionhistory_resource = UserCollectionHistoryResource()
#videolike_resource = VideoLikeResource()
#commentlike_resource = CommentLikeResource()
#user_resource = UserResource()

urlpatterns = patterns('',
    (r'^api/', include(video_resource.urls)),
    (r'^api/', include(farmer_resource.urls)),
    (r'^api/', include(activity_resource.urls)),
    (r'^api/', include(collection_resource.urls)),
    (r'^api/', include(partner_resource.urls)),
    (r'^api/', include(comment_resource.urls)),
    (r'^api/', include(partnerfarmer_resource.urls)),
    (r'^api/searchCompletions?$',searchCompletions),
    (r'^api/searchFilters$', searchFilters),
    (r'^api/elasticSearch/$', get_collections_from_elasticsearch),
    (r'^api/featuredCollection/$', featuredCollection),
        
#    (r'', include(signin_resource.urls)),
#    (r'', include(usercollectionhistory_resource.urls)),
#    (r'', include(videolike_resource.urls)),
#    (r'', include(commentlike_resource.urls)),
#    (r'', include(user_resource.urls)),
#    (r'', include(partnerfarmer_resource.urls)),
#)

#urlpatterns = patterns('',
    url(r'^$', social_home), 
    url(r'^collections/?$', collection_view, name='collections'),
    url(r'^discover/?$', search_view, name='search'),
    url(r'^discover/$', direct_to_template, {'template': 'collections.html', 'extra_context': {'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}}, name='discover'),
    url(r'^about/$', direct_to_template, {'template':'about.html', 'extra_context':{'header':{'currentPage':'About'}}}, name='about'),
    url(r'^about/ourwork/$', direct_to_template, {'template': 'our_work.html'}, name='ourwork'),
    url(r'^board/$', direct_to_template, {'template': 'board.html'}, name='board'),
    url(r'^careers/$', direct_to_template, {'template': 'career.html'}, name='career'),
    # TODO: Connect needs to be fixed.
    url(r'^connect/$', partner_view, name='connect'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html'}, name='contact'),
    url(r'^donate/$', direct_to_template, {'template': 'donate.html'}, name='donate'),
    url(r'^example/$', direct_to_template,{'template':'example1.html'}),
    url(r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}, name='mainjs'),
    url(r'^reports/1/$', direct_to_template, {'template': 'annualreport09.html'}, name='annualreport09'),
    # TODO: There are no names used below
    url(r'^reports/1/field$', direct_to_template,{'template': 'field-developments-09.html'}),
    url(r'^reports/1/learning$', direct_to_template,{'template': 'learnings-09.html'}),
    url(r'^resources/$', direct_to_template, {'template': 'resources.html'}, name='resources'),
    url(r'^tools/$', direct_to_template, {'template': 'tools.html', 'extra_context': {'header': {'currentPage':'Tools'}}}, name='tools'),
    

)
