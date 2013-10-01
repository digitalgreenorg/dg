from django.conf.urls import patterns
from feed.views import CombinedDistrictFeed, IndividualDistrictFeed

urlpatterns = patterns('',
    # ...
    (r'^feed/$', CombinedDistrictFeed()),
    (r'^feed/(?P<district_id>\d+)/$', IndividualDistrictFeed()),
    # ...
)