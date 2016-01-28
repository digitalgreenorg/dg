from functools import partial

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import ModelForm
from django.forms.models import model_to_dict, ModelChoiceField

from models import Trainer, Assessment, Question, Training, Score, TrainingUser
from geographies.models import District, Village, State
from programs.models import Partner
from videos.models import Language
from tastypie import fields
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import ImmediateHttpResponse, NotFound
from tastypie.resources import ModelResource
from people.models import Animator, AnimatorAssignedVillage

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
        dict["online_id"] = dict["id"]
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
#---------------------------------------------------------------------------------------------#

class PartnerResource(ModelResource):
	class Meta:
		queryset = Partner.objects.all()
		resource_name = 'partner'
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

class VillageResource(ModelResource):
	class Meta:
		queryset = Village.objects.all()
		resource_name = 'village'
		authentication = ApiKeyAuthentication()
		authorization = Authorization()

def get_user_districts(user_id):
	coco_user = TrainingUser.objects.get(user_id = user_id)
	user_states = coco_user.get_states()
	districts_of_states = District.objects.filter(state__in = user_states).values_list('id', flat = True)
	return districts_of_states

class DistrictAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_districts(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_districts(bundle.request.user.id):
            return True
        # Is the requested object owned by the user?
        else:
            raise NotFound( "Not allowed to download District")

class DistrictResource(ModelResource):
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        authentication = ApiKeyAuthentication()
        authorization = DistrictAuthorization()
        max_limit = None

def get_user_mediators(user_id):
    coco_user = TrainingUser.objects.get(user_id = user_id)
    user_states = coco_user.get_states()
    mediators_from_same_state = Animator.objects.filter(district__state__id__in = user_states).distinct().values_list('id', flat = True)      
    return mediators_from_same_state

class StateAuthorization(Authorization):
    def __init__(self,field):
        self.state_field = field
    
    def read_list(self, object_list, bundle):
        states = TrainingUser.objects.get(user_id= bundle.request.user.id).get_states()
        kwargs = {}
        kwargs[self.state_field] = states
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.state_field] = TrainingUser.objects.get(user_id= bundle.request.user.id).get_states()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound( "Not allowed to download State" )

class MediatorAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_mediators(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_mediators(bundle.request.user.id):
            return True
        # Is the requested object owned by the user?
        else:
            raise NotFound( "Not allowed to download Mediator")

class BaseResource(ModelResource):
    def full_hydrate(self, bundle):
        bundle = super(BaseResource, self).full_hydrate(bundle)
        bundle.obj.user_modified_id = bundle.request.user.id
        return bundle
    
    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        self.authorized_create_detail(self.get_object_list(bundle.request), bundle)
        bundle = self.full_hydrate(bundle)
        bundle.obj.user_created_id = bundle.request.user.id
        return self.save(bundle)
#---------------------------------------------------------------------------------#

class TrainerResource(ModelResource):
    language = fields.ForeignKey('training.api.LanguageResource', 'language')
    class Meta:
        resource_name = 'trainer'
        queryset = Trainer.objects.prefetch_related('language').all()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        authorization = Authorization()
    dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])
    hydrate_language = partial(dict_to_foreign_uri_coco, field_name='language')
    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class LanguageResource(ModelResource):
    class Meta:
        resource_name = 'language'
        queryset = Language.objects.all()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class MediatorResource(ModelResource):
    mediator_label = fields.CharField()
    assigned_villages = fields.ListField()
    partner = fields.ForeignKey('training.api.PartnerResource', 'partner')
    district = fields.ForeignKey('training.api.DistrictResource', 'district', null=True)
    class Meta:
        max_limit = None
        authentication = ApiKeyAuthentication()
        queryset = Animator.objects.prefetch_related('assigned_villages', 'district', 'partner').all()
        resource_name = 'mediator'
        authorization = MediatorAuthorization()
        always_return_data = True
        excludes = ['time_created', 'time_modified' ]
    dehydrate_partner = partial(foreign_key_to_id, field_name='partner',sub_field_names=['id','partner_name'])
    dehydrate_district = partial(foreign_key_to_id, field_name='district',sub_field_names=['id','district_name'])
    hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m, field_name='assigned_villages', resource_name = 'village')
    hydrate_district = partial(dict_to_foreign_uri, field_name ='district')
    
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
	language = fields.ForeignKey('training.api.LanguageResource', 'language')
	assessment = fields.ForeignKey('training.api.AssessmentResource', 'assessment')
	class Meta:
		resource_name = 'question'
		queryset = Question.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
	dehydrate_assessment = partial(foreign_key_to_id, field_name='assessment', sub_field_names=['id','name'])
	hydrate_assessment = partial(dict_to_foreign_uri, field_name='assessment')
	dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])
	hydrate_language = partial(dict_to_foreign_uri_coco, field_name='language')


class TrainingResource(ModelResource):
	language = fields.ForeignKey('training.api.LanguageResource', 'language')
	assessment = fields.ForeignKey('training.api.AssessmentResource', 'assessment')
	trainer = fields.ToManyField('training.api.TrainerResource', 'trainer')
	participants = fields.ToManyField('training.api.MediatorResource', 'participants')
	class Meta:
		resource_name = 'training'
		queryset = Training.objects.all()
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		always_return_data = True
	hydrate_language = partial(dict_to_foreign_uri_coco, field_name='language')
	hydrate_assessment = partial(dict_to_foreign_uri, field_name='assessment')
	hydrate_trainer = partial(dict_to_foreign_uri_m2m, field_name = 'trainer', resource_name = 'trainer')
	hydrate_participants = partial(dict_to_foreign_uri_m2m, field_name = 'participants', resource_name = 'mediator')
	dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])	
	dehydrate_assessment = 	partial(foreign_key_to_id, field_name='assessment', sub_field_names=['id','name'])

	def dehydrate_trainer(self, bundle):
	        return [{'id': trainer.id, 'name':trainer.name} for trainer in bundle.obj.trainer.all() ]

	def dehydrate_participants(self, bundle):
		return [{'id':mediator.id, 'name':mediator.name} for mediator in bundle.obj.participants.all()]

	


#------------------------------------------------------------------------------------------#

class StateResource(ModelResource):
    country_name = fields.CharField('country__country_name')
    
    class Meta:
        max_limit = None
        queryset = State.objects.all()        
	resource_name = 'state'
        authentication = ApiKeyAuthentication()
        authorization = StateAuthorization('id__in')
        always_return_data = True

class ScoreResource(ModelResource):
    participant = fields.ForeignKey('training.api.MediatorResource', 'participant')
    training = fields.ForeignKey('training.api.TrainingResource', 'training')
    question = fields.ForeignKey('training.api.QuestionResource', 'question')
    class Meta:
        max_limit = None
        queryset = Score.objects.all()
        resource_name = 'score'
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
    hydrate_participant = partial(dict_to_foreign_uri, field_name='participant', resource_name='mediator')
    hydrate_training = partial(dict_to_foreign_uri, field_name='training')
    hydrate_question = partial(dict_to_foreign_uri, field_name='question')
    
    dehydrate_participant = partial(foreign_key_to_id, field_name='participant', sub_field_names=['id','name'])
    dehydrate_training = partial(foreign_key_to_id, field_name='training', sub_field_names=['id'])
    dehydrate_question = partial(foreign_key_to_id, field_name='question', sub_field_names=['id','text'])	






#---------------------------------------------------------------------------#
