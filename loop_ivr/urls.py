from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url

from loop_ivr.views import *

urlpatterns = patterns('',
    url(r'^$', home, name='loop_ivr'),
    url(r'^market_info_incoming/',market_info_incoming),
    url(r'^market_info_response/',market_info_response),
    url(r'^crop_price_query/',crop_price_query),
    url(r'^crop_price_sms_content/',crop_price_sms_content),
    )
