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


def many_to_many_to_subfield(bundle, field_name, sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values(*sub_field_names)
    return list(sub_fields)

def foreign_key_to_id(bundle, field_name,sub_field_names):
    field = getattr(bundle.obj, field_name)
    if(field == None):
        dict = {}
        for sub_field in sub_field_names:
            dict[sub_field] = None 
    else:
        dict = model_to_dict(field, fields=sub_field_names, exclude=[])
    return dict

def dict_to_foreign_uri(bundle, field_name, resource_name=None):
    field_dict = bundle.data.get(field_name)
    if field_dict.get('id'):
        bundle.data[field_name] = "/training/api/v1/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle

def dict_to_foreign_uri_m2m(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/training/api/v1/%s/%s/"%(resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle

def dict_to_foreign_uri_coco(bundle, field_name, resource_name=None):
    field_dict = bundle.data.get(field_name)
    if field_dict.get('id'):
        bundle.data[field_name] = "/coco/api/v2/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle

def dict_to_foreign_uri_m2m_coco(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/coco/api/v2/%s/%s/"%(resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle



class TrainerResource(ModelResource):
	language = fields.ForeignKey('training.api.LanguageResource', 'language')
	class Meta:
		resource_name = 'trainer'
		queryset = Trainer.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
	dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])
	hydrate_language = partial(dict_to_foreign_uri_coco, field_name='language')

class LanguageResource(ModelResource):
	class Meta:
		resource_name = 'language'
		queryset = Language.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

class MediatorResource(ModelResource):
    mediator_label = fields.CharField()
    assigned_villages = fields.ListField()
    partner = fields.ForeignKey('coco.api.PartnerResource', 'partner')
    district = fields.ForeignKey('coco.api.DistrictResource', 'district', null=True)
    class Meta:
        max_limit = None
        authentication = ApiKeyAuthentication()
        queryset = Animator.objects.prefetch_related('assigned_villages', 'district', 'partner').all()
        resource_name = 'mediator'
        authorization = Authorization()
        always_return_data = True
        excludes = ['time_created', 'time_modified' ]
    dehydrate_partner = partial(foreign_key_to_id, field_name='partner',sub_field_names=['id','partner_name'])
    dehydrate_district = partial(foreign_key_to_id, field_name='district',sub_field_names=['id','district_name'])
    hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m_coco, field_name='assigned_villages', resource_name = 'village')
    hydrate_district = partial(dict_to_foreign_uri_coco, field_name ='district')
    
    def dehydrate_assigned_villages(self, bundle):
        return [{'id': vil.id, 'village_name': vil.village_name} for vil in set(bundle.obj.assigned_villages.all()) ]

    def dehydrate_mediator_label(self,bundle):
        #for sending out label incase of dropdowns
        return ','.join([ vil.village_name for vil in set(bundle.obj.assigned_villages.all())])
            
    def obj_create(self, bundle, **kwargs):
        bundle = super(MediatorResource, self).obj_create(bundle, **kwargs)
        vil_list = bundle.data.get('assigned_villages')
        for vil in vil_list:
            vil = Village.objects.get(id = int(vil.split('/')[-2]))
            u = AnimatorAssignedVillage(animator=bundle.obj, village=vil)
            u.save()
    
        return bundle

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
	dehydrate_assessment = partial(foreign_key_to_id, field_name='assessment', sub_field_names=['id','name'])
	hydrate_assessment = partial(dict_to_foreign_uri, field_name='assessment')

class TranslationResource(ModelResource):
	question = fields.ForeignKey('training.api.QuestionResource', 'question')
	class Meta:
		resource_name = 'translation'
		queryset = Question.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
	dehydrate_question = partial(foreign_key_to_id, field_name='question', sub_field_names=['id','text'])
	hydrate_question = partial(dict_to_foreign_uri, field_name='question')

class TrainingResource(ModelResource):
	language = fields.ForeignKey('training.api.LanguageResource', 'language')
	state = fields.ForeignKey('training.api.StateResource', 'state')
	class Meta:
		resource_name = 'training'
		queryset = Training.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
	hydrate_language = partial(dict_to_foreign_uri_coco, field_name='language')
