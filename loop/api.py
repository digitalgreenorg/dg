from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from django.forms.models import model_to_dict
from tastypie import fields, utils
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
		queryset = Village.objects.all()
		resource_name = 'village'
		authorization = Authorization()

class FarmerResource(ModelResource):
	village = fields.ForeignKey(VillageNameResource, 'village', full=True)
	class Meta:
		queryset = Farmer.objects.all()
		resource_name = 'farmer'
		authorization = Authorization()

class LoopUserResource(ModelResource):
	user = fields.ForeignKey(UserResource, 'user')
	assigned_villages = fields.ListField()
	class Meta:
		queryset = LoopUser.objects.prefetch_related('assigned_villages','user')
		resource_name = 'loopUser'
		authorization = Authorization()
	hydrate_user = partial(dict_to_foreign_uri, field_name = 'user')
	hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m, field_name='assigned_villages', resource_name = 'village')
	dehydrate_user = partial(foreign_key_to_id, field_name='user', sub_field_names=['id','username'])
