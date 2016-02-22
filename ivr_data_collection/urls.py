from django.conf.urls import patterns, include, url
from views import greeting_view, screening_question, screening_answer, adoption_question, adoption_answer, nonnegotiable_question, nonnegotiable_answer, thanks_view

urlpatterns = patterns('',
    (r'^greeting/',greeting_view),
    (r'^video/screening/',screening_question),
    (r'^video/screening/answer/(?P<option>.+)/',screening_answer),

    (r'^video/adoption/question',adoption_question),
    (r'^video/adoption/answer/(?P<option>.+)/',adoption_answer),

    (r'^video/nonnegotiable/question/(?P<num>.+)/',nonnegotiable_question),
    (r'^video/nonnegotiable/answer/(?P<num>.+)/(?P<option>.+)/',nonnegotiable_answer),
    (r'^thanks/',thanks_view),
)
