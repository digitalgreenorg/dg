from django.conf.urls.defaults import patterns, url
from views import save_fb_user

urlpatterns = patterns('',
    url(r'^savefbuser/$', save_fb_user),
)