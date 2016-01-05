from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import FarmerResource, VillageResource, LoopUserResource
from loop.views import *

api = Api(api_name = "v1")
api.register(VillageResource())
api.register(LoopUserResource())
api.register(FarmerResource())

urlpatterns = patterns('',
    url(r'^$', home, name='loop'),
    (r'^api/', include(api.urls)),
    url(r'^login/', login),
    )