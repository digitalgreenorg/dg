from django.conf.urls.defaults import patterns, include, url
from django.core.paginator import Paginator, InvalidPage
from django.forms.models import ModelChoiceField
from django.http import Http404
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.validation import FormValidation
from tastypie.utils import trailing_slash
from haystack.query import SearchQuerySet
from functools import partial
from dashboard.models import Country,State,District,Block,Village,FieldOfficer,Partners,Video,PersonGroups,Screening,Animator,Person,PersonAdoptPractice,UserPermission
from forms import  CountryForm,StateForm,DistrictForm,BlockForm,VillageForm,FieldOfficerForm,PartnerForm
from django.forms.models import model_to_dict

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
        form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors


def many_to_many_to_subfield(bundle, field_name,sub_field_names):
    sub_fields = getattr(bundle.obj, field_name).values(*sub_field_names)
    return list(sub_fields)

def foreign_key_to_id(bundle, field_name,sub_field_names):
    field = getattr(bundle.obj, field_name)
    if(field == None):
        return
    dict = model_to_dict(field, fields= sub_field_names, exclude=[])
    return dict

def get_user_villages(request):
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


class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","country_name"]
        filtering = {
        'country_name': ALL,
        'start_date':ALL,
        }
        always_return_data = True
        validation = FormValidation(form_class=CountryForm)
    
    
class StateResource(ModelResource):
    country = fields.ForeignKey(CountryResource, 'country')
    class Meta:
        queryset = State.objects.all()
        resource_name = 'state'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","state_name","region","country"]
        filtering = {
        'state_name': ALL,
        'start_date': ALL,
        'region':ALL,
        'country':ALL_WITH_RELATIONS,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=StateForm)
    
    def override_urls(self):
        return [
        url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(State).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class DistrictResource(ModelResource):
    state = fields.ForeignKey(StateResource, 'state')
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        #fields=["start_date","state","district_name","id"]
        ordering = ["start_date","state","district_name"]
        filtering = {
        'district_name': ALL,
        'state':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=DistrictForm)
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(District).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class BlockResource(ModelResource):
    district = fields.ForeignKey(DistrictResource, 'district')
    class Meta:
        queryset = Block.objects.all()
        resource_name = 'block'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","block_name","district"]
        filtering = {
        'block_name': ALL,
        'district':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        always_return_data = True
        validation = ModelFormValidation(form_class=BlockForm)
    
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Block).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)
        
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []
        
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)
        
        object_list = {
            'objects': objects,
        }
        
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

class PartnersResource(ModelResource):
    class Meta:
        queryset = Partners.objects.all()
        resource_name = 'partner'
        authentication = BasicAuthentication()
        
class AnimatorResource(ModelResource):
    village = fields.ForeignKey('dashboard.api.VillageResource', 'village')
    #    village_name = fields.CharField('village__village_name')
    #    village_id = fields.CharField('village__id')
    partner = fields.ForeignKey(PartnersResource, 'partner')
    #    partner_name = fields.CharField('partner__partner_name')
    #    partner_id = fields.CharField('partner__id')
    class Meta:
        queryset = Animator.objects.select_related('village','partner').all()
        resource_name = 'animator'
        authentication = BasicAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    dehydrate_partner = partial(foreign_key_to_id, field_name='partner',sub_field_names=['id','partner_name'])
# add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(village__in= villages)



class VillageResource(ModelResource):
    block_name = fields.CharField('block__block_name')
    district_name= fields.CharField('block__district__district_name')
    state_name = fields.CharField('block__district__state__state_name')
    country_name = fields.CharField('block__district__state__country__country_name')
    animators = fields.ToManyField(AnimatorResource, 'animators', related_name='village')
    class Meta:
        queryset = Village.objects.select_related('block__district__state__country').all()
        resource_name = 'village'
        authentication = BasicAuthentication()
        max_limit = None
    
    dehydrate_animators = partial(many_to_many_to_subfield, field_name='animators',sub_field_names=['id'])
    # add appropriate authorization

    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(id__in= villages)



class VideoResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
    class Meta:
        queryset = Video.objects.select_related('village').all()
        resource_name = 'video'
        authentication = BasicAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    # add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        vids = list(Screening.objects.filter(village__in=villages).values_list('videoes_screened',flat=True))
        return object_list.filter(id__in= vids )


class PersonGroupsResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
#    village_name = fields.CharField('village__village_name')
#    village_id = fields.CharField('village__id')
    class Meta:
        queryset = PersonGroups.objects.select_related('village').all()
        resource_name = 'persongroup'
        authentication = BasicAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
# add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(village__in= villages)


class ScreeningResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
#    village_name = fields.CharField('village__village_name')
#    village_id = fields.CharField('village__id')
    videos_screened = fields.ToManyField(VideoResource, 'videoes_screened', related_name='screening')
    person_groups = fields.ToManyField(VideoResource, 'farmer_groups_targeted', related_name='screening')
    person_attendance = fields.ToManyField('dashboard.api.PersonResource', 'farmers_attendance', related_name='screening')
    #field_officer = fields.CharField('fieldofficer__name')
    class Meta:
        queryset = Screening.objects.select_related('village').all()
        resource_name = 'screening'
        authentication = BasicAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    dehydrate_videos_screened = partial(many_to_many_to_subfield, field_name='videoes_screened',sub_field_names=['id','title'])
    dehydrate_person_groups = partial(many_to_many_to_subfield, field_name='farmer_groups_targeted',sub_field_names=['id','group_name'])
    dehydrate_person_attendance = partial(many_to_many_to_subfield, field_name='farmers_attendance',sub_field_names=['id'])
# add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(village__in= villages)


class PersonResource(ModelResource):
    village = fields.ForeignKey(VillageResource, 'village')
#    village_name = fields.CharField('village__village_name')
#    village_id = fields.CharField('village__id')
    person_group = fields.ForeignKey(PersonGroupsResource, 'group',null=True)
    #person_group_name = fields.CharField('group__group_name')
    #person_group_id = fields.CharField('group__id')
    screenings_attended = fields.ToManyField(ScreeningResource, 'screenings_attended', related_name='person')
    
    class Meta:
        queryset = Person.objects.select_related('village','group').all()
        resource_name = 'person'
        authentication = BasicAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village',sub_field_names=['id','village_name'])
    dehydrate_person_group = partial(foreign_key_to_id, field_name='group',sub_field_names=['id','group_name'])
    dehydrate_screenings_attended = partial(many_to_many_to_subfield, field_name='screenings_attended',sub_field_names=['id'])
# add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(village__in= villages)



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
    dehydrate_video = partial(foreign_key_to_id, field_name='video',sub_field_names=['id','title'])
    dehydrate_person = partial(foreign_key_to_id, field_name='person',sub_field_names=['id','person_name','village.village_name'])
# add appropriate authorization
    def apply_authorization_limits(self, request, object_list):
        villages = get_user_villages(request)
        return object_list.filter(person__village__in= villages)


class FieldOfficerResource(ModelResource):
    class Meta:
        queryset = FieldOfficer.objects.all()
        resource_name = 'field_officer'
        authentication = BasicAuthentication()
       



