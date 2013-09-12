from django.conf.urls import patterns
from feed.views import DistrictFeed

urlpatterns = patterns('',
    # ...
    (r'^feed/$', DistrictFeed()),
    # ...
)