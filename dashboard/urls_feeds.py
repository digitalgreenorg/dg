from django.conf.urls.defaults import patterns, url
from views import feed_person_html_on_person_group, feed_person_html_on_person_group_modified, \
feed_person_prac_pg_anim, feeds_persons_village, test, test_gwt

urlpatterns = patterns('',
    (r'^persons/$', feed_person_html_on_person_group),
    (r'^persons/modified/$', feed_person_html_on_person_group_modified),
    (r'^person_pract/$', feed_person_prac_pg_anim),
    (r'^persons_village/(\d+)/$', feeds_persons_village),
    (r'^test/(\d+)/$', test),
    (r'^test_gwt/(\d+)/$', test_gwt),
)