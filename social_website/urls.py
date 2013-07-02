from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from views import social_home, collection_view, partner_view, searchCompletions, searchFilters, elasticSearch, search_view, featuredCollection
from static_site_views import home
from django.conf import settings
from social_website.api import VideoResource, LanguageResource, CountryResource, FarmerResource, ActivityResource, CollectionResource, PartnerResource, InterestsResource, CommentResource, PartnerFarmerResource

video_resource = VideoResource()
language_resource = LanguageResource()
country_resource = CountryResource()
farmer_resource = FarmerResource()
activity_resource = ActivityResource()
collection_resource = CollectionResource()
partner_resource = PartnerResource()
interests_resource = InterestsResource()
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
    (r'^api/', include(language_resource.urls)),
    (r'^api/', include(country_resource.urls)),
    (r'^api/', include(farmer_resource.urls)),
    (r'^api/', include(activity_resource.urls)),
    (r'^api/', include(collection_resource.urls)),
    (r'^api/', include(partner_resource.urls)),
    (r'^api/', include(interests_resource.urls)),
    (r'^api/', include(comment_resource.urls)),
    (r'^api/', include(partnerfarmer_resource.urls)),
    
#    (r'', include(signin_resource.urls)),
#    (r'', include(usercollectionhistory_resource.urls)),
#    (r'', include(videolike_resource.urls)),
#    (r'', include(commentlike_resource.urls)),
#    (r'', include(user_resource.urls)),
#    (r'', include(partnerfarmer_resource.urls)),
#)

#urlpatterns = patterns('',   
    url(r'^main.js$', direct_to_template, {'template': 'main.js', 'mimetype':'text/javascript'}, name='mainjs'),
  #  (r'^$', direct_to_template, {'template': 'home.html', 'extra_context': {'header': {'jsController':'Home', 'loggedIn':False}}}),
    url(r'^discover/?$',search_view, name='search'),
    url(r'^discover/$', direct_to_template, {'template': 'collections.html', 'extra_context': {'header': {'jsController':'Collections', 'currentPage':'Discover', 'loggedIn':False}}}, name='discover'),
    url(r'^collections/?$',collection_view, name='collections'),
    url(r'^about/$', direct_to_template, {'template': 'about.html', 'extra_context': {'header': {'jsController':'About', 'currentPage':'About', 'loggedIn':False}}},name='about'),
    url(r'^connect/$', partner_view,name='connect'),
    url(r'^about/model/$', direct_to_template, {'template': 'model.html', 'extra_context': {'header': {'jsController':'Model', 'currentPage':'Model', 'loggedIn':False}}},name='model'),
    url(r'^donate/$', direct_to_template, {'template': 'donate.html', 'extra_context': {'header': {'jsController':'Donate', 'currentPage':'Donate', 'loggedIn':False}}},name='donate'),
    url(r'^tools/$', direct_to_template, {'template': 'tools.html', 'extra_context': {'header': {'jsController':'Tools', 'currentPage':'Tools', 'loggedIn':False}}},name='tools'),
    url(r'^reports/$', direct_to_template, {'template': 'reports.html', 'extra_context': {'header': {'jsController':'Report', 'currentPage':'Report', 'loggedIn':False}}},name='report'),
    url(r'^reports/1/$', direct_to_template, {'template': 'annualreport09.html', 'extra_context': {'header': {'jsController':'AnnualReport09', 'currentPage':'AnnualReport09', 'loggedIn':False}}},name='annualreport09'),
    url(r'^reports/1/field$', direct_to_template,{'template': 'field-developments-09.html'}),
    url(r'^reports/1/learning$', direct_to_template,{'template': 'learnings-09.html'}),
    url(r'^reports/2/$', direct_to_template, {'template': 'annualreport10.html', 'extra_context': {'header': {'jsController':'AnnualReport10', 'currentPage':'AnnualReport10', 'loggedIn':False}}},name='annualreport10'),
    url(r'^contact/$', direct_to_template, {'template': 'contact.html', 'extra_context': {'header': {'jsController':'Contact', 'currentPage':'Contact', 'loggedIn':False}}},name='contact'),
    url(r'^board/$', direct_to_template, {'template': 'board.html', 'extra_context': {'header': {'jsController':'Board', 'currentPage':'Board', 'loggedIn':False}}},name='board'),
    (r'^$',social_home),
    (r'^api/searchCompletions?$',searchCompletions),
    (r'^api/searchFilters$',searchFilters),
    (r'^api/elasticSearch/$',elasticSearch),
    (r'^api/featuredCollection/$',featuredCollection),
    
)
