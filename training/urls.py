from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from dg.base_settings import TRAINING_PAGE

from tastypie.api import Api
from training.api import TrainerResource, LanguageResource, AssessmentResource, QuestionResource, MediatorResource, DistrictResource, VillageResource, PartnerResource, TrainingResource, StateResource, ScoreResource

from views import login, dashboard, graph_data, get_overall_data, get_filter_data

from training.log.training_log import send_updated_log
from training.admin import training_admin

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
    url(r'^login/', login),
    url(r'^api/', include(api.urls)),
    url(r'^dashboard/', dashboard),
    url(r'^graph_data', graph_data),
    url(r'^get_log/', send_updated_log),
    url(r'^getData', get_overall_data),
    url(r'^get_filter_data',get_filter_data),
    url(r'^admin/', include(training_admin.urls)),
    )
