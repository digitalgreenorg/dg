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
    url(r'^market_info_response/',market_info_response),
    url(r'^crop_price_query/',crop_price_query),
    url(r'^crop_price_sms_content/',crop_price_sms_content),
    url(r'^push_message_sms_response/',push_message_sms_response),
    # admin/logout/ should be above admin/ URL
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/loopivr/admin/'}),
    (r'^admin/', include(loop_ivr_admin.urls)),
    url(r'^wrong_code_message/', wrong_code_message),
    url(r'^no_code_message/', no_code_message),
)
