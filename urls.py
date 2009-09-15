from django.conf.urls.defaults import *
from dg.views import hello,homepage, current_datetime, hours_ahead, feed_animators, feeds_subcat

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
	(r'^feeds/subcat/(\d+)/$', feeds_subcat),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
    	('^hello/$', hello),
	(r'^animators-by-village-id/(\d+)/$', feed_animators),
	#('^$',homepage),
	#('^time/$',current_datetime),
	#(r'^time/plus/(\d{1,2})/$',hours_ahead),

)

