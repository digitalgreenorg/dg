from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from dg.base_settings import TRAINING_PAGE, TRAINING_APP_PAGE

from tastypie.api import Api
from training.api import TrainerResource, LanguageResource, AssessmentResource, QuestionResource, MediatorResource, DistrictResource, VillageResource, PartnerResource, TrainingResource, StateResource, ScoreResource

from views import login, dashboard, graph_data, get_overall_data, get_filter_data

from training.log.training_log import send_updated_log
from training.admin import training_admin

from social_website.views import picoseekho_view, disseminationprep_view, disseminationform_view, adoptionverification_view

api = Api(api_name = "v1")
api.register(TrainerResource())
api.register(TrainingResource())
api.register(LanguageResource())
api.register(AssessmentResource())
api.register(QuestionResource())
api.register(MediatorResource())
api.register(DistrictResource())
api.register(VillageResource())
api.register(PartnerResource())
api.register(StateResource())
api.register(ScoreResource())

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=TRAINING_PAGE)),
    url(r'^app/', RedirectView.as_view(url=TRAINING_APP_PAGE)),
    url(r'^login/', login),
    url(r'^api/', include(api.urls)),
    url(r'^analytics/', dashboard),
    url(r'^graph_data', graph_data),
    url(r'^get_log/', send_updated_log),
    url(r'^getCardGraphData', get_overall_data),
    url(r'^get_filter_data',get_filter_data),
    # admin/logout/ should be above admin/ URL
    url(r'^admin/logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/training/admin/'}),
    url(r'^admin/', include(training_admin.urls)),
    url(r'^courseware/$', TemplateView.as_view(template_name='training_hi.html'), name='training'),
    url(r'^courseware/en/$', TemplateView.as_view(template_name='training_en.html'), name='training-el'),
    url(r'^courseware/hi/$', TemplateView.as_view(template_name='training_hi.html'), name='training-hi'),
    url(r'^courseware/fr/$', TemplateView.as_view(template_name='training_fr.html'), name='training-fr'),
    url(r'^courseware/picoseekho/(?P<uid>.+)/$', picoseekho_view, name='picoseekho'),
    url(r'^courseware/picoseekho/$', picoseekho_view, name='picoseekho'),
    url(r'^courseware/dissemination_prep/(?P<uid>.+)/$', disseminationprep_view, name='disseminationprep'),
    url(r'^courseware/dissemination_prep/$', disseminationprep_view, name='disseminationprep'),
    url(r'^courseware/dissemination_form/(?P<uid>.+)/$', disseminationform_view, name='disseminationform'),
    url(r'^courseware/dissemination_form/$', disseminationform_view, name='disseminationform'),
    url(r'^courseware/adoption_verification/(?P<uid>.+)/$', adoptionverification_view, name='adoptionverification'),
    url(r'^courseware/adoption_verification/$', adoptionverification_view, name='adoptionverification'),
    )
