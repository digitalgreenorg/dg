from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('coco_proto.views', 
    ('^offline/$', direct_to_template, {'template': 'coco_proto/dashboard_offline.html'}), 
)
