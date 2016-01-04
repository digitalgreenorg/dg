from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from tastypie.api import Api
from api import FarmerResource, VillageResource
from loop import views

api = Api(api_name = "v1")
api.register(VillageResource)

urlpatterns = patterns('',
    url(r'^$', views.home, name='loop'),
    (r'^api/', include(api.urls)),
    )