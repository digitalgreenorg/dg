from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url

from loop_ivr.views import *

urlpatterns = patterns('',
    url(r'^$', home, name='loop_ivr'),
    url(r'^crop_price_incoming/',crop_price_incoming),
    url(r'^crop_price_query/',crop_price_query),
    url(r'^crop_price_sms_content/',crop_price_sms_content),
    )
