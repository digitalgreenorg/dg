from django.conf.urls.defaults import patterns, url
from views import page, update

urlpatterns = patterns('',
    (r'^page/?$', page),
    (r'^update/?$', update),
)