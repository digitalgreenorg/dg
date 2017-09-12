from django.conf.urls import patterns, url
from views import save_submission

from dg.mcoco_admin import mcoco_admin

urlpatterns = patterns('',
    url(r'^submission/$', save_submission),
    (r'^admin/', include(mcoco_admin.urls)),
)
