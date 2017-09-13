from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from dg.base_settings import PRODUCT_PAGE

from loop_ivr.views import *

from loop_ivr.admin import loop_ivr_admin

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=PRODUCT_PAGE)),
    url(r'^market_info_incoming/',market_info_incoming),
    #url(r'^market_info_response/',market_info_response),
    url(r'^crop_price_query/',crop_price_query),
    url(r'^crop_price_sms_content/',crop_price_sms_content),
    url(r'^push_message_sms_response/',push_message_sms_response),
    (r'^admin/', include(loop_ivr_admin.urls)),
)
