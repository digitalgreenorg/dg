from django.conf.urls.defaults import *
from dg.views import *
from django.contrib.auth.views import login, logout
from dg.output.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^dg/', include('dg.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
        (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^ajax_filtered_fields/', include('ajax_filtered_fields.urls')),
	(r'^feeds/animators/(\d+)/$', feeds_animators),
	(r'^feeds/groups/(\d+)/$', feeds_groups),
	(r'^feeds/persons/(\d+)/$', feeds_persons),
	(r'^feeds/persons_village/(\d+)/$', feeds_persons_village),
	(r'^feeds/test/(\d+)/$', test),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
    	(r'^hello/$', hello),
	(r'^animators-by-village-id/(\d+)/$', feed_animators),
        (r'/search/', search),
	(r'^dashboard/language/add/$', add_language),
	(r'^dashboard/languages/(?P<language>[^/]+)/$',language),
	(r'^dashboard/region/add/$',add_region),
	(r'^dashboard/regions/$',region),
	(r'^dashboard/state/add/$',add_state),
	(r'^dashboard/states/$',state),
	(r'^dashboard/district/add/$', add_district),
	(r'^dashboard/districts/$', district),
	(r'^dashboard/block/add/$', add_block),
	(r'^dashboard/blocks/$', block),
	(r'^dashboard/persongroup/add/$', add_person_group),
	(r'^dashboard/persongroups/$', person_group),
	(r'^dashboard/developmentmanager/add/$', add_development_manager),
	(r'^dashboard/developmentmanagers/$', development_manager),
	(r'^dashboard/animatorassignedvillage/add/$', add_animator_assigned_village),
	(r'^dashboard/animatorassignedvillages/$', animator_assigned_village),
	(r'^dashboard/animator/add/$', add_animator),
	(r'^dashboard/animators/$', animator),
	(r'^dashboard/fieldofficer/add/$', add_field_officer),
	(r'^dashboard/fieldofficers/$', field_officer),
	(r'^dashboard/partner/add/$', add_partner),
	(r'^dashboard/partners/$', partner),
	(r'^dashboard/person/add/$', add_person),
	(r'^dashboard/persons/$', person),
	(r'^dashboard/practice/add/$', add_practice),
	(r'^dashboard/practices/$', practice),
	(r'^dashboard/village/add/$', add_village),
	(r'^dashboard/villages/$', village),
	(r'^dashboard/video/add/$', add_video),
	(r'^dashboard/videos/', video),
	(r'^dashboard/screening/add/$', add_screening),
	(r'^dashboard/screenings/$', screening),
	(r'^dashboard/login/$', login),
	(r'^dashboard/logout/$', logout),
    (r'^output/overview_flash_state/$',overview_flash_state),
    (r'^output/test1/$',test_output),
    (r'^output/state_overview/$',state_overview),
    (r'^output/state/(\d+)/$',district_overview),
    (r'^output/district/(\d+)/$',block_overview),
    (r'^output/block/(\d+)/$',village_overview),
	#('^$',homepage),
	#('^time/$',current_datetime),
	#(r'^time/plus/(\d{1,2})/$',hours_ahead),

)

