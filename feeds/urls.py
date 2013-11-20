from django.conf.urls import patterns
from feeds.views import CombinedDistrictFeed, IndividualDistrictFeed

urlpatterns = patterns('',
    (r'^feed/$', CombinedDistrictFeed()),
    (r'^feed/(?P<district_id>\d+)/$', IndividualDistrictFeed()),
)
