from django.conf.urls.defaults import patterns, url
from views import save_submission

urlpatterns = patterns('',
    url(r'^submission/$', save_submission),
)
