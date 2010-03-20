from django.conf.urls.defaults import *
from dg.views import *
from django.contrib.auth.views import login, logout
from dg.output.views import *
from django.conf import settings

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
    (r'^feeds/persons/$', feed_person_html_on_person_group),
    (r'^feeds/person_pract/$',feed_person_prac_pg_anim),
	(r'^feeds/persons_village/(\d+)/$', feeds_persons_village),
	(r'^feeds/test/(\d+)/$', test),
	(r'^feeds/test_gwt/(\d+)/$', test_gwt),
#   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
    (r'^hello/$', hello),
	(r'^animators-by-village-id/(\d+)/$', feed_animators),
    (r'/search/', search),
    (r'^dashboard/getkey/$', get_key_for_user),
	(r'^dashboard/login/$', login_view),
    (r'^dashboard/saveregion/$', save_region),
    (r'^dashboard/getregions/$', get_regions),
    (r'^dashboard/savefieldofficer/$', save_fieldofficer),
    (r'^dashboard/getfieldofficers/$', get_fieldofficers),
    (r'^dashboard/savepractice/$', save_practice),
    (r'^dashboard/getpractices/$', get_practices),
    (r'^dashboard/savelanguage/$', save_language),
    (r'^dashboard/getlanguages/$', get_languages),
    (r'^dashboard/savepartner/$', save_partner),
    (r'^dashboard/getpartners/$', get_partners),
    (r'^dashboard/addstates/$', add_state),
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
    (r'^output/test1/(country|state|district|block|village)/(\d+)$',test_output),

    (r'^output/dropdownval/$',overview_drop_down),
    (r'^output/overview/(country|state|district|block|village)/(\d+)/$',overview),
    (r'^output/overview/line/(country|state|district|block|village)/(\d+)/$',overview_line_graph),
    (r'^output/video/module/(country|state|district|block|village)/(\d+)/$',video_module),
    (r'^output/video/mfpie/(country|state|district|block|village)/(\d+)/$',video_pie_graph_mf_ratio),
    (r'^output/video/actorpie/(country|state|district|block|village)/(\d+)/$',video_actor_wise_pie),
    (r'^output/video/typepie/(country|state|district|block|village)/(\d+)/$',video_type_wise_pie),
    (r'^output/video/geogpie/(country|state|district|block|village)/(\d+)/$',video_geog_pie_data),
    (r'^output/video/practicescatter/(country|state|district|block|village)/(\d+)/$',video_practice_wise_scatter),
    (r'^output/video/languagescatter/data/(country|state|district|block|village)/(\d+)/$',video_language_wise_scatter_data),
    (r'^output/video/monthbar/data/(country|state|district|block|village)/(\d+)/$',video_monthwise_bar_data),
    (r'^output/video/monthbar/settings/(country|state|district|block|village)/(\d+)/$',video_monthwise_bar_settings)

)