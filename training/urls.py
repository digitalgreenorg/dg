from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from tastypie.api import Api
from training.api import TrainerResource, LanguageResource, AssessmentResource, QuestionResource, MediatorResource, DistrictResource, VillageResource, PartnerResource, TrainingResource, StateResource, ScoreResource

from views import login, dashboard, training_wise_data, trainer_wise_data, question_wise_data, mediator_wise_data, filter_data

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
	url(r'^login/', login),
	url(r'^api/', include(api.urls)),
	url(r'^dashboard/', dashboard),
	url(r'^training_wise_data', training_wise_data),
	url(r'^trainer_wise_data', trainer_wise_data),
	url(r'^question_wise_data', question_wise_data),
	url(r'^mediator_wise_data', mediator_wise_data),
	url(r'^filter_data/', filter_data),
	)
