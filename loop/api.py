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


class VillageAuthorization(Authorization):
    def __init__(self, field):
        self.village_field = field

    def read_list(self, object_list, bundle):
        villages = LoopUser.objects.get(
            user_id=bundle.request.user.id).get_villages()
        kwargs = {}
        kwargs[self.village_field] = villages
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.village_field] = LoopUser.objects.get(
            user_id=bundle.request.user.id).get_villages()
        obj = object_list.filter(**kwargs).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Village")


class BlockAuthorization(Authorization):
    def __init__(self, field):
        self.block_field = field

    def read_list(self, object_list, bundle):
        block = LoopUser.objects.get(
            user_id=bundle.request.user.id).village.block
        kwargs = {}
        kwargs[self.block_field] = block
        return object_list.filter(**kwargs).distinct()

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        kwargs = {}
        kwargs[self.block_field] = LoopUser.objects.get(
            user_id=bundle.request.user.id).village.block
        obj = object_list.filter(**kwargs).distinct()
        userObject = LoopUser.objects.get(user_id=bundle.request.user.id)
        if obj or userObject.role == 1:
            return True
        else:
            raise NotFound("Not allowed to download Block")


class MandiAuthorization(Authorization):
    def __init__(self, field):
        self.mandi_field = field

    def read_list(self, object_list, bundle):
        mandis = LoopUser.objects.get(user_id=bundle.request.user.id).get_mandis()
        mandis_list = {}
        mandis_list[self.mandi_field] = mandis
        return object_list.filter(**mandis_list).distinct()

    def read_details(self, object_list, bundle):
        mandis_list = {}
        mandis_list[self.mandi_field] = LoopUser.objects.get(
            user_id=bundle.request.user.id).get_mandis()
        obj = object_list.filter(**mandis_list).distinct()
        if obj:
            return True
        else:
            raise NotFound("Not allowed to download Mandi")

            # def read_list(self, object_list, bundle):
            # villages = LoopUser.objects.get(user_id= bundle.request.user.id).get_villages()
            #     district_list = []
            #     for village in villages:
            #         if village.block.district_id not in district_list:
            #             district_list.append(village.block.district_id)
            #     return object_list.filter(district_id__in = district_list)
            #
            # def read_detail(self, object_list, bundle):
            #     # Is the requested object owned by the user?
            #     villages = LoopUser.objects.get(user_id= bundle.request.user.id).get_villages()
            #     district_list = []
            #     for village in villages:
            #         if village.block.district_id not in district_list:
            #             district_list.append(village.block.district_id)
            #     kwargs={}
            #     kwargs['district_id__in'] = district_list
            #     obj = object_list.filter(**kwargs).distinct()
            #     if obj:
            #         return True
            #     else:
            #         raise NotFound( "Not allowed to download Village" )


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
        # filtering = {'username':ALL,
        # }


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
        queryset = District.objects.all()
        resource_name = 'district'
        authorization = Authorization()
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
        queryset = Block.objects.all()
        resource_name = 'block'
        authorization = Authorization()
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
        allowed_methods = ['post', 'get']
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

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
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
        attempt = Farmer.objects.filter(
            phone=bundle.data['phone'], name=bundle.data['name'])
        if attempt.count() < 1:
            bundle = super(FarmerResource, self).obj_create(bundle, **kwargs)
        else:
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(FarmerResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = Farmer.objects.filter(
                phone=bundle.data['phone'], name=bundle.data['name'])
            send_duplicate_message(int(attempt[0].id))
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['image_path'] = bundle.data['name'] + bundle.data['phone']
        return bundle


class LoopUserResource(BaseResource):
    user = fields.ForeignKey(UserResource, 'user')
    village = fields.ForeignKey(VillageResource, 'village')
    assigned_villages = fields.ListField()
    assigned_mandis = fields.ListField()

    class Meta:
        queryset = LoopUser.objects.prefetch_related(
            'assigned_villages', 'assigned_mandis','user').all()
        resource_name = 'loopuser'
        authorization = Authorization()

    hydrate_user = partial(dict_to_foreign_uri, field_name='user')
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')
    hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m, field_name='assigned_villages',
                                        resource_name='village')
    hydrate_assigned_mandis = partial(dict_to_foreign_uri_m2m, field_name='assigned_mandis', resource_name='mandi')

    dehydrate_user = partial(
        foreign_key_to_id, field_name='user', sub_field_names=['id', 'username'])
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])

    def obj_create(self, bundle, **kwargs):
        bundle = super(LoopUserResource, self).obj_create(bundle, **kwargs)
        assigned_mandi_list = bundle.data.get('assigned_mandis')
        assigned_village_list = bundle.data.get('assigned_villages')
        if assigned_mandi_list or assigned_village_list:
            user_id = None
            if bundle.request.user:
                user_id = bundle.request.user.id

            loop_user_id = getattr(bundle.obj, 'id')

            for mandi in assigned_mandi_list:
                try:
                    assigned_mandi_obj = LoopUserAssignedMandi(loop_user_id=loop_user_id, mandi_id=mandi['mandi_id'],
                                                               user_created_id=user_id)
                    assigned_mandi_obj.save()
                except Exception, e:
                    raise AssignedMandiNotSaved('For Loop User with id: ' + str(
                        loop_user_id) + ' mandi is not getting saved. Mandi details: ' + str(e))

            for village in assigned_village_list:
                try:
                    assigned_village_obj = LoopUserAssignedVillage(loop_user_id=loop_user_id, village_id=village['village_id'],
                                                               user_created_id=user_id)
                    assigned_village_obj.save()
                except Exception, e:
                    raise AssignedVillageNotSaved('For Loop User with id: ' + str(
                        loop_user_id) + ' village is not getting saved. Village details: ' + str(e))
            return bundle
        else:
            raise AssignedMandiNotSaved(
                'Loop User with details: ' + str(bundle.data) + ' can not be saved because mandi list is not available')

    def obj_update(self, bundle, **kwargs):
        # Edit case many to many handling. First clear out the previous related objects and create new objects
        bundle = super(LoopUserResource, self).obj_update(bundle, **kwargs)
        user_id = None
        if bundle.request.user:
            user_id = bundle.request.user.id
        loop_user_id = bundle.data.get('id')
        del_mandi_objs = LoopUserAssignedMandi.objects.filter(
            loop_user_id=loop_user_id).delete()
        del_village_objs = LoopUserAssignedVillage.objects.filter(
            loop_user_id=loop_user_id).delete()
        assigned_mandi_list = bundle.data.get('assigned_mandis')
        for mandi in assigned_mandi_list:
            assigned_mandi_obj = LoopUserAssignedMandi(loop_user_id=loop_user_id, mandi_id=mandi['mandi_id'],
                                                       user_created_id=user_id)
            assigned_mandi_obj.save()
        assigned_village_list = bundle.data.get('assigned_villages')
        for village in assigned_village_list:
            assigned_village_obj = LoopUserAssignedVillage(loop_user_id=loop_user_id, village_id=village['village_id'],
                                                       user_created_id=user_id)
            assigned_village_obj.save()
        return bundle

    def dehydrate_assigned_mandis(self, bundle):
        return [{'id': assigned_mandi_obj.id, 'mandi_name':assigned_mandi_obj.mandi_name} for assigned_mandi_obj in
                set(bundle.obj.assigned_mandis.all())]

    def dehydrate_assigned_villages(self, bundle):
        return [{'id': assigned_village_obj.id, 'village_name':assigned_village_obj.village_name} for assigned_village_obj in
                set(bundle.obj.assigned_villages.all())]

class LanguageResource(BaseResource):
    class Meta:
        limit = 0
        max_limit = 0
        queryset = Language.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'language'
        authorization = Authorization()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    
        
class CropLanguageResource(BaseResource):
    language = fields.ForeignKey(LanguageResource,'language')
    
    class Meta:
        limit = 0
        max_limit = 0
        queryset = CropLanguage.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'croplanguage'
        authorization = Authorization()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    dehydrate_language = partial(
        foreign_key_to_id, field_name='language', sub_field_names=['id','notation'])

class CropResource(BaseResource):
    crops = fields.ToManyField(CropLanguageResource, 'crops', full=True, null=True, blank=True)

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Crop.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'crop'
        authorization = Authorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
 
    def get_object_list(self, request):
        # apply filters from url        
        user = LoopUser.objects.get(user_id=request.user)
        languageFilter = str(user.preferred_language.notation)
        if languageFilter:
            result = super(CropResource, self).get_object_list(request).filter(crops__language__notation=languageFilter)         
        else:
            result = super(CropResource,self).get_object_list(request).filter(crops__language_id=1)
        return result

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Crop.objects.filter(crop_name=bundle.data['crop_name'])
        if attempt.count() < 1:
            bundle = super(CropResource, self).obj_create(bundle, **kwargs)
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
        user = LoopUser.objects.get(user_id=bundle.request.user)
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['crop_name_en'] = bundle.data['crop_name']
        for d in bundle.data['crops']:
            if d.data['language']['notation'] == user.preferred_language.notation:
                bundle.data['crop_name'] = d.data['crop_name']
                break
        del bundle.data['crops']
        return bundle


class MandiResource(BaseResource):
    district = fields.ForeignKey(DistrictResource, 'district')

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ['post', 'get']
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

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

class VehicleLanguageResource(BaseResource):
    language = fields.ForeignKey(LanguageResource,'language')
    
    class Meta:
        limit = 0
        max_limit = 0
        queryset = VehicleLanguage.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'vehiclelanguage'
        authorization = Authorization()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False
    dehydrate_language = partial(
        foreign_key_to_id, field_name='language', sub_field_names=['id','notation'])

class VehicleResource(BaseResource):
    vehicles = fields.ToManyField(VehicleLanguageResource, 'vehicles', full=True, null=True, blank=True)

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

    def get_object_list(self, request):
        # apply filters from url
        user = LoopUser.objects.get(user_id=request.user)
        languageFilter = user.preferred_language.notation
        if languageFilter:
            result = super(VehicleResource, self).get_object_list(request).filter(vehicles__language__notation=languageFilter)         
        else:
            result = super(VehicleResource,self).get_object_list(request).filter(vehicles__language__id=1)
        return result

    def dehydrate(self, bundle):
        user = LoopUser.objects.get(user_id=bundle.request.user)
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['vehicle_name_en'] = bundle.data['vehicle_name']
        for d in bundle.data['vehicles']:
            if d.data['language']['notation'] == user.preferred_language.notation:
                bundle.data['vehicle_name'] = d.data['vehicle_name']
                break
        del bundle.data['vehicles']
        return bundle


class TransporterResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block', full=True)

    class Meta:
        limit = 0
        max_limit = 0
        allowed_methods = ["get", "post", "put", "delete"]
        queryset = Transporter.objects.all()
        resource_name = 'transporter'
        authorization = BlockAuthorization('block')
        authentication = ApiKeyAuthentication()
        always_return_data = True
        excludes = ('time_created', 'time_modified')
        include_resource_uri = False

    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id'])
    # hydrate_block = partial(dict_to_foreign_uri, field_name='village')

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
        authorization = BlockAuthorization('transporter__block')
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
    hydrate_aggregator = partial(dict_to_foreign_uri,field_name='aggregator',resource_name='loopuser')

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
