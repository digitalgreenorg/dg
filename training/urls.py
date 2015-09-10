from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from tastypie.api import Api
from training.api import TrainerResource, LanguageResource, AssessmentResource, QuestionResource, TranslationResource
from views import login

api = Api(api_name = "v1")
api.register(TrainerResource())
api.register(LanguageResource())
api.register(AssessmentResource())
api.register(QuestionResource())
api.register(TranslationResource())


urlpatterns = patterns('',
	(r'^login/', login),
	(r'^api/', include(api.urls)),
	)
