from django.conf.urls import patterns, url
from views import save_submission

urlpatterns = patterns('',
    url(r'^submission/$', save_submission),
)
