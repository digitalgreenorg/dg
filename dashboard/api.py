from django.conf.urls.defaults import patterns, include, url
from tastypie import fields
from tastypie.authentication import BasicAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import FormValidation
from tastypie.validation import Validation
from functools import partial
from dashboard.models import CocoUser, Country, State, District, Block, Village, FieldOfficer,Partners, \
                AnimatorAssignedVillage, Video, PersonGroups, Screening, Animator, Person, PersonAdoptPractice, UserPermission, Language, PersonMeetingAttendance
from forms import  VideoForm, PersonForm, AnimatorForm, PersonGroupsForm, ScreeningForm
from django.forms.models import model_to_dict
from django.db import models
from django.forms.models import ModelChoiceField

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
        
        converted = []
        if type(uri) == type(dict()):
            converted.append(uri.get('id'))
            return uri.get('id')
        elif type(uri) == type(list()):
            for item in uri:
                converted.append(item.get('id'))
            return converted

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
        
        print self.form_class
        # validate and return messages on error
        if request.method == "PUT":
            #Handles edit case
            form = self.form_class(data, instance = bundle.obj.__class__.objects.get(pk=bundle.data['id']))
        else:
            form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors

class MediatorFormValidation(FormValidation):
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
        converted = []
        if type(uri) == type(dict()):
            converted.append(uri.get('id'))
            return uri.get('id')
        elif type(uri) == type(list()):
            for item in uri:
                print item.get('id')
                converted.append(item.get('id'))
            return converted

    def is_valid(self, bundle, request=None):
        partner_id = get_user_partner_id(request)
        if partner_id:
            bundle.data['partner'] ={'id':partner_id, 'partner_name':''} #"/api/v1/partner/"+str(partner_id)+"/"
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

def get_user_partner_id(request):
    if request.user.id:
        partner_id = CocoUser.objects.filter(user__id = request.user.id)
        if partner_id:
            partner_id = partner_id[0]
        else:
            partner_id = None
            if request.user.id == 1 or request.user.id == 2:
                partner_id = 10000000000001            
    return partner_id
def get_user_villages(request):
    if request:
        user_permissions = UserPermission.objects.filter(username = request.user)
        villages = Village.objects.none()
        for user_permission in user_permissions:
            if(user_permission.role=='A'):
                villages = villages | Village.objects.all()
            if(user_permission.role=='D'):
                states = State.objects.filter(region = user_permission.region_operated)
                districts = District.objects.filter(state__in = states)
                blocks = Block.objects.filter(district__in = districts)
                villages = villages | Village.objects.filter(block__in = blocks)
            if(user_permission.role=='F'):
                blocks = Block.objects.filter(district = user_permission.district_operated)
                villages = villages | Village.objects.filter(block__in = blocks)
        return villages

#Get User Districts for video download purpose

def get_user_districts(request):
    if request:
        user_permissions = UserPermission.objects.filter(username = request.user)
        districts = District.objects.none()
        for user_permission in user_permissions:
            if(user_permission.role=='A'):
                districts = districts | District.objects.all()
            if(user_permission.role=='D'):
                states = State.objects.filter(region = user_permission.region_operated)
                districts = districts | District.objects.filter(state__in = states)
            if(user_permission.role=='F'):
                districts = District.objects.filter(district_name = user_permission.district_operated)
        return districts

class VillageLevelAuthorization(DjangoAuthorization):
    def __init__(self, field):
        self.village_field = field
    def apply_limits(self, request, object_list):
        villages = get_user_villages(request)
        kwargs = {}
        kwargs[self.village_field] = villages
        # params = {
        #             village_field: villages,
        #         }
        return object_list.filter(**kwargs).distinct()

class MediatorResource(ModelResource):
    mediator_label = fields.CharField()
    assigned_villages = fields.ListField()
    partner = fields.ForeignKey('dashboard.api.PartnersResource', 'partner')
    
    class Meta:
        queryset = Animator.objects.all()
        resource_name = 'mediator'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('assigned_villages__in')
        #authorization = Authorization()
        validation = MediatorFormValidation(form_class=AnimatorForm)
        always_return_data = True
        excludes = ['total_adoptions','time_created', 'time_modified' ]
    dehydrate_partner = partial(foreign_key_to_id, field_name='partner',sub_field_names=['id','partner_name'])

    def dehydrate_assigned_villages(self, bundle):
        print 'in dehrate assigned villages'
        v_field = getattr(bundle.obj, 'assigned_villages').all().distinct()
        vil_list=[]
        for i in v_field:
            vil_list.append({"id":i.id, "name":i.village_name})
        return vil_list
    
    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(MediatorResource, self).obj_create(
            bundle)
        vil_list = bundle.data.get('assigned_villages')
        for vil in vil_list:
            vil = Village.objects.get(id = int(vil.split('/')[-2]))
            u = AnimatorAssignedVillage(animator=bundle.obj, village=vil)
            u.save()
    
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        #Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(MediatorResource, self).obj_create(bundle)
        
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
        
    def dehydrate_mediator_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'assigned_villages').all().distinct()
        label = ""
        for i in v_field:
            label = label + i.village_name + ","
        return "("+ label +")"
    
    def hydrate_assigned_villages(self, bundle):
        m2m_list = bundle.data.get('assigned_villages')
        resource_uri_list = []
        for item in m2m_list:
            try:
                resource_uri_list.append("/api/v1/village/"+str(item.get('id'))+"/")
            except:
                continue
        if not hasattr(bundle,'assigned_villages_flag'):
            bundle.data['assigned_villages'] = resource_uri_list
            bundle.assigned_villages_flag = True
            
        return bundle

class VillageResource(ModelResource):
    # nandini: add the fields which have been chosen. so that if we want a field to come through the api we have to add it here.
    
    block_name = fields.CharField('block__block_name')
    district_name= fields.CharField('block__district__district_name')
    state_name = fields.CharField('block__district__state__state_name')
    country_name = fields.CharField('block__district__state__country__country_name')
    
    class Meta:
        queryset = Village.objects.select_related('block__district__state__country').all()
        resource_name = 'village'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('id__in')
        #authorization = Authorization()
        
        max_limit = None

class VideoResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
    cameraoperator = fields.ForeignKey(MediatorResource, 'cameraoperator')
    facilitator = fields.ForeignKey(MediatorResource, 'facilitator')
    farmers_shown = fields.ToManyField('dashboard.api.PersonResource', 'farmers_shown')
    language = fields.ForeignKey('dashboard.api.LanguageResource', 'language')
    
    dehydrate_village = partial(foreign_key_to_id, field_name='village', sub_field_names=['id','village_name'])
    dehydrate_language = partial(foreign_key_to_id, field_name='language', sub_field_names=['id','language_name'])
    dehydrate_cameraoperator = partial(foreign_key_to_id, field_name='cameraoperator', sub_field_names=['id','name'])
    dehydrate_facilitator = partial(foreign_key_to_id, field_name='facilitator', sub_field_names=['id','name'])
    dehydrate_farmers_shown = partial(many_to_many_to_subfield, field_name='farmers_shown',sub_field_names=['id','person_name'])
    
    class Meta:
        queryset = Video.objects.select_related('village').all()
        resource_name = 'video'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        #authorization = Authorization()
        
        validation = ModelFormValidation(form_class=VideoForm)
        always_return_data = True
        excludes = ['viewers','time_created', 'time_modified', 'duration' ]
    
    def apply_authorization_limits(self, request, object_list):
        districts = get_user_districts(request)
        screened_vids = list(Screening.objects.filter(village__block__district__in=districts).distinct().values_list('videoes_screened__id',flat=True))
        produced_vids = list(Video.objects.filter(village__block__district__in = districts).values_list('id', flat=True))
        #doing set of two lists avoid merging duplicates in the final merged list
        vids = list(set(screened_vids + produced_vids))
        return object_list.filter(id__in= vids)

    def hydrate_language(self, bundle):
        language = bundle.data.get('language')
        if language and not hasattr(bundle,'language_flag'):
            try:
                id = language.get('id')
                bundle.data['language'] = "/api/v1/language/"+str(id)+"/"
                bundle.language_flag = True
            except:
                print 'language id in video does not exist'
                bundle.data['language'] = None
        return bundle
    
    def hydrate_village(self, bundle):
        village = bundle.data.get('village')
        if village and not hasattr(bundle,'village_flag'):
            try:
                village_id = village.get('id')
                bundle.data['village'] = "/api/v1/village/"+str(village_id)+"/"
                bundle.village_flag = True
            except:
                print 'village id in video does not exist'
                bundle.data['village'] = None
        return bundle
    
    def hydrate_cameraoperator(self, bundle):
        cameraoperator = bundle.data.get('cameraoperator')
        if cameraoperator and not hasattr(bundle,'cameraoperator_flag'):
            try:
                id = cameraoperator.get('id')
                bundle.data['cameraoperator'] = "/api/v1/mediator/"+str(id)+"/"
                bundle.cameraoperator_flag = True
            except:
                print 'camera operator id in video does not exist'
                bundle.data['cameraoperator'] = None
        return bundle
    
    def hydrate_facilitator(self, bundle):
        facilitator = bundle.data.get('facilitator')
        if facilitator and not hasattr(bundle,'facilitator_flag'):
            try:
                id = facilitator.get('id')
                bundle.data['facilitator'] = "/api/v1/mediator/"+str(id)+"/"
                bundle.facilitator_flag = True
            except:
                print 'facilitator id in video does not exist'
                bundle.data['facilitator'] = None
        return bundle
    
    def hydrate_farmers_shown(self, bundle):
        m2m_list = bundle.data.get('farmers_shown')
        resource_uri_list = []
        for item in m2m_list:
            try:
                resource_uri_list.append("/api/v1/person/"+str(item.get('id'))+"/")
            except:
                continue
        if not hasattr(bundle,'farmers_shown_flag'):
            bundle.data['farmers_shown'] = resource_uri_list
            bundle.farmers_shown_flag = True
            
        return bundle
    
class PersonGroupsResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
    group_label = fields.CharField()
    class Meta:
        queryset = PersonGroups.objects.select_related('village').all()
        resource_name = 'group'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('village__in')
        #authorization = Authorization()
        
        validation = ModelFormValidation(form_class=PersonGroupsForm)
        excludes = ['days', 'timings', 'time_created', 'time_modified', 'time_updated']
        always_return_data = True
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id', 'village_name'])
    
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
                bundle.data['village'] = "/api/v1/village/"+str(village_id)+"/"
                bundle.village_flag = True
            except:
                bundle.data['village'] = None
        return bundle

class ScreeningResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
    animator = fields.ForeignKey(MediatorResource, 'animator')
    videoes_screened = fields.ToManyField('dashboard.api.VideoResource', 'videoes_screened', related_name='screening')
    farmer_groups_targeted = fields.ToManyField('dashboard.api.PersonGroupsResource', 'farmer_groups_targeted', related_name='screening')
    farmers_attendance = fields.ListField()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    dehydrate_animator = partial(foreign_key_to_id, field_name='animator',sub_field_names=['id','name'])

    class Meta:
        queryset = Screening.objects.select_related('village').all()
        resource_name = 'screening'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('village__in')
        #authorization = Authorization()
        
        validation = ModelFormValidation(form_class = ScreeningForm)
        always_return_data = True
        excludes = ['time_created', 'time_modified']
    
    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(ScreeningResource, self).obj_create(bundle)
        screening_id  = getattr(bundle.obj,'id')
        pma_list = bundle.data.get('farmers_attendance')
        for pma in pma_list:
#            try:
#                per = Person.objects.get(id = pma['person_id'])
#            except:
#                per = None
#                print 'person does not exist in pma'
#            if pma['expressed_adoption_video']['id']:
#                try:
#                    vid = Video.objects.get(id = pma['expressed_adoption_video']['id'])
#                except:
#                    vid = None
#                    print 'expressed adoption video does not exist in pma'
#            else:
#                vid = None
            pma = PersonMeetingAttendance(screening_id=screening_id, person_id=pma['person_id'], expressed_adoption_video_id = pma['expressed_adoption_video']['id'],
                                           interested = pma['interested'], 
                                          expressed_question = pma['expressed_question'])
            pma.save()
    
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        #Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(ScreeningResource, self).obj_create(bundle)
        screening_id = bundle.data.get('id')
        del_objs = PersonMeetingAttendance.objects.filter(screening__id=screening_id).delete()
        pma_list = bundle.data.get('farmers_attendance')
        for pma in pma_list:
            pma = PersonMeetingAttendance(screening_id=screening_id, person_id=pma['person_id'], expressed_adoption_video = pma['expressed_adoption_video']['id'],
                                           interested = pma['interested'], 
                                          expressed_question = pma['expressed_question'])
            pma.save()    
        return bundle
    
    def dehydrate_videoes_screened(self, bundle):
        v_field = getattr(bundle.obj, 'videoes_screened').all().distinct()
        vid_list=[]
        for i in v_field:
            vid_list.append({"id":i.id, "title":i.title})
        return vid_list
    
    def dehydrate_farmer_groups_targeted(self, bundle):
        v_field = getattr(bundle.obj, 'farmer_groups_targeted').all().distinct()
        group_list=[]
        for i in v_field:
            group_list.append({"id":i.id, "group_name":i.group_name})
        return group_list
    
    def dehydrate_farmers_attendance(self, bundle):
        v_field = getattr(bundle.obj, 'farmers_attendance').all().select_related().distinct()
        screening_id  = getattr(bundle.obj,'id')
        pma_list=[]
        for i in v_field:
            pma = PersonMeetingAttendance.objects.filter(person__id = i.id, screening__id = screening_id).values('id',
                                                                                           'person__id',
                                                                                           'person__person_name',
                                                                                           'expressed_adoption_video__id',
                                                                                           'expressed_adoption_video__title',
                                                                                           'interested', 
                                                                                           'expressed_question')
            if pma:
                pma_list.append({'person_id':pma[0]['person__id'],'person_name':pma[0]['person__person_name'], 
                             'expressed_adoption_video': {'id':pma[0]['expressed_adoption_video__id'], 'title':pma[0]['expressed_adoption_video__title']},
                              'interested': pma[0]['interested'], 'expressed_question': pma[0]['expressed_question']})
            
        return pma_list
    
    
#    def obj_create(self, bundle, request=None, **kwargs):
#        bundle = super(MediatorResource, self).obj_create(
#            bundle)
#        vil_list = bundle.data.get('assigned_villages')
#        for vil in vil_list:
#            vil = Village.objects.get(id = int(vil.split('/')[-2]))
#            u = AnimatorAssignedVillage(animator=bundle.obj, village=vil)
#            u.save()
#    
#        return bundle
    
    def hydrate_videoes_screened(self, bundle):
        print 'in hydrate videoes'
        groups = bundle.data.get('videoes_screened')
        resource_uri_list = []
        for group in groups:
            try:
                resource_uri_list.append("/api/v1/video/"+str(group.get('id'))+"/")
            except:
                continue
        if not hasattr(bundle,'videoes_screened_flag'):
            bundle.data['videoes_screened'] = resource_uri_list
            bundle.videoes_screened_flag = True
        return bundle
    
    def hydrate_farmer_groups_targeted(self, bundle):
        print 'in hydrate groups'
        groups = bundle.data.get('farmer_groups_targeted')
        resource_uri_list = []
        for group in groups:
            try:
                resource_uri_list.append("/api/v1/group/"+str(group.get('id'))+"/")
            except:
                continue
                print 'in exception'
        if not hasattr(bundle,'farmer_groups_targeted_flag'):
            bundle.data['farmer_groups_targeted'] = resource_uri_list
            bundle.farmer_groups_targeted_flag = True
        return bundle
    
#    def hydrate_farmers_attendance(self, bundle):
#        print 'in farmers attendance'
#        pmas = bundle.data['farmers_attendance']
#        resource_uri_list = []
#        for pma in pmas:
#            #print pma
#            try:
#                resource_uri_list.append("/api/v1/person/"+str(pma.get('id'))+"/")
#            except:
#                continue
#                print 'in exception'
#        bundle.data['farmers_attendance'] = resource_uri_list
#        print resource_uri_list
#        return bundle
    
#    def save_m2m(self, bundle):
#        print 'in save m2m'
#        pmas = bundle.data.get('farmers_attendance', [])
#        print pmas

    
    def hydrate_village(self, bundle):
        village = bundle.data.get('village')
        if village:
            village_id = village.get('id')
            village_resource_uri = "/api/v1/village/"+str(village_id)+"/"
            bundle.data['village'] = village_resource_uri
        return bundle
    
    def hydrate_animator(self, bundle):
        animator = bundle.data.get('animator')
        if animator:
            animator_id = animator.get('id')
            animator_resource_uri = "/api/v1/mediator/"+str(animator_id)+"/"
            bundle.data['animator'] = animator_resource_uri
        return bundle

class PersonResource(ModelResource):
    label = fields.CharField()
    village = fields.ForeignKey(VillageResource, 'village')
    group = fields.ForeignKey(PersonGroupsResource, 'group',null=True)
    videos_seen = fields.DictField(null=True)
    
    class Meta:
        queryset = Person.objects.select_related('village','group').all()
        resource_name = 'person'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('village__in')
        #authorization = Authorization()
        
        validation = ModelFormValidation(form_class = PersonForm)
        always_return_data = True
        excludes = ['date_of_joining', 'address', 'image_exists', 'land_holdings', 'time_created', 'time_modified']
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id', 'village_name'])
    dehydrate_group = partial(foreign_key_to_id, field_name='group',sub_field_names=['id','group_name'])
    
    
    def dehydrate_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'village').village_name
        f_field = getattr(bundle.obj, 'father_name')
        p_field = getattr(bundle.obj, 'person_name')
        return p_field+"("+v_field+","+f_field+")"
    
    def dehydrate_videos_seen(self, bundle):
        person_id = getattr(bundle.obj, 'id')
        videos = Video.objects.filter(screening__personmeetingattendance__person__id = person_id).distinct().values('id','title')
        return list(videos)
    
    def hydrate_village(self, bundle):
        print 'in hydrate village'
        print bundle
        village = bundle.data.get('village')
        if village and not hasattr(bundle,'village_flag'):
            try:
                village_id = village.get('id')
                bundle.data['village'] = "/api/v1/village/"+str(village_id)+"/"
                bundle.village_flag = True
            except:
                print 'village id in video does not exist'
                bundle.data['village'] = None
        return bundle
    
    def hydrate_group(self, bundle):
        print 'in hydrate group'
        print bundle
        group = bundle.data.get('group')
        if group and not hasattr(bundle,'group_flag'):
            try:
                group_id = group.get('id')
                bundle.data['group'] = "/api/v1/group/"+str(group_id)+"/"
                bundle.group_flag = True
            except:
                print 'group id in video does not exist'
                bundle.data['group'] = None
        return bundle

class PersonAdoptVideoResource(ModelResource):
    person = fields.ForeignKey(PersonResource, 'person')
    video = fields.ForeignKey(VideoResource, 'video')
    group = fields.DictField(null = True)
    village = fields.DictField(null = True)
    class Meta:
        queryset = PersonAdoptPractice.objects.select_related('person__village','video').all()
        resource_name = 'adoption'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('person__village__in')
        #authorization = Authorization()
        
        excludes = ['prior_adoption_flag', 'quality', 'quantity', 'quantity_unit', 'time_created', 'time_modified']
    dehydrate_video = partial(foreign_key_to_id, field_name='video',sub_field_names=['id','title'])
    dehydrate_person = partial(foreign_key_to_id, field_name='person',sub_field_names=['id','person_name'])
    
    def dehydrate_group(self, bundle):
        person_id = getattr(bundle.obj, 'person').id
        t_dict = {}
        group = Person.objects.get(id = person_id).group
        if group:
            t_dict["id"] = group.id
            t_dict["group_name"] = group.group_name
        else:
            t_dict["id"] = None
            t_dict["group_name"] = None
        return t_dict
    
    def dehydrate_village(self, bundle):
        person_id = getattr(bundle.obj, 'person').id
        t_dict = {}
        village = Person.objects.get(id=person_id).village
        t_dict["id"] = village.id
        t_dict["village_name"] = village.village_name
        return t_dict
    
    def hydrate_video(self, bundle):
        print 'in hydrate video'
        print bundle
        video = bundle.data.get('video')
        if video and not hasattr(bundle,'video_flag'):
            try:
                video_id = video.get('id')
                bundle.data['video'] = "/api/v1/video/"+str(video_id)+"/"
                bundle.video_flag = True
            except:
                print 'video id in pap does not exist'
                bundle.data['video'] = None
        return bundle
    
    def hydrate_person(self, bundle):
        print 'in hydrate person'
        print bundle
        person = bundle.data.get('person')
        if person and not hasattr(bundle,'person_flag'):
            try:
                person_id = person.get('id')
                bundle.data['person'] = "/api/v1/person/"+str(person_id)+"/"
                bundle.person_flag = True
            except:
                print 'person id in person adopt video does not exist'
                bundle.data['person'] = None
        return bundle
    

# Disallow POST PUT DELETE
# Get Id and String

class FieldOfficerResource(ModelResource):
    class Meta:
        queryset = FieldOfficer.objects.all()
        resource_name = 'field_officer'
        authentication = BasicAuthentication()
        authorization = Authorization()
      
# class BlockResource(ModelResource):
#     district = fields.ForeignKey(DistrictResource, 'district')
#     class Meta:
#         queryset = Block.objects.all()
#         resource_name = 'block'
#         authentication = BasicAuthentication()
#         authorization = DjangoAuthorization()
#         ordering = ["start_date","block_name","district"]
#         filtering = {
#         'block_name': ALL,
#         'district':ALL_WITH_RELATIONS,
#         'start_date': ALL,
#         }
#         always_return_data = True
#         validation = ModelFormValidation(form_class=BlockForm)

class PartnersResource(ModelResource):    
    class Meta:
        queryset = Partners.objects.all()
        resource_name = 'partner'
        authentication = BasicAuthentication()
        authorization = Authorization()
        

class LanguageResource(ModelResource):    
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'
        authentication = BasicAuthentication()
        authorization = Authorization()
        

class PersonMeetingAttendanceResource(ModelResource):    
    class Meta:
        queryset = PersonMeetingAttendance.objects.all()
        resource_name = 'pma'
        authentication = BasicAuthentication()
        authorization = Authorization()
        
