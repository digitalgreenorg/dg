# -*- coding: utf-8 -*-
from tastypie.exceptions import ImmediateHttpResponse, NotFound, BadRequest
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from django.forms.models import model_to_dict
from tastypie import fields, utils
from tastypie import bundle
from functools import partial
from django import http
from tastypie.bundle import Bundle
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import json

from django.contrib.auth.models import User
from models import *

class AssignedMandiNotSaved(Exception):
    pass

class AssignedVillageNotSaved(Exception):
    pass

def send_duplicate_message(obj_id):
    response = {"error_message": {"id": obj_id, "error": "Duplicate"}}
    raise ImmediateHttpResponse(response=HttpResponse(json.dumps(response), status=500, content_type="application/json"))

def foreign_key_to_id(bundle, field_name, sub_field_names):
    field = getattr(bundle.obj, field_name)
    if (field == None):
        dict = {}
        for sub_field in sub_field_names:
            dict[sub_field] = None
    else:
        dict = model_to_dict(field, fields=sub_field_names, exclude=[])
        # dict["online_id"] = dict['id']
    return dict


def dict_to_foreign_uri(bundle, field_name, resource_name=None):
    field_dict = bundle.data.get(field_name)
    if field_dict.get('online_id'):
        bundle.data[field_name] = "/loop/api/v1/%s/%s/" % (resource_name if resource_name else field_name,
                                                           str(field_dict.get('online_id')))
    else:
        bundle.data[field_name] = None
    return bundle


def id_to_foreign_uri(bundle, field_name, resource_name=None):
    field_dict = bundle.data.get(field_name)
    if field_dict:
        bundle.data[field_name] = "/loop/api/v1/%s/%s/" % (resource_name if resource_name else field_name,
                                                           str(field_dict))
    else:
        bundle.data[field_name] = None
    return bundle


def dict_to_foreign_uri_m2m(bundle, field_name, resource_name):
    m2m_list = bundle.data.get(field_name)
    resource_uri_list = []
    for item in m2m_list:
        try:
            resource_uri_list.append("/loop/api/v1/%s/%s/" %
                                     (resource_name, str(item.get('id'))))
        except:
            return bundle
    bundle.data[field_name] = resource_uri_list
    return bundle

class LoopUserAuthorization(Authorization):
    def __init__(self, field):
        self.loopuser_field = field

    def read_list(self,object_list,bundle):
        kwargs = {}
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        aggregators = user.get_loopusers()
        kwargs[self.loopuser_field] = aggregators
        return object_list.filter(**kwargs).distinct()


class VillageAuthorization(Authorization):
    def __init__(self, field):
        self.village_field = field

    def read_list(self, object_list, bundle):
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        districts =District.objects.filter(adminassigneddistrict__admin_user_id=user,adminassigneddistrict__aggregation_switch=True)
        villages = Village.objects.filter(block__district__in=districts)
        kwargs = {}
        kwargs[self.village_field] = villages
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        districts =District.objects.filter(adminassigneddistrict__admin_user_id=user,adminassigneddistrict__aggregation_switch=True)
        villages = Village.objects.filter(block__district__in=districts)
        kwargs = {}
        kwargs[self.village_field] = villages
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Village")

class CropLanguageAuthorization(Authorization):
    def __init__(self, field):
        self.croplanguage_field = field

    def read_list(self, object_list, bundle):
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language
        croplanguage = CropLanguage.objects.filter(language=preferred_language)
        kwargs = {}
        kwargs[self.croplanguage_field] = croplanguage
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language
        croplanguage = CropLanguage.objects.filter(language=preferred_language)
        kwargs = {}
        kwargs[self.croplanguage_field] = croplanguage
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download CropLanguage")

class VehicleLanguageAuthorization(Authorization):
    def __init__(self, field):
        self.vehiclelanguage_field = field

    def read_list(self, object_list, bundle):
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language
        vehiclelanguage = VehicleLanguage.objects.filter(language=preferred_language)
        kwargs = {}
        kwargs[self.vehiclelanguage_field] = vehiclelanguage
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language
        vehiclelanguage = VehicleLanguage.objects.filter(language=preferred_language)
        kwargs = {}
        kwargs[self.vehiclelanguage_field] = vehiclelanguage
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download CropLanguage")

class DistrictAuthorization(Authorization):
    def __init__(self, field):
        self.district_field = field

    def read_list(self, object_list, bundle):
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        kwargs = {}
        kwargs[self.district_field] = districts
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        kwargs = {}
        kwargs[self.district_field] = districts
        obj=object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download District")

class BlockAuthorization(Authorization):
    def __init__(self, field):
        self.block_field = field

    def read_list(self, object_list, bundle):
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        kwargs = {}
        kwargs[self.block_field] = Block.objects.filter(district__in=districts)
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        kwargs = {}
        kwargs[self.block_field] = Block.objects.filter(district__in=districts)
        obj=object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Block")


class MandiAuthorization(Authorization):
    def __init__(self, field):
        self.mandi_field = field

    def read_list(self, object_list, bundle):
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        mandis_list = {}
        mandis_list[self.mandi_field] = Mandi.objects.filter(district__in=districts)
        return object_list.filter(**mandis_list).distinct()

    def read_details(self, object_list, bundle):
        districts  = AdminUser.objects.get(user_id=bundle.request.user.id).get_districts()
        mandis_list = {}
        mandi_list[self.mandi_field] = Mandi.objects.filter(district__in=districts)
        obj = object_list.filter(**mandis_list).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Mandi")


class CombinedTransactionAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user_created_id=bundle.request.user.id).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        obj = object_list.filter(
            user_created_id=bundle.request.user.id).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Transaction")


class DayTransportationAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user_created_id=bundle.request.user.id).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        obj = object_list.filter(
            user_created_id=bundle.request.user.id).distinct()
        userObject = LoopUser.objects.get(user_id=bundle.request.user.id)
        if obj or userObject.role == 1:
            return True
        else:
            raise NotFound("Not allowed to download Transportations")


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

        self.authorized_create_detail(
            self.get_object_list(bundle.request), bundle)
        bundle = self.full_hydrate(bundle)
        bundle.obj.user_created_id = bundle.request.user.id
        return self.save(bundle)


class UserResource(ModelResource):
    # We need to store raw password in a virtual field because hydrate method
    # is called multiple times depending on if it's a POST/PUT/PATCH request

    class Meta:
        authorization = Authorization()
        allowed_methods = ['get', 'patch', 'put', 'post']
        always_return_data = True
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                    'last_login']
       



class CountryResource(BaseResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        fields = ["country_name"]
        authorization = Authorization()


class StateResource(BaseResource):
    country = fields.ForeignKey(
        CountryResource, attribute='country', full=True)

    class Meta:
        queryset = State.objects.all()
        resource_name = 'state'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_country = partial(
        foreign_key_to_id, field_name='country', sub_field_names=['id'])
    hydrate_country = partial(dict_to_foreign_uri, field_name='country')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class DistrictResource(BaseResource):
    state = fields.ForeignKey(StateResource, 'state', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        queryset = District.objects.all()
        resource_name = 'district'
        authorization = DistrictAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_state = partial(
        foreign_key_to_id, field_name='state', sub_field_names=['id'])
    hydrate_state = partial(dict_to_foreign_uri, field_name='state')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class BlockResource(BaseResource):
    district = fields.ForeignKey(DistrictResource, 'district', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Block.objects.all()
        resource_name = 'block'
        authorization = BlockAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_district = partial(
        foreign_key_to_id, field_name='district', sub_field_names=['id'])
    hydrate_district = partial(dict_to_foreign_uri, field_name='district')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class VillageResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ['post', 'get','put']
        always_return_data = True
        queryset = Village.objects.all()
        resource_name = 'village'
        authorization = VillageAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id'])
    hydrate_block = partial(dict_to_foreign_uri, field_name='block')

    def obj_create(self, bundle, request=None, **kwargs):
        block_id = bundle.data['block']['online_id']
        block = Block.objects.get(id=block_id)
        attempt = Village.objects.filter(village_name=bundle.data['village_name'],block=block)
        if attempt.count() < 1:
            bundle = super(VillageResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(VillageResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            block_id = bundle.data['block']['online_id']
            block = Block.objects.get(id=block_id)
            attempt = Village.objects.filter(village_name=bundle.data['village_name'],block=block)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['farmer_count'] = Farmer.objects.filter(village=bundle.data['id']).count()
        return bundle


class FarmerResource(BaseResource):
    village = fields.ForeignKey(VillageResource, 'village', full=True)
    image = fields.FileField(attribute='img', null=True, blank=True)

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ["get", "post", "put", "delete"]
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
        always_return_data = True
        authorization = VillageAuthorization('village_id__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id'])
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')

    def obj_create(self, bundle, request=None, **kwargs):
        village = Village.objects.get(id=bundle.data["village"]["online_id"])
        attempt = Farmer.objects.filter(
            phone=bundle.data['phone'], name=bundle.data['name'], village=village)
        if attempt.count() < 1:
            bundle = super(FarmerResource, self).obj_create(bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(FarmerResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            village = Village.objects.get(id=bundle.data["village"]["online_id"])
            attempt = Farmer.objects.filter(
                phone=bundle.data['phone'], name=bundle.data['name'], village=village)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['image_path'] = bundle.data['name'] + bundle.data['phone']
        return bundle

class LanguageResource(BaseResource):
    class Meta:
        limit = 0
        max_limit = 0
        queryset = Language.objects.all()
        resource_name = 'language'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class PartnerResource(BaseResource):
    class Meta:
        limit = 0
        max_limit = 0
        queryset = Partner.objects.all()
        allowed_methods = ['get']
        always_return_data = True
        resource_name = 'partner'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        del bundle.data['id']
        return bundle

class LoopUserResource(BaseResource):
    user = fields.ForeignKey(UserResource, 'user')
    village = fields.ForeignKey(VillageResource, 'village')
    preferred_language = fields.ForeignKey(LanguageResource,'preferred_language')
    partner = fields.ForeignKey(PartnerResource,'partner')
    assigned_villages = fields.ListField()
    assigned_mandis = fields.ListField()

    class Meta:
        limit = 0
        max_limit = 0
        queryset = LoopUser.objects.prefetch_related(
            'assigned_villages', 'assigned_mandis','user').all()
        resource_name = 'loopuser'
        allowed_methods=['get','put','post']
        authorization = LoopUserAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        include_resource_uri = False
        excludes =('time_created','time_modified','registration','version','preferred_language')

    hydrate_user = partial(dict_to_foreign_uri, field_name='user')
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')
    hydrate_preferred_language = partial(dict_to_foreign_uri,field_name='preferred_language')
    hydrate_partner = partial(dict_to_foreign_uri,field_name='partner')
  
    dehydrate_user = partial(
         foreign_key_to_id, field_name='user', sub_field_names=['id', 'username'])
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    dehydrate_partner = partial(foreign_key_to_id,field_name='partner',sub_field_names=['id'])
    dehydrate_preferred_language = partial(foreign_key_to_id,field_name='preferred_language',sub_field_names=['id'])

    def obj_create(self, bundle, **kwargs):
        attempt = LoopUser.objects.filter(name=bundle.data['name'],phone_number=bundle.data['phone_number'])
        user = None
        try:
            user = User.objects.get(username=bundle.data['username'])
        except:
            pass
        if attempt.count() < 1:
            if user is None:
                try:
                    user = User.objects.create_user(username=bundle.data['username'],password=bundle.data['password'],first_name=bundle.data['name_en'])
                except:
                    pass
            bundle.data['user']={}
            bundle.data['user']['online_id']=user.id
            adminUser= AdminUser.objects.get(user_id=bundle.request.user.id)
            bundle.data['preferred_language']={}
            bundle.data['preferred_language']['online_id']= adminUser.preferred_language.id
            bundle = super(LoopUserResource, self).obj_create(bundle, **kwargs)
            AdminAssignedLoopUser(admin_user=adminUser,loop_user=bundle.obj).save()
        
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, **kwargs):
        # Edit case many to many handling. First clear out the previous related objects and create new objects
        user = None
        try:
            user = User.objects.get(username=bundle.data['username'])
        except:
            pass
        #attempt = LoopUser.objects.filter(name=bundle.data['name'],phone_number=bundle.data['phone_number'])
        try:
            if user is None:
                user = User.objects.create_user(username=bundle.data['username'],password=bundle.data['password'],first_name=bundle.data['name_en'])
            bundle.data['user']={}
            bundle.data['user']['online_id']=user.id
            adminUser= AdminUser.objects.get(user_id=bundle.request.user.id)
            bundle.data['preferred_language']={}
            bundle.data['preferred_language']['online_id']= adminUser.preferred_language.id
            bundle = super(LoopUserResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = LoopUser.objects.filter(id=bundle.data['online_id'])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate_assigned_mandis(self, bundle):
        return [{'row_id':assigned_mandi_obj.id, 'id': assigned_mandi_obj.mandi.id ,'mandi_name':assigned_mandi_obj.mandi.mandi_name} for assigned_mandi_obj in
                set(LoopUserAssignedMandi.objects.select_related('mandi').filter(loop_user=bundle.obj))]

    def dehydrate_assigned_villages(self, bundle):

        return [{'row_id': assigned_village_obj.id,'id': assigned_village_obj.village.id,'village_name':assigned_village_obj.village.village_name} for assigned_village_obj in
                set(LoopUserAssignedVillage.objects.select_related('village').filter(loop_user=bundle.obj))]

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class LoopUserAssignedVillageResource(BaseResource):
    aggregator = fields.ForeignKey(LoopUserResource, 'loop_user')
    village = fields.ForeignKey(VillageResource, 'village')
    
    class Meta:
        limit = 0
        max_limit = 0
        always_return_data = True
        queryset = LoopUserAssignedVillage.objects.all()
        allowed_methods = ['get','post', 'put','delete']
        resource_name = 'loopuserassignedvillage'
        authorization = LoopUserAuthorization('loop_user__in')
        authentication = ApiKeyAuthentication()
        include_resource_uri = False
        excludes =('time_created','time_modified','user_created','user_modified')
    
    dehydrate_aggregator = partial(foreign_key_to_id, field_name='loop_user', sub_field_names=['id'])
    dehydrate_village = partial(foreign_key_to_id,field_name='village',sub_field_names=['id'])

    hydrate_aggregator = partial(dict_to_foreign_uri, field_name="aggregator", resource_name="loopuser")
    hydrate_village = partial(dict_to_foreign_uri, field_name="village")

    def obj_create(self, bundle, **kwargs):
        loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
        village_ = Village.objects.get(id=bundle.data['village']['online_id'])
        attempt = LoopUserAssignedVillage.objects.filter(loop_user=loop_user ,village=village_)
        if attempt.count() < 1:
            bundle = super(LoopUserAssignedVillageResource,self).obj_create(bundle,**kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        try:
            loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
            village = Village.objects.get(id=bundle.data['village']['online_id'])
            assignedVillage = LoopUserAssignedMandi.objects.filter(loop_user=loop_user,mandi=mandi)
            assignedVillage.is_visible = False
            assignedVillage.save()
            # bundle = super(LoopUserAssignedVillageResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
            village_ = Village.objects.get(id=bundle.data['village']['online_id'])
            attempt = LoopUserAssignedVillage.objects.filter(loop_user=loop_user ,village=village_)
            send_duplicate_message(int(attempt[0].id))
        return bundle
    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        return bundle
    
class CropResource(BaseResource):

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Crop.objects.all()
        allowed_methods = ['post', 'get', 'put']
        resource_name = 'crop'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Crop.objects.filter(crop_name=bundle.data['crop_name'])
        if attempt.count() < 1:
            bundle = super(CropResource, self).obj_create(bundle, **kwargs)
            # CropLanguage(language=language,crop=bundle.obj,crop_name=crop_name_reg).save()
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(CropResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = Crop.objects.filter(crop_name=bundle.data['crop_name'])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class CropLanguageResource(BaseResource):
    language = fields.ForeignKey(LanguageResource,'language')
    crop = fields.ForeignKey(CropResource,'crop')
    class Meta:
        limit = 0
        max_limit = 0
        queryset = CropLanguage.objects.all()
        allowed_methods = ['post', 'get','put']
        resource_name = 'croplanguage'
        authorization = CropLanguageAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    dehydrate_language = partial(
        foreign_key_to_id, field_name='language', sub_field_names=['id','notation'])
    dehydrate_crop = partial(foreign_key_to_id,field_name='crop',sub_field_names=['id'])
    hydrate_crop = partial(dict_to_foreign_uri, field_name='crop')

    def obj_create(self,bundle,request=None,**kwargs):
        preferred_language = AdminUser.objects.get(user_id=bundle.request.user.id).preferred_language.id
        bundle.data['language'] = "/loop/api/v1/language/%s/" % preferred_language 
        attempt = CropLanguage.objects.filter(crop_id=bundle.data['crop']['online_id'],language=preferred_language)
        if attempt.count() < 1:
            bundle = super(CropLanguageResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle
    def obj_update(self, bundle, request=None, **kwargs):
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language.id
        bundle.data['language'] = "/loop/api/v1/language/%s/" % preferred_language
        try:
            bundle = super(CropLanguageResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = CropLanguage.objects.filter(crop_id=bundle.data['crop']['online_id'],language=preferred_language)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self,bundle):
         bundle.data['online_id']= bundle.data['id']
         return bundle

class MandiTypeResource(BaseResource):

    class Meta:
        limit = 0
        max_limit = 0
        queryset = MandiType.objects.all()
        resource_name = 'mandi_type'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class MandiResource(BaseResource):
    district = fields.ForeignKey(DistrictResource, 'district')
    mandi_type = fields.ForeignKey(MandiTypeResource, 'mandi_type', null=True)

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ['post', 'get','put']
        always_return_data = True
        queryset = Mandi.objects.all()
        resource_name = 'mandi'
        authorization = MandiAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_district = partial(
        foreign_key_to_id, field_name='district', sub_field_names=['id'])
    hydrate_district = partial(dict_to_foreign_uri, field_name='district')

    dehydrate_mandi_type = partial(foreign_key_to_id, field_name='mandi_type', sub_field_names=['id'])
    hydrate_mandi_type = partial(dict_to_foreign_uri, field_name='mandi_type')

    def obj_create(self, bundle, request=None, **kwargs):
        district_id = bundle.data['district']['online_id']
        district = District.objects.get(id=district_id)
        attempt = Mandi.objects.filter(mandi_name=bundle.data['mandi_name'],district=district)
        if attempt.count() < 1:
            bundle = super(MandiResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(MandiResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            district_id = bundle.data['district']['online_id']
            district = District.objects.get(id=district_id)
            attempt = Mandi.objects.filter(mandi_name=bundle.data['mandi_name'],district=district)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class GaddidarResource(BaseResource):
    mandi = fields.ForeignKey(MandiResource, 'mandi', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Gaddidar.objects.all()
        resource_name = 'gaddidar'
        authorization = MandiAuthorization('mandi_id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

        dehydrate_mandi = partial(
            foreign_key_to_id, field_name='mandi', sub_field_names=['id'])
        hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def obj_create(self, bundle, request=None, **kwargs):
        mandi_id = bundle.data['mandi']['online_id']
        mandi = Mandi.objects.get(id=mandi_id)
        attempt = Gaddidar.objects.filter(gaddidar_phone=bundle.data['gaddidar_phone'],gaddidar_name=bundle.data['gaddidar_name'],mandi=mandi)
        if attempt.count() < 1:
            bundle = super(GaddidarResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(GaddidarResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            mandi_id = bundle.data['mandi']['id']
            mandi = Mandi.objects.get(id=mandi_id)
            attempt = Gaddidar.objects.filter(gaddidar_phone=bundle.data['gaddidar_phone'],gadddiar_name=bundle.data['gaddidar_name'],mandi=mandi)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle



class VehicleResource(BaseResource):

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Vehicle.objects.all()
        resource_name = 'vehicle'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Vehicle.objects.filter(vehicle_name=bundle.data['vehicle_name'])

        if attempt.count() < 1:
            bundle = super(VehicleResource, self).obj_create(bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(VehicleResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = Vehicle.objects.filter(vehicle_name=bundle.data['vehicle_name'])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class VehicleLanguageResource(BaseResource):
    language = fields.ForeignKey(LanguageResource,'language')
    vehicle = fields.ForeignKey(VehicleResource,'vehicle')
    
    class Meta:
        limit = 0
        max_limit = 0
        queryset = VehicleLanguage.objects.all()
        allowed_methods = ['post', 'get','put']
        resource_name = 'vehiclelanguage'
        authorization = VehicleLanguageAuthorization('id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    dehydrate_language = partial(
        foreign_key_to_id, field_name='language', sub_field_names=['id','notation'])
    dehydrate_vehicle = partial(foreign_key_to_id,field_name='vehicle',sub_field_names=['id'])
    hydrate_vehicle= partial(dict_to_foreign_uri, field_name='vehicle')
    def obj_create(self,bundle,request=None,**kwargs):
        preferred_language = AdminUser.objects.get(user_id=bundle.request.user.id).preferred_language.id
        bundle.data['language'] = "/loop/api/v1/language/%s/" % preferred_language
        attempt = VehicleLanguage.objects.filter(vehicle_id=bundle.data['vehicle']['online_id'],language=preferred_language)
        if attempt.count() < 1:
            bundle = super(VehicleLanguageResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle
    def obj_update(self, bundle, request=None, **kwargs):
        user = AdminUser.objects.get(user_id=bundle.request.user.id)
        preferred_language = user.preferred_language.id
        bundle.data['language'] = "/loop/api/v1/language/%s/" % preferred_language
        try:
            bundle = super(VehicleLanguageResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = VehicleLanguage.objects.filter(vehicle_id=bundle.data['vehicle']['online_id'],language=preferred_language)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        return bundle


class TransporterResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ["get", "post", "put", "delete"]
        queryset = Transporter.objects.all()
        resource_name = 'transporter'
        authorization = BlockAuthorization('block_id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id'])

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Transporter.objects.filter(transporter_phone=bundle.data['transporter_phone'],
                                             transporter_name=bundle.data['transporter_name'])
        if attempt.count() < 1:
            bundle = super(TransporterResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(TransporterResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            attempt = Transporter.objects.filter(transporter_phone=bundle.data['transporter_phone'],
                                                 transporter_name=bundle.data['transporter_name'])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        online_id = bundle.data['id']
        if bundle.request.method=='POST':
            bundle.data.clear()
            bundle.data['online_id'] = online_id
        return bundle

    def hydrate_block(self, bundle):
        bundle.data['block'] = LoopUser.objects.get(
            user__id=bundle.request.user.id).village.block
        return bundle


class TransportationVehicleResource(BaseResource):
    transporter = fields.ForeignKey(TransporterResource, 'transporter')
    vehicle = fields.ForeignKey(VehicleResource, 'vehicle')

    class Meta:
        limit = 0
        max_limit = 0
        queryset = TransportationVehicle.objects.all()
        allowed_methods = ["get", "post", "put", "delete"]
        resource_name = 'transportationvehicle'
        authorization = BlockAuthorization('transporter__block_id__in')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_transporter = partial(foreign_key_to_id, field_name='transporter',
                                    sub_field_names=['id'])
    dehydrate_vehicle = partial(
        foreign_key_to_id, field_name='vehicle', sub_field_names=['id'])
    hydrate_transporter = partial(
        dict_to_foreign_uri, field_name='transporter')
    hydrate_vehicle = partial(dict_to_foreign_uri, field_name='vehicle')

    def obj_create(self, bundle, request=None, **kwargs):
        transporter = Transporter.objects.get(
            id=bundle.data["transporter"]["online_id"])
        vehicle = Vehicle.objects.get(id=bundle.data["vehicle"]["online_id"])
        attempt = TransportationVehicle.objects.filter(transporter=transporter, vehicle=vehicle,
                                                       vehicle_number=bundle.data["vehicle_number"])
        if attempt.count() < 1:
            try:
                bundle = super(TransportationVehicleResource,
                           self).obj_create(bundle, **kwargs)    
            except Exception, e:
                print e
            
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        transporter = Transporter.objects.get(
            id=bundle.data["transporter"]["online_id"])
        vehicle = Vehicle.objects.get(id=bundle.data["vehicle"]["online_id"])
        try:
            bundle = super(TransportationVehicleResource,
                           self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = TransportationVehicle.objects.filter(transporter=transporter, vehicle=vehicle,
                                                           vehicle_number=bundle.data["vehicle_number"])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        online_id = bundle.data['id']
        if bundle.request.method=='POST':
            bundle.data.clear()
            bundle.data['online_id'] = online_id
        return bundle

    def obj_delete(self, bundle, **kwargs):
        try:
            # get an instance of the bundle.obj that will be deleted
            deleted_obj = self.obj_get(bundle=bundle, **kwargs)
            super(TransportationVehicleResource, self).obj_delete(
                bundle, user=bundle.request.user)
        except ObjectDoesNotExist:
            raise NotFound(
                "A model instance matching the provided arguments could not be found.")
        # call the delete, deleting the obj from the database
        return deleted_obj

    def delete_detail(self, request, **kwargs):
        bundle = Bundle(request=request)

        try:
            # call our obj_delete, storing the deleted_obj we returned
            # del_obj = CombinedTransaction.objects.get(id=kwargs['pk'])
            deleted_obj = self.obj_delete(
                bundle=bundle, **self.remove_api_resource_names(kwargs))
            # build a new bundle with the deleted obj and return it in a response

            deleted_bundle = self.build_bundle(
                obj=deleted_obj, request=request)

            # deleted_bundle = self.full_dehydrate()
            # deleted_bundle = self.alter_detail_data_to_serialize(request, deleted_bundle)
            return self.create_response(request, deleted_bundle, response_class=http.HttpResponse)
        except NotFound:
            return http.Http404()


class DayTransportationResource(BaseResource):
    transportation_vehicle = fields.ForeignKey(
        TransportationVehicleResource, 'transportation_vehicle')
    mandi = fields.ForeignKey(MandiResource, 'mandi')

    class Meta:
        limit = 0
        max_limit = 0
        queryset = DayTransportation.objects.all()
        detail_allowed_methods = ["get", "post", "put", "delete","patch"]
        resource_name = 'daytransportation'
        authorization = DayTransportationAuthorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_transportation_vehicle = partial(foreign_key_to_id, field_name='transportation_vehicle', sub_field_names=[
        'id'])
    hydrate_transportation_vehicle = partial(
        dict_to_foreign_uri, field_name='transportation_vehicle', resource_name='transportationvehicle')
    dehydrate_mandi = partial(
        foreign_key_to_id, field_name='mandi', sub_field_names=['id'])
    hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def obj_create(self, bundle, request=None, **kwargs):
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        user = LoopUser.objects.get(user__username=bundle.request.user)
        if "aggregator" in bundle.data.keys():
            user = LoopUser.objects.get(id=bundle.data["aggregator"]["online_id"])
        transportationvehicle = TransportationVehicle.objects.get(
            id=bundle.data["transportation_vehicle"]["online_id"])
        attempt = DayTransportation.objects.filter(date=bundle.data[
                "date"], user_created=user.user_id, timestamp=bundle.data["timestamp"])
        if attempt.count() < 1:
            bundle = super(DayTransportationResource,
                           self).obj_create(bundle, **kwargs)
        else:
            bundle.request.method = 'put'
            bundle.request.path = bundle.request.path + \
                str(attempt[0].id) + "/"
            kwargs['pk'] = attempt[0].id
            bundle = super(DayTransportationResource,self).obj_update(bundle, **kwargs)
        #raise DayTransportationNotSaved({"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        transportationvehicle = TransportationVehicle.objects.get(
            id=bundle.data["transportation_vehicle"]["online_id"])

        try:
            bundle = super(DayTransportationResource,
                           self).obj_update(bundle, **kwargs)
        except Exception, e:
            user = LoopUser.objects.get(user__username=bundle.request.user)
            attempt = DayTransportation.objects.filter(date=bundle.data[
                "date"], user_created=user.user_id, timestamp=bundle.data["timestamp"])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        online_id = bundle.data['id']
        if bundle.request.method=='POST':
            bundle.data.clear()
            bundle.data['online_id'] = online_id
        return bundle

    def obj_delete(self, bundle, **kwargs):
        try:
            # get an instance of the bundle.obj that will be deleted
            deleted_obj = self.obj_get(bundle=bundle, **kwargs)
            super(DayTransportationResource, self).obj_delete(
                bundle, user=bundle.request.user)
        except ObjectDoesNotExist:
            raise NotFound(
                "A model instance matching the provided arguments could not be found.")
        # call the delete, deleting the obj from the database
        return deleted_obj

    def delete_detail(self, request, **kwargs):
        bundle = Bundle(request=request)

        try:
            deleted_obj = self.obj_delete(
                bundle=bundle, **self.remove_api_resource_names(kwargs))
            deleted_bundle = self.build_bundle(
                obj=deleted_obj, request=request)
            return self.create_response(request, deleted_bundle, response_class=http.HttpResponse)
        except NotFound:
            return http.Http404()

class GaddidarCommissionResource(BaseResource):
    mandi = fields.ForeignKey(MandiResource,'mandi')
    gaddidar = fields.ForeignKey(GaddidarResource,'gaddidar')
    class Meta:
        limit = 0
        max_limit = 0
        queryset = GaddidarCommission.objects.all()
        authorization = MandiAuthorization('mandi_id__in')
        authentication = ApiKeyAuthentication()
        resource_name = 'gaddidarcommission'
        always_return_data = True
        excludes = ('time_created','time_modified')
        include_resource_uri = False

    dehydrate_mandi = partial(foreign_key_to_id,field_name="mandi",sub_field_names=['id'])
    dehydrate_gaddidar = partial(foreign_key_to_id,field_name="gaddidar",sub_field_names=['id'])

    hydrate_mandi = partial(dict_to_foreign_uri,field_name='mandi')
    hydrate_gaddidar = partial(dict_to_foreign_uri,field_name='gaddidar')
    def obj_create(self, bundle, request=None, **kwargs):
        mandi_id = bundle.data['mandi']['online_id']
        mandi = Mandi.objects.get(id=mandi_id)
        gaddidar_id = bundle.data['gaddidar']['online_id']
        gaddidar = Gaddidar.objects.get(id=gaddidar_id)
        attempt = GaddidarCommission.objects.filter(start_date=bundle.data['start_date'],gaddidar=gaddidar,mandi=mandi)
        if attempt.count() < 1:
            bundle = super(GaddidarCommissionResource, self).obj_create(
                bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(GaddidarCommissionResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            mandi_id = bundle.data['mandi']['online_id']
            mandi = Mandi.objects.get(id=mandi_id)
            gaddidar_id = bundle.data['gaddidar']['online_id']
            gaddidar = Gaddidar.objects.get(id=gaddidar_id)
            attempt = GaddidarCommission.objects.filter(start_date=bundle.data['start_date'],gaddidar=gaddidar,mandi=mandi)
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class GaddidarShareOutliersResource(BaseResource):
    mandi = fields.ForeignKey(MandiResource,'mandi')
    gaddidar = fields.ForeignKey(GaddidarResource,'gaddidar')
    aggregator = fields.ForeignKey(LoopUserResource,'aggregator')
    class Meta:
        queryset =GaddidarShareOutliers.objects.all()
        allowed_methods = ['post','patch','put','get']
        authorization = Authorization()
        authentication =ApiKeyAuthentication()
        resource_name = 'gaddidarshareoutliers'
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_mandi = partial(foreign_key_to_id,field_name="mandi",sub_field_names=['id'])
    dehydrate_gaddidar = partial(foreign_key_to_id,field_name="gaddidar",sub_field_names=['id'])
    dehydrate_aggregator = partial(foreign_key_to_id,field_name="aggregator",sub_field_names=['id'])
    hydrate_mandi = partial(dict_to_foreign_uri,field_name='mandi')
    hydrate_gaddidar = partial(dict_to_foreign_uri,field_name='gaddidar')
    hydrate_aggregator = partial(dict_to_foreign_uri, field_name='aggregator',resource_name='loopuser')

    def obj_create(self,bundle,request=None,**kwargs):
        mandiObject = Mandi.objects.get(id=bundle.data['mandi']['online_id'])
        gaddidarObject = Gaddidar.objects.get(id = bundle.data['gaddidar']['online_id'])
        aggregatorObject = LoopUser.objects.get(id = bundle.data['aggregator']['online_id'])

        attempt = GaddidarShareOutliers.objects.filter(date=bundle.data['date'],mandi=mandiObject,gaddidar=gaddidarObject,aggregator=aggregatorObject)
        if attempt.count() < 1:
            bundle = super(GaddidarShareOutliersResource,self).obj_create(bundle,**kwargs)
        else:
            bundle.request.method = 'PUT'
            bundle.request.path = bundle.request.path + \
                str(attempt[0].id) + "/"
            kwargs['pk'] = attempt[0].id
            bundle = super(GaddidarShareOutliersResource,self).obj_update(bundle, **kwargs)
        return bundle

class AggregatorShareOutliersResource(BaseResource):
    mandi = fields.ForeignKey(MandiResource,'mandi')
    aggregator = fields.ForeignKey(LoopUserResource,'aggregator')
    class Meta:
        queryset =AggregatorShareOutliers.objects.all()
        allowed_methods = ['post','patch','put','get']
        resource_name = 'aggregatorshareoutliers'
        authorization = Authorization()
        authentication =ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_mandi = partial(foreign_key_to_id,field_name="mandi",sub_field_names=['id'])
    dehydrate_aggregator = partial(foreign_key_to_id,field_name="aggregator",sub_field_names=['id'])
    hydrate_mandi = partial(dict_to_foreign_uri,field_name='mandi')
    hydrate_aggregator = partial(dict_to_foreign_uri,field_name='aggregator',resource_name='loopuser')

    def obj_create(self,bundle,request=None,**kwargs):
        mandiObject = Mandi.objects.get(id=bundle.data['mandi']['online_id'])
        aggregatorObject = LoopUser.objects.get(id = bundle.data['aggregator']['online_id'])

        attempt = AggregatorShareOutliers.objects.filter(date=bundle.data['date'],mandi=mandiObject,aggregator=aggregatorObject)
        if attempt.count() < 1:
            bundle = super(AggregatorShareOutliersResource,self).obj_create(bundle,**kwargs)
        else:
            bundle.request.method = 'PUT'
            bundle.request.path = bundle.request.path + \
                str(attempt[0].id) + "/"
            kwargs['pk'] = attempt[0].id
            bundle = super(AggregatorShareOutliersResource,self).obj_update(bundle, **kwargs)
        return bundle

class CombinedTransactionResource(BaseResource):
    crop = fields.ForeignKey(CropResource, 'crop')
    farmer = fields.ForeignKey(FarmerResource, 'farmer')
    mandi = fields.ForeignKey(MandiResource, 'mandi')
    gaddidar = fields.ForeignKey(GaddidarResource, 'gaddidar')

    class Meta:
        limit = 0
        max_limit = 0
        detail_allowed_methods = ["get", "post", "put", "delete"]
        queryset = CombinedTransaction.objects.all()
        resource_name = 'combinedtransaction'
        authorization = CombinedTransactionAuthorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_farmer = partial(
        foreign_key_to_id, field_name='farmer', sub_field_names=['id'])
    dehydrate_crop = partial(
        foreign_key_to_id, field_name='crop', sub_field_names=['id'])
    dehydrate_mandi = partial(
        foreign_key_to_id, field_name='mandi', sub_field_names=['id'])
    dehydrate_gaddidar = partial(
        foreign_key_to_id, field_name='gaddidar', sub_field_names=['id'])

    hydrate_farmer = partial(dict_to_foreign_uri, field_name='farmer')
    hydrate_crop = partial(dict_to_foreign_uri, field_name='crop')
    hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')
    hydrate_gaddidar = partial(dict_to_foreign_uri, field_name='gaddidar')

    def obj_create(self, bundle, request=None, **kwargs):
        farmer = Farmer.objects.get(id=bundle.data["farmer"]["online_id"])
        crop = Crop.objects.get(id=bundle.data["crop"]["online_id"])
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        gaddidar = Gaddidar.objects.get(id=bundle.data["gaddidar"]["online_id"])

        user = LoopUser.objects.get(user__username=bundle.request.user)
        attempt = CombinedTransaction.objects.filter(date=bundle.data[
                                                     "date"], user_created=user.user_id, timestamp=bundle.data["timestamp"])
        if attempt.count() < 1:
            bundle = super(CombinedTransactionResource,self).obj_create(bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        farmer = Farmer.objects.get(id=bundle.data["farmer"]["online_id"])
        crop = Crop.objects.get(id=bundle.data["crop"]["online_id"])
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        gaddidar = Gaddidar.objects.get(id=bundle.data["gaddidar"]["online_id"])

        try:
            bundle = super(CombinedTransactionResource,
                           self).obj_update(bundle, **kwargs)
        except Exception, e:
            user = LoopUser.objects.get(user__username=bundle.request.user)
            attempt = CombinedTransaction.objects.filter(date=bundle.data[
                                                         "date"], user_created=user.user_id, timestamp=bundle.data["timestamp"])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        online_id = bundle.data['id']
        if bundle.request.method=='POST':
            bundle.data.clear()
            bundle.data['online_id'] = online_id
        return bundle

    def obj_delete(self, bundle, **kwargs):
        try:
            # get an instance of the bundle.obj that will be deleted
            deleted_obj = self.obj_get(bundle=bundle, **kwargs)
            super(CombinedTransactionResource, self).obj_delete(
                bundle, user=bundle.request.user)
        except ObjectDoesNotExist:
            raise NotFound(
                "A model instance matching the provided arguments could not be found.")
        # call the delete, deleting the obj from the database
        return deleted_obj

    def delete_detail(self, request, **kwargs):
        bundle = Bundle(request=request)

        try:
            # call our obj_delete, storing the deleted_obj we returned
            deleted_obj = self.obj_delete(
                bundle=bundle, **self.remove_api_resource_names(kwargs))
            # build a new bundle with the deleted obj and return it in a response
            deleted_bundle = self.build_bundle(
                obj=deleted_obj, request=request)
            return self.create_response(request, deleted_bundle, response_class=http.HttpResponse)
        except NotFound:
            return http.Http404()

class LoopUserAssignedMandiResource(BaseResource):
    aggregator = fields.ForeignKey(LoopUserResource, 'loop_user')
    mandi = fields.ForeignKey(MandiResource, 'mandi')
    
    class Meta:
        limit = 0
        max_limit = 0
        queryset = LoopUserAssignedMandi.objects.all()
        allowed_methods = ['get','post', 'put','delete']
        always_return_data = True
        resource_name = 'loopuserassignedmandi'
        authorization = LoopUserAuthorization('loop_user__in')
        authentication = ApiKeyAuthentication()
        include_resource_uri = False
        excludes =('time_created','time_modified','user_created','user_modified')
    
    dehydrate_aggregator = partial(foreign_key_to_id, field_name="loop_user", sub_field_names=["id"])
    dehydrate_mandi = partial(foreign_key_to_id,field_name="mandi", sub_field_names=["id"])

    hydrate_aggregator = partial(dict_to_foreign_uri, field_name="aggregator", resource_name="loopuser")
    hydrate_mandi = partial(dict_to_foreign_uri,field_name="mandi")

    def obj_create(self, bundle, **kwargs):
        loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
        mandi = Mandi.objects.get(id=bundle.data['mandi']['online_id'])
        attempt = LoopUserAssignedMandi.objects.filter(loop_user=loop_user ,mandi=mandi)
        if attempt.count() < 1:
            bundle = super(LoopUserAssignedMandiResource,self).obj_create(bundle,**kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        try:
            loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
            mandi = Mandi.objects.get(id=bundle.data['mandi']['online_id'])
            #assignedMandi = LoopUserAssignedMandi.objects.filter(loop_user=loop_user,mandi=mandi)
            bundle = super(LoopUserAssignedMandiResource,self).obj_update(bundle, **kwargs)
            # bundle = super(LoopUserAssignedMandiResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            loop_user = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
            mandi = Mandi.objects.get(id=bundle.data['mandi']['online_id'])
            attempt = LoopUserAssignedMandi.objects.filter(loop_user=loop_user ,mandi=mandi)
            send_duplicate_message(int(attempt[0].id))
        return bundle       
    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        return bundle




class IncentiveModelResource(BaseResource):
    class Meta:
        limit = 0
        max_limit = 0
        queryset = IncentiveModel.objects.all()
        allowed_methods = ['get']
        always_return_data = True
        resource_name = 'incentive_model'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        excludes = ('time_created', 'time_modified','is_visible')
        include_resource_uri = False

    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        del bundle.data['id']
        return bundle


class AggregatorIncentiveResource(BaseResource):
    aggregator = fields.ForeignKey(LoopUserResource,'aggregator')
    incentive_model = fields.ForeignKey(IncentiveModelResource,'incentive_model')
    class Meta:
        limit = 0
        max_limit = 0
        queryset = AggregatorIncentive.objects.all()
        allowed_methods =['get','put','post','delete']
        always_return_data = True
        resource_name = 'aggregator_incentive'
        authorization = LoopUserAuthorization('aggregator__in')
        authentication = ApiKeyAuthentication()
        excludes = ('time_created','time_modified','user_created_id','user_modified_id')
        include_resource_uri = False

    dehydrate_aggregator = partial(
        foreign_key_to_id, field_name='aggregator', sub_field_names=['id'])
    dehydrate_incentive_model = partial(
        foreign_key_to_id, field_name='incentive_model', sub_field_names=['id'])

    hydrate_aggregator = partial(dict_to_foreign_uri, field_name='aggregator',resource_name='loopuser')
    hydrate_incentive_model = partial(dict_to_foreign_uri, field_name='incentive_model')

    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        del bundle.data['id']
        return bundle  

    def obj_create(self, bundle, **kwargs):
        aggregator = LoopUser.objects.get(id=bundle.data['aggregator']['online_id'])
        incentive_model = IncentiveModel.objects.get(id=bundle.data['incentive_model']['online_id'])
        attempt = AggregatorIncentive.objects.filter(aggregator=aggregator ,incentive_model=incentive_model,start_date=bundle.data['start_date'])
        if attempt.count() < 1:
            bundle = super(AggregatorIncentiveResource,self).obj_create(bundle,**kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self,bundle):
        bundle.data['online_id']=bundle.data['id']
        return bundle  
