from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('coco_proto.views',
                ('^$', direct_to_template, {'template': 'coco_proto/dashboard.html'}),
                url(r'^country/$', 'country_list', name='country_list'),
                url(r'^state/$', 'state_list', name='state_list'),
                url(r'^district/$', 'district_list', name='district_list'),
                url(r'^block/$', 'block_list', name='block_list'),
                url(r'^village/$', 'village_list', name='village_list'),
                       )