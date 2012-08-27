from tastypie.resources import ModelResource
from dashboard.models import *
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.conf.urls.defaults import patterns, include, url
from tastypie.utils import trailing_slash
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from forms import *
from tastypie import fields
from tastypie.validation import FormValidation

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
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Country).load_all().auto_query(request.GET.get('q', ''))
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
        validation = FormValidation(form_class=StateForm)
    
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
        fields=["start_date","state","district_name","id"]
        ordering = ["start_date","state","district_name"]
        filtering = {
        'district_name': ALL,
        'state':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        validation = FormValidation(form_class=DistrictForm)
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
        validation = FormValidation(form_class=BlockForm)
    
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

class VillageResource(ModelResource):
    block = fields.ForeignKey(BlockResource, 'block')
    class Meta:
        queryset = Village.objects.all()
        resource_name = 'village'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        excludes = ["no_of_households","road_connectivity"]
        ordering = ["start_date","village_name","block","population"]
        filtering = {
        'village_name': ALL,
        'block':ALL_WITH_RELATIONS,
        'start_date': ALL,
        }
        validation = FormValidation(form_class=VillageForm)
    
    def override_urls(self):
        return [
                url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
                ]
    
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        # Do the query.
        sqs = SearchQuerySet().models(Village).load_all().auto_query(request.GET.get('q', ''))
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


