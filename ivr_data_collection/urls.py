from django.conf.urls import patterns, include, url
from views import call_exotel, greeting_view, custom_field_update
 
urlpatterns = patterns('',
    (r'^call/', call_exotel),
    (r'^greeting/',greeting_view),
    (r'^updatecustomfield/',custom_field_update),    

)
