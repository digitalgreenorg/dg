from django.conf.urls import patterns, url, include
from views import save_submission

from dg.mcoco_admin import mcoco_admin
from dg.base_settings import PRODUCT_PAGE

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=PRODUCT_PAGE)),
    url(r'^submission/$', save_submission),
    (r'^admin/', include(mcoco_admin.urls)),
)
