from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url

from loop_ivr.views import *

urlpatterns = patterns('',
    url(r'^$', home, name='loop_ivr'),
    url(r'^crop_price_query/',crop_price_query),
    )
