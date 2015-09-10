from functools import partial

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import ModelForm
from django.forms.models import model_to_dict, ModelChoiceField

from models import Trainer, Assessment, Question, Translation, Training, Score
from videos.models import Language
from tastypie import fields
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource
from people.models import Animator

from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication

class TrainerResource(ModelResource):
	language = fields.ForeignKey('training.api.LanguageResource', 'language')
	class Meta:
		resource_name = 'trainer'
		queryset = Trainer.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

class LanguageResource(ModelResource):
	class Meta:
		resource_name = 'language'
		queryset = Language.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

# class MediatorResource(ModelResource):
# 	class Meta:
# 		resource_name = 'mediator'
# 		queryset = Animator.objects.all()
# 		authentication = ApiKeyAuthentication()
# 		authorization = Authorization()

class AssessmentResource(ModelResource):
	class Meta:
		resource_name = 'assessment'
		queryset = Assessment.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

class QuestionResource(ModelResource):
	assessment = fields.ForeignKey('training.api.AssessmentResource', 'assessment')
	class Meta:
		resource_name = 'question'
		queryset = Question.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

class TranslationResource(ModelResource):
	question = fields.ForeignKey('training.api.QuestionResource', 'question')
	class Meta:
		resource_name = 'translation'
		queryset = Question.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

# class TrainingResource(ModelResource):
# 	language = fields.ForeignKey('training.api.LanguageResource', 'language')
# 	state = fields.ForeignKey('training.api.StateResource', 'state')
