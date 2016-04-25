from tastypie.exceptions import ImmediateHttpResponse, NotFound
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


class FarmerNotSaved(Exception):
    pass


class CropNotSaved(Exception):
    pass


class TransactionNotSaved(Exception):
    pass


class TransporterNotSaved(Exception):
    pass


class TransportationVehicleNotSaved(Exception):
    pass


class DayTransportationNotSaved(Exception):
    pass


def foreign_key_to_id(bundle, field_name, sub_field_names):
    field = getattr(bundle.obj, field_name)
    if (field == None):
        dict = {}
        for sub_field in sub_field_names:
            dict[sub_field] = None
    else:
        dict = model_to_dict(field, fields=sub_field_names, exclude=[])
        dict["online_id"] = dict['id']
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
        if obj:
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
            #     villages = LoopUser.objects.get(user_id= bundle.request.user.id).get_villages()
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
        if obj:
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
        #              }


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
        fields = ["state_name"]
        authorization = Authorization()


class DistrictResource(BaseResource):
    state = fields.ForeignKey(StateResource, 'state', full=True)

    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        fields = ["district_name"]
        authorization = Authorization()


class BlockResource(BaseResource):
    district = fields.ForeignKey(DistrictResource, 'district', full=True)

    class Meta:
        queryset = Block.objects.all()
        resource_name = 'block'
        fields = ["block_name"]
        authorization = Authorization()


class VillageResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block', full=True)

    class Meta:
        allowed_methods = ['post', 'get']
        always_return_data = True
        queryset = Village.objects.all()
        resource_name = 'village'
        authorization = VillageAuthorization('id__in')
        authentication = ApiKeyAuthentication()

    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id', 'block_name'])
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
        queryset = Farmer.objects.all()
        resource_name = 'farmer'
        always_return_data = True
        authorization = VillageAuthorization('village_id__in')
        authentication = ApiKeyAuthentication()

    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])
    hydrate_village = partial(dict_to_foreign_uri, field_name='village')

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Farmer.objects.filter(
            phone=bundle.data['phone'], name=bundle.data['name'])
        if attempt.count() < 1:
            bundle = super(FarmerResource, self).obj_create(bundle, **kwargs)
        else:
            raise FarmerNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(FarmerResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = Farmer.objects.filter(
                phone=bundle.data['phone'], name=bundle.data['name'])
            raise FarmerNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['image_path'] = bundle.data['name'] + bundle.data['phone']
        return bundle


class LoopUserResource(BaseResource):
    user = fields.ForeignKey(UserResource, 'user')
    village = fields.ForeignKey(VillageResource, 'village')
    assigned_villages = fields.ListField()

    class Meta:
        queryset = LoopUser.objects.prefetch_related(
            'assigned_villages', 'user')
        resource_name = 'loopuser'
        authorization = Authorization()

    hydrate_user = partial(dict_to_foreign_uri, field_name='user')
    hyderate_village = partial(dict_to_foreign_uri, field_name='village')
    hydrate_assigned_villages = partial(dict_to_foreign_uri_m2m, field_name='assigned_villages',
                                        resource_name='village')
    dehydrate_user = partial(
        foreign_key_to_id, field_name='user', sub_field_names=['id', 'username'])
    dehydrate_village = partial(
        foreign_key_to_id, field_name='village', sub_field_names=['id', 'village_name'])


class CropResource(BaseResource):

    class Meta:
        limit = 0
        max_limit = 0
        queryset = Crop.objects.all()
        resource_name = 'crop'
        authorization = Authorization()
        always_return_data = True

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Crop.objects.filter(crop_name=bundle.data['crop_name'])
        if attempt.count() < 1:
            bundle = super(CropResource, self).obj_create(bundle, **kwargs)
        else:
            raise CropNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(CropResource, self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = Crop.objects.filter(crop_name=bundle.data['crop_name'])
            raise CropNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        bundle.data['image_path'] = bundle.data['crop_name']
        return bundle


class MandiResource(BaseResource):
    district = fields.ForeignKey(DistrictResource, 'district')

    class Meta:
        allowed_methods = ['post', 'get']
        always_return_data = True
        queryset = Mandi.objects.all()
        resource_name = 'mandi'
        authorization = MandiAuthorization('id__in')
        authentication = ApiKeyAuthentication()

    dehydrate_district = partial(
        foreign_key_to_id, field_name='district', sub_field_names=['id', 'district_name'])
    hydrate_district = partial(dict_to_foreign_uri, field_name='district')

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
        always_return_data = True

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle


class TransporterResource(BaseResource):
    block = fields.ForeignKey(BlockResource, 'block', full=True)

    class Meta:
        queryset = Transporter.objects.all()
        resource_name = 'transporter'
        authorization = BlockAuthorization('block')
        authentication = ApiKeyAuthentication()
        always_return_data = True
    dehydrate_block = partial(
        foreign_key_to_id, field_name='block', sub_field_names=['id', 'block_name'])
    # hydrate_block = partial(dict_to_foreign_uri, field_name='village')

    def obj_create(self, bundle, request=None, **kwargs):
        attempt = Transporter.objects.filter(transporter_phone=bundle.data['transporter_phone'],
                                             transporter_name=bundle.data['transporter_name'])
        if attempt.count() < 1:
            bundle = super(TransporterResource, self).obj_create(
                bundle, **kwargs)
        else:
            raise TransporterNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        try:
            bundle = super(TransporterResource, self).obj_update(
                bundle, **kwargs)
        except Exception, e:
            attempt = Transporter.objects.filter(transporter_phone=bundle.data['transporter_phone'],
                                                 transporter_name=bundle.data['transporter_name'])
            raise TransporterNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle

    def hydrate_block(self, bundle):
        bundle.data['block'] = LoopUser.objects.get(
            user__id=bundle.request.user.id).village.block
        return bundle


class TransportationVehicleResource(BaseResource):
    transporter = fields.ForeignKey(TransporterResource, 'transporter')
    vehicle = fields.ForeignKey(VehicleResource, 'vehicle')

    class Meta:
        queryset = TransportationVehicle.objects.all()
        resource_name = 'transportationvehicle'
        authorization = BlockAuthorization('transporter__block')
        authentication = ApiKeyAuthentication()
        always_return_data = True

    dehydrate_transporter = partial(foreign_key_to_id, field_name='transporter',
                                    sub_field_names=['id', 'transporter_name', 'transporter_phone'])
    dehydrate_vehicle = partial(
        foreign_key_to_id, field_name='vehicle', sub_field_names=['id', 'vehicle_name'])
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
            bundle = super(TransportationVehicleResource,
                           self).obj_create(bundle, **kwargs)
        else:
            raise TransportationVehicleNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
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
            raise TransportationVehicleNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
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
            # print del_obj.id, del_obj.amount
            # print type(del_obj)
            deleted_bundle = self.build_bundle(
                obj=deleted_obj, request=request)
            # print deleted_bundle
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
        detail_allowed_methods = ["get", "post", "put", "delete"]
        resource_name = 'daytransportation'
        authorization = DayTransportationAuthorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True
    dehydrate_transportation_vehicle = partial(foreign_key_to_id, field_name='transportation_vehicle', sub_field_names=[
                                               'id', 'transporter', 'vehicle', 'vehicle_number'])
    hydrate_transportation_vehicle = partial(
        dict_to_foreign_uri, field_name='transportation_vehicle', resource_name='transportationvehicle')
    dehydrate_mandi = partial(
        foreign_key_to_id, field_name='mandi', sub_field_names=['id', 'mandi_name'])
    hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
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


class CombinedTransactionResource(BaseResource):
    crop = fields.ForeignKey(CropResource, 'crop')
    farmer = fields.ForeignKey(FarmerResource, 'farmer')
    mandi = fields.ForeignKey(MandiResource, 'mandi')

    class Meta:
        limit = 0
        max_limit = 0
        detail_allowed_methods = ["get", "post", "put", "delete"]
        queryset = CombinedTransaction.objects.all()
        resource_name = 'combinedtransaction'
        authorization = CombinedTransactionAuthorization()
        authentication = ApiKeyAuthentication()
        always_return_data = True

    dehydrate_farmer = partial(
        foreign_key_to_id, field_name='farmer', sub_field_names=['id', 'name'])
    dehydrate_crop = partial(
        foreign_key_to_id, field_name='crop', sub_field_names=['id', 'crop_name'])
    dehydrate_mandi = partial(
        foreign_key_to_id, field_name='mandi', sub_field_names=['id', 'mandi_name'])
    hydrate_farmer = partial(dict_to_foreign_uri, field_name='farmer')
    hydrate_crop = partial(dict_to_foreign_uri, field_name='crop')
    hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def obj_create(self, bundle, request=None, **kwargs):
        farmer = Farmer.objects.get(id=bundle.data["farmer"]["online_id"])
        crop = Crop.objects.get(id=bundle.data["crop"]["online_id"])
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        attempt = CombinedTransaction.objects.filter(date=bundle.data["date"], price=bundle.data["price"],
                                                     farmer=farmer, crop=crop, mandi=mandi)
        if attempt.count() < 1:
            bundle = super(CombinedTransactionResource,
                           self).obj_create(bundle, **kwargs)
        else:
            raise TransactionNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def obj_update(self, bundle, request=None, **kwargs):
        farmer = Farmer.objects.get(id=bundle.data["farmer"]["online_id"])
        crop = Crop.objects.get(id=bundle.data["crop"]["online_id"])
        mandi = Mandi.objects.get(id=bundle.data["mandi"]["online_id"])
        try:
            bundle = super(CombinedTransactionResource,
                           self).obj_update(bundle, **kwargs)
        except Exception, e:
            attempt = CombinedTransaction.objects.filter(date=bundle.data["date"], price=bundle.data["price"],
                                                         farmer=farmer, crop=crop, mandi=mandi)
            raise TransactionNotSaved(
                {"id": int(attempt[0].id), "error": "Duplicate"})
        return bundle

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
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
            # del_obj = CombinedTransaction.objects.get(id=kwargs['pk'])
            deleted_obj = self.obj_delete(
                bundle=bundle, **self.remove_api_resource_names(kwargs))
            # build a new bundle with the deleted obj and return it in a response
            # print del_obj.id, del_obj.amount
            # print type(del_obj)
            deleted_bundle = self.build_bundle(
                obj=deleted_obj, request=request)
            # print deleted_bundle
            # deleted_bundle = self.full_dehydrate()
            # deleted_bundle = self.alter_detail_data_to_serialize(request, deleted_bundle)
            return self.create_response(request, deleted_bundle, response_class=http.HttpResponse)
        except NotFound:
            return http.Http404()


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

        dehydrate_mandi = partial(foreign_key_to_id, field_name='mandi', sub_field_names=['id', 'mandi_name'])
        hydrate_mandi = partial(dict_to_foreign_uri, field_name='mandi')

    def dehydrate(self, bundle):
        bundle.data['online_id'] = bundle.data['id']
        return bundle
