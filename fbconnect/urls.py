from django.conf.urls.defaults import patterns, url
from views import save_fb_user, save_follower

urlpatterns = patterns('',
    url(r'^savefbuser/$', save_fb_user),
    url(r'^savefollower/$', save_follower),
)