from functools import partial
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict, ModelChoiceField
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource, NOT_AVAILABLE
from tastypie.validation import FormValidation

from activities.models import Screening, PersonAdoptPractice, PersonMeetingAttendance
from geographies.models import Village, District, State
from programs.models import Partner
from people.models import Animator, AnimatorAssignedVillage, Person, PersonGroup
from videos.models import Video, Language
from models import CocoUser

# Will need to changed when the location of forms.py is changed
from dashboard.forms import AnimatorForm, PersonAdoptPracticeForm, PersonForm, PersonGroupForm, ScreeningForm, VideoForm

class PMANotSaved(Exception):
    pass

class PartnerDoesNotExist(Exception):
    pass

### Reference for below class https://github.com/toastdriven/django-tastypie/issues/152
class ModelFormValidation(FormValidation):
    """
        Override tastypie's standard ``FormValidation`` since this does not care
        about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
        """
    
    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]
        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()
        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]
        
        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])
        
        # validate and return messages on error
        if request.method == "PUT":
            #Handles edit case
            form = self.form_class(data, instance = bundle.obj.__class__.objects.get(pk=bundle.data['id']))
        else:
            form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors

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
        bundle.data[field_name] = "/coco/api/v2/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle

def dict_to_foreign_uri_m2m(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/coco/api/v2/%s/%s/"%(resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle

def get_user_partner_id(user_id):
    if user_id:
        try:
            partner_id = CocoUser.objects.get(user_id = user_id).partner.id
        except Exception as e:
            partner_id = None
            raise PartnerDoesNotExist('partner does not exist for user '+ user_id+" : "+ e)
        
    return partner_id

def get_user_videos(user_id):
    ###Videos produced by partner with in the same state
    coco_user = CocoUser.objects.get(user_id = user_id)
    villages = coco_user.get_villages()
    user_states = State.objects.filter(district__block__village__in = villages).distinct().values_list('id', flat=True)
    ###FIRST GET VIDEOS PRODUCED IN STATE WITH SAME PARTNER
    videos = Video.objects.filter(village__block__district__state__in = user_states, partner_id = coco_user.partner_id).values_list('id', flat = True)
    ###Get videos screened to allow inter partner sharing of videos
    videos_seen = set(Person.objects.filter(village__in = villages, partner_id = coco_user.partner_id).values_list('screening__videoes_screened', flat=True))
    return set(list(videos) + list(videos_seen))
    
def get_user_mediators(user_id):
    coco_user = CocoUser.objects.get(user_id = user_id)
    villages = coco_user.get_villages()
    partner = get_user_partner_id(user_id)
    user_districts = District.objects.filter(block__village__in = villages).distinct().values_list('id', flat=True)
    mediators_from_same_district = Animator.objects.filter(district__in = user_districts, partner_id = partner).distinct().values_list('id', flat = True)
        
    return mediators_from_same_district

def assign_partner(bundle):
    partner_id = get_user_partner_id(bundle.request.user.id)
    if partner_id:
        bundle.data['partner'] = "/coco/api/v2/%s/%s/"%('partner', str(partner_id))
    else:
        bundle.data['partner'] = None
    
    return bundle
    
class VillagePartnerAuthorization(Authorization):
    def __init__(self, field):
        self.village_field = field
    
    def read_list(self, object_list, bundle):
        villages = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages()
        kwargs = {}
        kwargs[self.village_field] = villages
        kwargs['partner_id'] = get_user_partner_id(bundle.request.user.id)
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.village_field] = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages()
        kwargs['partner_id'] = get_user_partner_id(bundle.request.user.id)
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound( "Not allowed to download" )

class VillageAuthorization(Authorization):
    def __init__(self, field):
        self.village_field = field
    
    def read_list(self, object_list, bundle):
        villages = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages()
        kwargs = {}
        kwargs[self.village_field] = villages
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.village_field] = CocoUser.objects.get(user_id= bundle.request.user.id).get_villages()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound( "Not allowed to download Village" )

class MediatorAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_mediators(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        if bundle.obj.id in get_user_mediators(bundle.request.user.id):
            return True
        # Is the requested object owned by the user?
        else:
            raise NotFound( "Not allowed to download Mediator")

class VideoAuthorization(Authorization):
    def read_list(self, object_list, bundle):        
        return object_list.filter(id__in= get_user_videos(bundle.request.user.id))
    
    def read_detail(self, object_list, bundle):
        #To add adoption for the video seen which is outside user access
        if bundle.obj.id in get_user_videos(bundle.request.user.id):
            return True
        else:
            raise NotFound( "Not allowed to download video")

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

class PartnerResource(ModelResource):    
    class Meta:
        max_limit = None
        queryset = Partner.objects.all()
        resource_name = 'partner'
        authentication = SessionAuthentication()
        authorization = Authorization()

class MediatorResource(BaseResource):
    mediator_label = fields.CharField()
    assigned_villages = fields.ListField()
    partner = fields.ForeignKey('coco.api.PartnerResource', 'partner')
    district = fields.ForeignKey('coco.api.DistrictResource', 'district', null=True)
    class Meta:
        max_limit = None
        authentication = SessionAuthentication()
        queryset = Animator.objects.prefetch_related('assigned_villages', 'district', 'partner').all()
        resource_name = 'mediator'
        authorization = MediatorAuthorization()
        validation = ModelFormValidation(form_class=AnimatorForm)
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

    def obj_update(self, bundle, **kwargs):
        #Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(MediatorResource, self).obj_update(bundle, **kwargs)
        mediator_id = bundle.data.get('id')
        vil_id_list = []
        for vil_resource in bundle.data.get('assigned_villages'):
            vil_id_list.append(int(vil_resource.split('/')[-2]))
        existing_vil_ids = AnimatorAssignedVillage.objects.filter(animator__id=mediator_id).values_list('village__id', flat=True)
        #delete only if assigned villages are different
        if len(list(set(vil_id_list) & set(existing_vil_ids))) != len(vil_id_list) :
            #first delete the old associations
            del_objs = AnimatorAssignedVillage.objects.filter(animator__id=mediator_id).delete()
            #add new villages again
            vil_list = bundle.data.get('assigned_villages')
            for vil in vil_list:
                vil = Village.objects.get(id = int(vil.split('/')[-2]))
                u = AnimatorAssignedVillage(animator=bundle.obj, village=vil)
                u.save()
    
        return bundle
        
    def hydrate_partner(self, bundle):
        partner_id = get_user_partner_id(bundle.request.user.id)
        if partner_id:
            bundle.data['partner'] ="/coco/api/v2/partner/"+str(partner_id)+"/"
        return bundle

class VillageResource(ModelResource):
    # nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
    
    block_name = fields.CharField('block__block_name')
    district_name= fields.CharField('block__district__district_name')
    state_name = fields.CharField('block__district__state__state_name')
    country_name = fields.CharField('block__district__state__country__country_name')
    
    class Meta:
        max_limit = None
        queryset = Village.objects.select_related('block__district__state__country').all()
        resource_name = 'village'
        authentication = SessionAuthentication()
        authorization = VillageAuthorization('id__in')
        always_return_data = True

class DistrictResource(ModelResource):
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        authentication = SessionAuthentication()
        authorization = VillageAuthorization('block__village__id__in')
        max_limit = None

class VideoResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village')
    cameraoperator = fields.ForeignKey(MediatorResource, 'cameraoperator')
    facilitator = fields.ForeignKey(MediatorResource, 'facilitator')
    farmers_shown = fields.ToManyField('coco.api.PersonResource', 'farmers_shown')
    language = fields.ForeignKey('coco.api.LanguageResource', 'language')
    partner = fields.ForeignKey(PartnerResource, 'partner')
    
    dehydrate_village = partial(foreign_key_to_id, field_name='village', sub_field_names=['id','village_name'])
    dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])
    dehydrate_cameraoperator = partial(foreign_key_to_id, field_name='cameraoperator', sub_field_names=['id','name'])
    dehydrate_facilitator = partial(foreign_key_to_id, field_name='facilitator', sub_field_names=['id','name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name ='village')
    hydrate_language = partial(dict_to_foreign_uri, field_name='language')
    hydrate_cameraoperator = partial(dict_to_foreign_uri, field_name='cameraoperator', resource_name='mediator')
    hydrate_facilitator = partial(dict_to_foreign_uri, field_name='facilitator', resource_name='mediator')
    hydrate_farmers_shown = partial(dict_to_foreign_uri_m2m, field_name = 'farmers_shown', resource_name = 'person')
    hydrate_partner = partial(assign_partner)
    
    class Meta:
        max_limit = None
        queryset = Video.objects.prefetch_related('village', 'language', 'cameraoperator', 'facilitator', 'farmers_shown').all()
        resource_name = 'video'
        authentication = SessionAuthentication()
        authorization = VideoAuthorization()
        validation = ModelFormValidation(form_class=VideoForm)
        always_return_data = True
        excludes = ['duration', 'related_practice', 'time_created', 'time_modified',]
    
    def dehydrate_farmers_shown(self, bundle):
        return [{'id': person.id, 'person_name': person.person_name} for person in bundle.obj.farmers_shown.all() ]

class PersonGroupResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village')
    group_label = fields.CharField()
    partner = fields.ForeignKey(PartnerResource, 'partner')
    class Meta:
        max_limit = None
        queryset = PersonGroup.objects.prefetch_related('village').all()
        resource_name = 'group'
        authentication = SessionAuthentication()
        authorization = VillagePartnerAuthorization('village__in')
        validation = ModelFormValidation(form_class=PersonGroupForm)
        excludes = ['time_created', 'time_modified']
        always_return_data = True
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id', 'village_name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')
    hydrate_partner = partial(assign_partner)
    
    def dehydrate_group_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'village').village_name
        g_field = getattr(bundle.obj, 'group_name')
        return "("+ g_field+"," + v_field +")"

    def hydrate_village(self, bundle):
        village = bundle.data.get('village')
        if village and not hasattr(bundle,'village_flag'):
            try:
                village_id = village.get('id')
                bundle.data['village'] = "/coco/api/v2/village/"+str(village_id)+"/"
                bundle.village_flag = True
            except:
                bundle.data['village'] = None
        return bundle

class ScreeningResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village')
    animator = fields.ForeignKey(MediatorResource, 'animator')
    partner = fields.ForeignKey(PartnerResource, 'partner')
    videoes_screened = fields.ToManyField('coco.api.VideoResource', 'videoes_screened', related_name='screening')
    farmer_groups_targeted = fields.ToManyField('coco.api.PersonGroupResource', 'farmer_groups_targeted', related_name='screening')
    farmers_attendance = fields.ListField()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    dehydrate_animator = partial(foreign_key_to_id, field_name='animator',sub_field_names=['id','name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')
    hydrate_animator = partial(dict_to_foreign_uri, field_name='animator', resource_name='mediator')
    hydrate_farmer_groups_targeted = partial(dict_to_foreign_uri_m2m, field_name = 'farmer_groups_targeted', resource_name='group')
    hydrate_videoes_screened = partial(dict_to_foreign_uri_m2m, field_name = 'videoes_screened', resource_name='video')
    hydrate_partner = partial(assign_partner)
    
    class Meta:
        max_limit = None
        queryset = Screening.objects.prefetch_related('village', 'animator', 'videoes_screened', 'farmer_groups_targeted',
                                                      'personmeetingattendance_set__person', 'personmeetingattendance_set__expressed_adoption_video').all()
        resource_name = 'screening'
        authentication = SessionAuthentication()
        authorization = VillagePartnerAuthorization('village__in')
        validation = ModelFormValidation(form_class = ScreeningForm)
        always_return_data = True
        excludes = ['location', 'time_created', 'time_modified']
    
    def obj_create(self, bundle, **kwargs):
        pma_list = bundle.data.get('farmers_attendance')
        if pma_list:
            bundle = super(ScreeningResource, self).obj_create(bundle, **kwargs)
            user_id = None
            if bundle.request.user:
                user_id =  bundle.request.user.id
            screening_id  = getattr(bundle.obj,'id')
            for pma in pma_list:
                try:
                    attendance = PersonMeetingAttendance(screening_id=screening_id, person_id=pma['person_id'], 
                                                  expressed_adoption_video_id = pma['expressed_adoption_video']['id'],
                                                   interested = pma['interested'], user_created_id = user_id,
                                                  expressed_question = pma['expressed_question'],)
                    attendance.save()
                except Exception, e:
                    raise PMANotSaved('For Screening with id: ' + str(screening_id) + ' pma is not getting saved. pma details: '+ str(e))
        
            return bundle
        else:
            raise PMANotSaved('Screening with details: ' + str(bundle.data) + ' can not be saved because attendance list is not available')

    def obj_update(self, bundle, **kwargs):
        #Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(ScreeningResource, self).obj_update(bundle, **kwargs)
        user_id = None
        if bundle.request.user:
            user_id =  bundle.request.user.id
        
        screening_id = bundle.data.get('id')
        del_objs = PersonMeetingAttendance.objects.filter(screening__id=screening_id).delete()
        pma_list = bundle.data.get('farmers_attendance')
        for pma in pma_list:
            pma = PersonMeetingAttendance(screening_id=screening_id, person_id=pma['person_id'], 
                                          expressed_adoption_video_id = pma['expressed_adoption_video']['id'],
                                           interested = pma['interested'], 
                                          expressed_question = pma['expressed_question'], user_created_id = user_id)
            pma.save()    
        return bundle
    
    def dehydrate_videoes_screened(self, bundle):
        return [{'id': video.id, 'title': video.title,} for video in bundle.obj.videoes_screened.all()]
        
    def dehydrate_farmer_groups_targeted(self, bundle):
        return [{'id': group.id, 'group_name': group.group_name,} for group in bundle.obj.farmer_groups_targeted.all()]
    
    def dehydrate_farmers_attendance(self, bundle):
        return [{'person_id':pma.person.id, 
                 'person_name': pma.person.person_name, 
                 'interested': pma.interested, 
                 'expressed_question': pma.expressed_question, 
                 'expressed_adoption_video': {'id': pma.expressed_adoption_video.id, 
                                              'title': pma.expressed_adoption_video.title } if pma.expressed_adoption_video else {}
                 }  for pma in bundle.obj.personmeetingattendance_set.all()]
    
class PersonResource(BaseResource):
    label = fields.CharField()
    village = fields.ForeignKey(VillageResource, 'village')
    group = fields.ForeignKey(PersonGroupResource, 'group',null=True)
    videos_seen = fields.DictField(null=True)
    partner = fields.ForeignKey(PartnerResource, 'partner')
    
    class Meta:
        max_limit = None
        queryset = Person.objects.prefetch_related('village','group', 'personmeetingattendance_set__screening__videoes_screened').all()
        resource_name = 'person'
        authorization = VillagePartnerAuthorization('village__in')
        validation = ModelFormValidation(form_class = PersonForm)
        always_return_data = True
        excludes = ['date_of_joining', 'image_exists', 'time_created', 'time_modified']
    
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id', 'village_name'])
    dehydrate_group = partial(foreign_key_to_id, field_name='group',sub_field_names=['id','group_name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name = 'village')
    hydrate_group = partial(dict_to_foreign_uri, field_name = 'group')
    hydrate_partner = partial(assign_partner)
    
    def dehydrate_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'village').village_name
        f_field = getattr(bundle.obj, 'father_name')
        p_field = getattr(bundle.obj, 'person_name')
        return p_field+"("+v_field+","+f_field+")"
    
    def dehydrate_videos_seen(self, bundle):
        videos_seen = [{'id': video.id, 'title': video.title} for pma in bundle.obj.personmeetingattendance_set.all() for video in pma.screening.videoes_screened.all() ]
        return [dict(tupleized) for tupleized in set(tuple(item.items()) for item in videos_seen)]
        
class PersonAdoptVideoResource(BaseResource):
    person = fields.ForeignKey(PersonResource, 'person')
    video = fields.ForeignKey(VideoResource, 'video')
    partner = fields.ForeignKey(PartnerResource, 'partner')
    group = fields.DictField(null = True)
    village = fields.DictField(null = True)
    class Meta:
        max_limit = None
        queryset = PersonAdoptPractice.objects.prefetch_related('person__village','video', 'person__group', 'person').all()
        resource_name = 'adoption'
        authentication = SessionAuthentication()
        authorization = VillagePartnerAuthorization('person__village__in')
        validation = ModelFormValidation(form_class = PersonAdoptPracticeForm)
        always_return_data = True
        excludes = ['time_created', 'time_modified']
    dehydrate_video = partial(foreign_key_to_id, field_name='video',sub_field_names=['id','title'])
    dehydrate_person = partial(foreign_key_to_id, field_name='person',sub_field_names=['id','person_name'])
    hydrate_video = partial(dict_to_foreign_uri, field_name='video')
    hydrate_person = partial(dict_to_foreign_uri, field_name='person')
    hydrate_partner = partial(assign_partner)
    
    def dehydrate_group(self, bundle):
        return {'id': bundle.obj.person.group.id, 'group_name': bundle.obj.person.group.group_name} if bundle.obj.person.group else {'id': None, 'group_name': None}

    def dehydrate_village(self, bundle):
        return {'id': bundle.obj.person.village.id, 'village_name': bundle.obj.person.village.village_name}

class LanguageResource(ModelResource):    
    class Meta:
        max_limit = None
        queryset = Language.objects.all()
        resource_name = 'language'
        authentication = SessionAuthentication()
        authorization = Authorization()
