from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from views import save_submission

from dg.mcoco_admin import mcoco_admin
from dg.base_settings import PRODUCT_PAGE

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=PRODUCT_PAGE)),
    url(r'^submission/$', save_submission),
    # admin/logout/ should be above admin/ URL
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/dimagi/admin/'}),
    (r'^admin/', include(mcoco_admin.urls)),
)
