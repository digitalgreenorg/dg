from tastypie.resources import ModelResource
from dashboard.models import *
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

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

class DistrictResource(ModelResource):
    state = fields.ForeignKey(StateResource, 'state')
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","state","district_name"]
        filtering = {
        'district_name': ALL,
        'state':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
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
class VillageResource(ModelResource):
    block = fields.ForeignKey(BlockResource, 'block')
    class Meta:
        queryset = Village.objects.all()
        resource_name = 'village'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ["start_date","village_name","block","population","no_of_households"]
        filtering = {
        'village_name': ALL,
        'block':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }

