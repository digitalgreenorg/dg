from tastypie.exceptions import ImmediateHttpResponse
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from django.forms.models import model_to_dict
from tastypie import fields, utils
from functools import partial
from django.http import  HttpResponse

import json

from django.contrib.auth.models import User
from models import *

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
        bundle.data[field_name] = "/loop/api/v1/%s/%s/"%(resource_name if resource_name else field_name, 
                                                    str(field_dict.get('id')))
    else:
        bundle.data[field_name] = None
    return bundle

def dict_to_foreign_uri_m2m(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/loop/api/v1/%s/%s/"%(resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle

class VillageAuthorization(Authorization):
    def __init__(self,field):
        self.village_field = field
    
    def read_list(self, object_list, bundle):
        villages = LoopUser.objects.get(user_id= bundle.request.user.id).get_villages()
        kwargs = {}
        kwargs[self.village_field] = villages
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.village_field] = LoopUser.objects.get(user_id= bundle.request.user.id).get_villages()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound( "Not allowed to download Village" )

class MultipartResource(object):
    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)

class UserResource(ModelResource):
   # We need to store raw password in a virtual field because hydrate method
   # is called multiple times depending on if it's a POST/PUT/PATCH request

   class Meta:
       authorization = Authorization()
       allowed_methods = ['get', 'patch', 'put', 'post']
       always_return_data = True
       queryset = User.objects.all()
       resource_name='user'
       excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                   'last_login']
       # filtering = {'username':ALL,
       #              }

class CountryResource(ModelResource):
	class Meta:
		queryset = Country.objects.all()
		resource_name = 'country'
		fields = ["country_name"]
		authorization = Authorization()

class StateResource(ModelResource):
	country = fields.ForeignKey(CountryResource, attribute='country', full=True)
	class Meta:
		queryset = State.objects.all()
		resource_name = 'state'
		fields = ["state_name"]
		authorization = Authorization()

class DistrictResource(ModelResource):
	state = fields.ForeignKey(StateResource, 'state', full=True)
	class Meta:
		queryset = District.objects.all()
		resource_name = 'district'
		fields = ["district_name"]
		authorization = Authorization()

class BlockResource(ModelResource):
	district = fields.ForeignKey(DistrictResource, 'district', full=True)
	class Meta:
		queryset = Block.objects.all()
		resource_name = 'block'
		fields = ["block_name"]
		authorization = Authorization()

class VillageResource(ModelResource):
	block = fields.ForeignKey(BlockResource, 'block', full=True)
	class Meta:
		allowed_methods = ['post','get']
		always_return_data = True
		queryset = Village.objects.all()
		resource_name = 'village'
		authorization = VillageAuthorization('id__in')
		authentication = ApiKeyAuthentication()
	dehydrate_block = partial(foreign_key_to_id, field_name='block', sub_field_names=['id','block_name'])
	hydrate_block = partial(dict_to_foreign_uri, field_name='block')

class FarmerResource(MultipartResource, ModelResource):
    village = fields.ForeignKey(VillageResource, 'village', full=True)
    image = fields.FileField(attribute='img', null=True, blank=True)
    class Meta:
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
        always_return_data = True
        authorization = VillageAuthorization('village_id__in')
        authentication = ApiKeyAuthentication()
    dehydrate_village = partial(foreign_key_to_id, field_name='village', sub_field_names=['id','village_name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')
    def obj_create(self, bundle, request=None, **kwargs):
        bundle = self.full_hydrate(bundle)
        attempt = Farmer.objects.filter(phone = bundle.data['phone'])
        print kwargs
        print bundle.data
        print bundle.data['village']
        print bundle.data['village'].split('/')[-2]
        result = {}
        if attempt.count() < 1:
            bundle.obj = Farmer(name = bundle.data['name'], phone = bundle.data['phone'], village = Village.objects.get(id = int((bundle.data['village'].split('/'))[-2])))
        else:
            raise ImmediateHttpResponse(response = HttpResponse("Duplicate : " + str(attempt[0].id), status=501))

        # print type(bundle)
        # print type(bundle.obj)
        # print bundle
        # result['id'] = bundle.obj.id
        # result['error'] = 'Duplicate Entry'
        return bundle

class LoopUserResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	assigned_villages = fields.ListField()
	class Meta:
		queryset = LoopUser.objects.prefetch_related('assigned_villages','user')
		resource_name = 'loopuser'
		authorization = Authorization()
	hydrate_user = partial(dict_to_foreign_uri, field_name = 'user')
	hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m, field_name='assigned_villages', resource_name = 'village')
	dehydrate_user = partial(foreign_key_to_id, field_name='user', sub_field_names=['id','username'])

class CropResource(ModelResource):
	class Meta:
		queryset = Crop.objects.all()
		resource_name = 'crop'
		authorization = Authorization()

class MandiResource(ModelResource):
	district = fields.ForeignKey(DistrictResource, 'district')
	class Meta:
		queryset = Mandi.objects.all()
		resource_name = 'mandi'
		authorization = Authorization()
	dehydrate_district = partial(foreign_key_to_id, field_name='district', sub_field_names=['id','district_name'])
	hydrate_district = partial(dict_to_foreign_uri, field_name='district')

class CombinedTransactionResource(ModelResource):
	aggregator = fields.ForeignKey(LoopUserResource,'aggregator')
	farmer = fields.ForeignKey(FarmerResource,'farmer')
	crop = fields.ForeignKey(CropResource,'crop')
	mandi = fields.ForeignKey(MandiResource,'mandi')
	class Meta:
		queryset = CombinedTransaction.objects.all()
		resource_name = 'combinedtransaction'
		authorization = VillageAuthorization('farmer__village_id__in')
		authentication = ApiKeyAuthentication()
	dehydrate_farmer = partial(foreign_key_to_id, field_name='farmer', sub_field_names=['id','farmer_name'])
	dehydrate_aggregator = partial(foreign_key_to_id, field_name='aggregator', sub_field_names=['id','loopuser_user_username'])
	dehydrate_crop = partial(foreign_key_to_id, field_name='crop', sub_field_names=['id','crop_name'])
	dehydrate_mandi = partial(foreign_key_to_id, field_name='mandi', sub_field_names=['id','mandi_name'])
	hydrate_farmer = partial(dict_to_foreign_uri, field_name='farmer')
	hydrate_crop = partial(dict_to_foreign_uri, field_name='crop')
	hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')
	hydrate_aggregator = partial(dict_to_foreign_uri, field_name='aggregator', resource_name='loopuser')
