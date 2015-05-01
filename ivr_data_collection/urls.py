from django.conf.urls import patterns, include, url
from views import call_exotel, greeting_view, custom_field_update, screening_question, screening_answer, adoption_question, adoption_answer, nonnegotiable_question, nonnegotiable_answer

urlpatterns = patterns('',
    (r'^call/', call_exotel),
    (r'^greeting/',greeting_view),
    (r'^updatecustomfield/',custom_field_update), 
    (r'^video/screening/question/',screening_question),
    (r'^video/screening/answer/(?P<option>.+)/',screening_answer),

    (r'^video/adoption/question',adoption_question),
    (r'^video/adoption/answer/(?P<option>.+)/',adoption_answer),

    (r'^video/nonnegotiable/question/(?P<num>.+)/',nonnegotiable_question),
    (r'^video/nonnegotiable/answer/(?P<num>.+)/(?P<option>.+)/',nonnegotiable_answer),
 

)
