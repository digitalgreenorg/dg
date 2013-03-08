from django.conf.urls.defaults import patterns, include, url
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import FormValidation
from tastypie.validation import Validation
from functools import partial
from dashboard.models import Country, State, District, Block, Village, FieldOfficer,Partners, \
                Video, PersonGroups, Screening, Animator, Person, PersonAdoptPractice, UserPermission, Language, PersonMeetingAttendance
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
        
        # convert everything to lists
        #multiple = not isinstance(uri, basestring)
        #uris = uri if multiple else [uri]
        converted = []
        if type(uri) == type(dict()):
            print 'dict'
            converted.append(uri.get('id'))
            return uri.get('id')
        elif type(uri) == type(list()):
            print 'list'
            for item in uri:
                print item.get('id')
                converted.append(item.get('id'))
            return converted
#        print uris
#        print uris.get('id')
#        
#        converted.append(uris.get('id'))
#        # handle all passed URIs
#        
#        for one_uri in uris:
#            print one_uri
#            try:
#                # hopefully /api/v1/<resource_name>/<pk>/
#                converted.append(int(one_uri.split('/')[-2]))
#            except (IndexError, ValueError):
#                raise ValueError(
#                                 "URI %s could not be converted to PK integer." % one_uri)
        
        # convert back to original format
       # return converted if multiple else converted[0]
    
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
        return object_list.filter(**kwargs)


class MediatorResource(ModelResource):
    mediator_label = fields.CharField()
    assigned_villages = fields.ToManyField('dashboard.api.VillageResource', 'assigned_villages')
    partner = fields.ForeignKey('dashboard.api.PartnerResource', 'partner')
    
    class Meta:
        queryset = Animator.objects.all()
        resource_name = 'mediator'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        validation = ModelFormValidation(form_class=AnimatorForm)
        excludes = ['total_adoptions','time_created', 'time_modified' ]
    dehydrate_assigned_villages = partial(many_to_many_to_subfield, field_name='assigned_villages',sub_field_names=['id', 'village_name'])
    dehydrate_partner = partial(foreign_key_to_id, field_name='partner',sub_field_names=['id','partner_name'])
    
    def hydrate(self, bundle):
        print bundle
    
    def apply_authorization_limits(self, request, object_list):
        districts = get_user_districts(request)
        #get partner first
        partner = Partners.objects.filter(district__in = districts)
        if partner:
            partner = partner[0]
        animators = Animator.objects.filter(partner__in = [partner]).values_list('id', flat=True)
        return object_list.filter(id__in= animators)

    
    def dehydrate_mediator_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'assigned_villages').all().distinct()
        label = ""
        for i in v_field:
            label = label + i.village_name + ","
        return "("+ label +")"
    
    def hydrate_partner(self, bundle):
        print 'in hydrate partner'
        print bundle
        partner = bundle.data.get('partner')
        if partner and not hasattr(bundle,'partner_flag'):
            try:
                id = partner.get('id')
                bundle.data['partner'] = "/api/v1/partner/"+str(id)+"/"
                bundle.partner_flag = True
            except:
                print 'partner id in video does not exist'
                bundle.data['partner'] = None
        return bundle

    
    def hydrate_assigned_villages(self, bundle):
        print 'in hydrate assigned villlages'
        m2m_list = bundle.data.get('assigned_villages')
        resource_uri_list = []
        for item in m2m_list:
            try:
                resource_uri_list.append("/api/v1/village/"+str(item.get('id'))+"/")
            except:
                continue
                print 'in exception'
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
        validation = ModelFormValidation(form_class=VideoForm)
        excludes = ['viewers','time_created', 'time_modified', 'duration' ]
    
    def apply_authorization_limits(self, request, object_list):
        districts = get_user_districts(request)
        screened_vids = list(Screening.objects.filter(village__block__district__in=districts).distinct().values_list('videoes_screened__id',flat=True))
        produced_vids = list(Video.objects.filter(village__block__district__in = districts).values_list('id', flat=True))
        #doing set of two lists avoid merging duplicates in the final merged list
        vids = list(set(screened_vids + produced_vids))
        return object_list.filter(id__in= vids)

    def hydrate_language(self, bundle):
        print 'in hydrate language'
        print bundle
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
    
    def hydrate_cameraoperator(self, bundle):
        print 'in hydrate camera operator'
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
        print 'in hydrate facilitator'
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
        print 'in hydrate farmers shown'
        m2m_list = bundle.data.get('farmers_shown')
        resource_uri_list = []
        for item in m2m_list:
            try:
                resource_uri_list.append("/api/v1/person/"+str(item.get('id'))+"/")
            except:
                continue
                print 'in exception'
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
        validation = ModelFormValidation(form_class=PersonGroupsForm)
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id'])
    
    def dehydrate_group_label(self,bundle):
        #for sending out label incase of dropdowns
        v_field = getattr(bundle.obj, 'village').village_name
        g_field = getattr(bundle.obj, 'group_name')
        return "("+ g_field+"," + v_field +")"

class ScreeningResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
    animator = fields.ForeignKey(MediatorResource, 'animator')
#    village_name = fields.CharField('village__village_name')
#    village_id = fields.CharField('village__id')
    videoes_screened = fields.ToManyField('dashboard.api.VideoResource', 'videoes_screened', related_name='screening')
    farmer_groups_targeted = fields.ToManyField('dashboard.api.PersonGroupsResource', 'farmer_groups_targeted', related_name='screening')
    farmers_attendance = fields.ToManyField('dashboard.api.PersonResource', 'farmers_attendance', related_name='screening')
#    #field_officer = fields.CharField('fieldofficer__name')
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
#    dehydrate_animator = partial(foreign_key_to_id, field_name='animator',sub_field_names=['id','name'])
#    dehydrate_videoes_screened = partial(many_to_many_to_subfield, field_name='videoes_screened',sub_field_names=['id','title'])
#    dehydrate_farmer_groups_targeted = partial(many_to_many_to_subfield, field_name='farmer_groups_targeted',sub_field_names=['id','group_name'])
#    dehydrate_farmers_attendance = partial(many_to_many_to_subfield, field_name='farmers_attendance',sub_field_names=['personmeetingattendance__id',
#                                                                                                                     'id', 
#                                                                                                                     'person_name',
#                                                                                                                     'personmeetingattendance__interested',
#                                                                                                                     'personmeetingattendance__expressed_question',
#                                                                                                                     'personmeetingattendance__expressed_adoption_video'])

    class Meta:
        queryset = Screening.objects.select_related('village').all()
        resource_name = 'screening'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('village__in')
        #validation = ModelFormValidation(form_class = ScreeningForm)
    
    def hydrate_videoes_screened(self, bundle):
        groups = bundle.data.get('videoes_screened')
        resource_uri_list = []
        for group in groups:
            try:
                resource_uri_list.append("/api/v1/video/"+str(group.get('id'))+"/")
            except:
                continue
                print 'in exception'
        bundle.data['videoes_screened'] = resource_uri_list
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
        bundle.data['farmer_groups_targeted'] = resource_uri_list
        return bundle
    
    def hydrate_farmers_attendance(self, bundle):
        print 'in farmers attendance'
        pmas = bundle.data['farmers_attendance']
        resource_uri_list = []
        for pma in pmas:
            #print pma
            try:
                resource_uri_list.append("/api/v1/person/"+str(pma.get('id'))+"/")
            except:
                continue
                print 'in exception'
        bundle.data['farmers_attendance'] = resource_uri_list
        print resource_uri_list
        return bundle
    
    def save_m2m(self, bundle):
        print 'in save m2m'
        pmas = bundle.data.get('farmers_attendance', [])
        print pmas

    
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
        


#    def save_m2m(self, bundle):
#        for field_name, field_object in self.fields.items():
#            print field_name
#            print field_object
#            if not getattr(field_object, 'is_m2m', False):
#                continue
#            print "m2m"
#            if not field_object.attribute:
#                continue
#              
#            if field_object.blank:
#                continue
#            
#            if field_object.readonly:
#                continue
# 
#            # Get the manager.
#            related_mngr = getattr(bundle.obj, field_object.attribute)
#            through_class = getattr(related_mngr, 'through', None)
#            print related_mngr, through_class
##            if through_class and not through_class._meta.auto_created:
##                # ManyToMany with an explicit intermediary table.
##                # This should be handled by with specific code, so continue
##                # without modifying anything. 
##                # NOTE: this leaves the bundle.needs_save set to True
##                continue
##            
#            print "notautocreated"
# 
#            related_bundles = bundle.data[field_name]
#            print related_bundles
##            # Remove any relations that were not POSTed
##            if through_class:
##                # ManyToMany with hidden intermediary table. 
##                # Use the manager to clear out the relations.
##                related_mngr.clear()
##            else:
##                # OneToMany with foreign keys to this object. 
##                # Explicitly delete objects to pass in the user.
##                posted_pks = [b.obj.pk for b in related_bundles if b.obj.pk]
##                if self._meta.pass_request_user_to_django:
##                    for obj in related_mngr.for_user(
##                        user=bundle.request.user).exclude(pk__in=posted_pks):
##                        obj.delete(user=bundle.request.user)
##                else:
##                    for obj in related_mngr.all().exclude(pk__in=posted_pks):
##                        obj.delete()
##            
##            # Save the posted related objects
#            related_objs = []
#            for related_bundle in related_bundles:
#                print related_bundle.obj
##                related_objs.append(related_bundle.obj)
##                if related_bundle.needs_save:
##                    if self._meta.pass_request_user_to_django:
##                        related_bundle.obj.save(user=bundle.request.user)
##                    else:
##                        related_bundle.obj.save()
##                    related_bundle.needs_save = False
##            
##            if through_class:
##                # ManyToMany with hidden intermediary table. Since the save
##                # method on a hidden table can not be overridden we can use the
##                # related_mngr to add.
##                related_mngr.add(*related_objs)
##        print 'here'
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
        return videos
    
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
#    person_name = fields.CharField('person__person_name')
#    person_id = fields.CharField('person__id')
    person_village_name = fields.CharField('person__village__village_name')
#    video_name = fields.CharField('video__title')
#    video_id = fields.CharField('video__id')
    video = fields.ForeignKey(VideoResource, 'video')
    class Meta:
        queryset = PersonAdoptPractice.objects.select_related('person__village','video').all()
        resource_name = 'personadoptvideo'
        authentication = BasicAuthentication()
        authorization = VillageLevelAuthorization('person__village__in')
    dehydrate_video = partial(foreign_key_to_id, field_name='video',sub_field_names=['id','title'])
    dehydrate_person = partial(foreign_key_to_id, field_name='person',sub_field_names=['id','person_name','village.village_name'])


# Disallow POST PUT DELETE
# Get Id and String
class FieldOfficerResource(ModelResource):
    class Meta:
        queryset = FieldOfficer.objects.all()
        resource_name = 'field_officer'
        authentication = BasicAuthentication()
      
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

class LanguageResource(ModelResource):    
    class Meta:
        queryset = Language.objects.all()
        resource_name = 'language'
        authentication = BasicAuthentication()

class PersonMeetingAttendanceResource(ModelResource):    
    class Meta:
        queryset = PersonMeetingAttendance.objects.all()
        resource_name = 'pma'
        authentication = BasicAuthentication()
