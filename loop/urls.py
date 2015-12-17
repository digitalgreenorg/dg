from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from tastypie.api import Api
from api import UploadResource
from loop import views

api = Api(api_name = "v1")
api.register(UploadResource())

urlpatterns = patterns('',
    url(r'^$', views.home, name='loop'),
    (r'^api/', include(api.urls)),
    )